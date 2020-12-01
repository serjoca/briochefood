import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from app.graphql.object import Bakery as Bakery, Product as Product, Order as Order

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    products = SQLAlchemyConnectionField(Product)
    bakeries = SQLAlchemyConnectionField(Bakery)
    orders = SQLAlchemyConnectionField(Order)
