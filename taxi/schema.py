import graphene
from graphene_django.types import DjangoObjectType
from .models import Order

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(self, info):
        return Order.objects.all()

schema = graphene.Schema(query=Query)
