from inspect import Arguments
import graphene

from app import db
from app.graphql.object import ItemsInput, Bakery as Bakery, Product as Product, Order as Order
from app.model import Bakery as BakeryModel, Product as ProductModel, Order as OrderModel, OrderDetails as OrderDetailsModel
from app.services.pagarme import cancel_transaction, create_recipient, create_transaction


class BakeryMutation(graphene.Mutation):
    class Arguments:
        bank_code = graphene.String(required=True)
        agencia = graphene.String(required=True)
        agencia_dv = graphene.String(required=True)
        conta = graphene.String(required=True)
        conta_dv = graphene.String(required=True)
        document_number = graphene.String(required=True)
        legal_name = graphene.String(required=True)
        name = graphene.String(required=True)

    bakery = graphene.Field(lambda: Bakery)
    
    def mutate(self, info, bank_code, agencia, agencia_dv, conta, conta_dv, document_number, legal_name, name):
        data = {
            "bank_code": bank_code,
            "agencia": agencia,
            "agencia_dv": agencia_dv,
            "conta":conta,
            "conta_dv": conta_dv,
            "document_number": document_number,
            "legal_name":legal_name,
            "type": "conta_corrente"
        }

        bakery = BakeryModel(name=name)

        recipient = create_recipient(data)
        bakery.recipient_id = recipient["id"]

        db.session.add(bakery)
        db.session.commit()

        return BakeryMutation(bakery=bakery)

class ProductMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        bakery_id = graphene.Int(required=True)

    product = graphene.Field(lambda: Product)
    
    def mutate(self, info, name, price, bakery_id):
        bakery = BakeryModel.query.get(bakery_id)

        product = ProductModel(name=name, price=price)

        product.bakery = bakery

        db.session.add(product)
        db.session.commit()

        return ProductMutation(product=product)

class OrderMutation(graphene.Mutation):
    class Arguments:
        bakery_id = graphene.Int(required=True)
        items = graphene.List(ItemsInput, required=True)
        card_number = graphene.String(required=True)
        card_cvv = graphene.String(required=True)
        card_expiration_date = graphene.String(required=True)
        card_holder_name = graphene.String(required=True)
        name = graphene.String(required=True)
        country = graphene.String(required=True)
        state = graphene.String(required=True)
        city = graphene.String(required=True)
        neighborhood = graphene.String(required=True)
        street = graphene.String(required=True)
        street_number = graphene.String(required=True)
        zipcode = graphene.String(required=True)

    order = graphene.Field(lambda: Order)

    def mutate(self, info, bakery_id, items, card_number, card_cvv, card_expiration_date, card_holder_name, name, country, state, city, neighborhood, street, street_number, zipcode,):
        data = {
            "card_number":  card_number,
            "card_cvv":  card_cvv,
            "card_expiration_date":  card_expiration_date,
            "card_holder_name":  card_holder_name,
            "name":  name,
            "country":  country,
            "state":  state,
            "city":  city,
            "neighborhood":  neighborhood,
            "street":  street,
            "street_number":  street_number,
            "zipcode":  zipcode,
        }

        bakery = BakeryModel.query.get(bakery_id)

        product_list = [ProductModel.query.get(input_item.product_id) for input_item in items]

        order = OrderModel(bakery_id=bakery_id, bakery=bakery)

        items_list = [OrderDetailsModel(order_id=order.id, product_id=input_item.product_id, quantity=input_item.quantity) for input_item in items]
        
        payment_items = list()

        for product, item in zip(product_list, items_list):
            payment_items.append({
                "id": product.id,
                "title": product.name,
                "unit_price": product.price,
                "quantity": item.quantity,
                "tangible": True
            })

        total_price = sum(item["unit_price"] * item["quantity"] for item in payment_items) * 100 # total_price is in cents
        
        payment_response = create_transaction(bakery.recipient_id, total_price, payment_items, data)

        order.items.extend(items_list)
        order.total_price = total_price
        order.transaction_id = payment_response["id"]
        order.status = payment_response["status"]

        db.session.add(order)
        db.session.commit()

        return OrderMutation(order=order)

class CancelOrderMutation(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)

    order = graphene.Field(lambda: Order)

    def mutate(self, info, order_id):
        order = OrderModel.query.get(order_id)

        cancel_transaction_response = cancel_transaction(order.transaction_id)

        print(cancel_transaction_response)
        
        order.status = cancel_transaction_response["status"]
        
        db.session.commit()

        return CancelOrderMutation(order=order)


class Mutation(graphene.ObjectType):
    mutate_bakery = BakeryMutation.Field()
    mutate_product = ProductMutation.Field()
    mutate_order = OrderMutation.Field()
    cancel_order = CancelOrderMutation.Field()
