import graphene
from graphene_django import DjangoObjectType
from .models import Order

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "phone",
            "from_address",
            "to_address",
            "comment",
            "status",
            "created_at",
            "updated_at",
        )

class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(root, info):
        return Order.objects.all()

class CreateOrder(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        phone = graphene.String(required=True)
        from_address = graphene.String(required=True)
        to_address = graphene.String(required=True)
        comment = graphene.String(required=False)

    order = graphene.Field(OrderType)

    def mutate(self, info, name, phone, from_address, to_address, comment=None):
        order = Order.objects.create(
            name=name,
            phone=phone,
            from_address=from_address,
            to_address=to_address,
            comment=comment or "",
        )
        return CreateOrder(order=order)

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
