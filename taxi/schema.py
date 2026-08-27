import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Order
from .services import estimate_price


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            'id',
            'name',
            'phone',
            'from_address',
            'to_address',
            'comment',
            'driver_note',
            'estimated_price',
            'status',
            'created_at',
            'updated_at',
        )


def require_auth(info):
    user = info.context.user
    if not user.is_authenticated:
        raise GraphQLError('Требуется авторизация.')
    return user


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(root, info):
        user = require_auth(info)
        queryset = Order.objects.all()
        if not user.can_dispatch:
            queryset = queryset.filter(user=user)
        return queryset.order_by('-created_at')


class CreateOrder(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        phone = graphene.String(required=True)
        from_address = graphene.String(required=True)
        to_address = graphene.String(required=True)
        comment = graphene.String(required=False)

    order = graphene.Field(OrderType)

    def mutate(self, info, name, phone, from_address, to_address, comment=None):
        user = require_auth(info)
        order = Order.objects.create(
            user=user,
            name=name,
            phone=phone,
            from_address=from_address,
            to_address=to_address,
            comment=comment or '',
            estimated_price=estimate_price(from_address, to_address),
        )
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
