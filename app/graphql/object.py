import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.model import Bakery as BakeryModel, Product as ProductModel, Order as OrderModel, OrderDetails as OrderDetailsModel


class Bakery(SQLAlchemyObjectType):
    class Meta:
        model = BakeryModel
        interfaces = (relay.Node,)

    products = graphene.List(lambda: Product, name=graphene.String(), price=graphene.Float())

    def resolve_products(self, info, name=None, price=None):
        query = Product.get_query(info=info)
        query = query.filter(ProductModel.bakery_id == self.id)

        if name:
            query = query.filter(ProductModel.name == name)

        return query.all()


class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node,)

class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node,)
    
    items = graphene.List(lambda: OrderDetails, quantity=graphene.Int(), product_id=graphene.Int())

    def resolve_items(self, info):
        query = OrderDetails.get_query(info=info)
        query = query.filter(OrderDetailsModel.order_id == self.id)

        return query.all()


class OrderDetails(SQLAlchemyObjectType):
    class Meta:
        model = OrderDetailsModel
        interfaces = (relay.Node,)

    product = graphene.List(lambda: Product, name=graphene.String(), price=graphene.Float())

    def resolve_product(self, info):
        query = Product.get_query(info=info)
        query = query.filter(ProductModel.id == self.product_id)

        return query.all()

class ItemsInput(graphene.InputObjectType):
    product_id = graphene.Int()
    quantity = graphene.Int()