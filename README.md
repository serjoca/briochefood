# Briochefood

[GraphQL](https://graphql.org/) API built with [Flask](https://graphql.org/), MySQL, [SQLAlchemy](https://www.sqlalchemy.org/), [Graphene](https://graphene-python.org/) and Python 3.7

This app is intended to run with Docker and is composed of 4 basic entities (Bakery, Product, Order, orderDetails) that are exposed with both queries and mutations in a GraphQL API.

## Prerequisites

- Docker
- Docker Compose

## Run

This application is deployed in its own Docker image and the database is in a MySQL image. In order to run them both, there's a Docker Compose yml file ready to go:

```bash
    $ docker-compose up
```

To test the application, access http://localhost:5000/graphql

## Examples

This application implements both mutations and queries. For a complete payment flow integrating with the Pagarme API we can do the following:

1. Create a new bakery. You can do this by using the following GraphQL mutation on http://localhost:5000/graphql

```javascript
mutation {
	mutateBakery(
		bankCode: "341"
		agencia: "0932"
		agenciaDv: "5"
		conta: "58054"
		contaDv: "1"
		documentNumber: "26268738888"
		legalName: "Três Irmãos"
		name: "Padaria Três Irmãos"
	) {
		bakery {
			id
			name
			recipientId
			products {
				id
				name
			}
		}
	}
}
```

2. When creating a bakery, it will receive a `recipientId` from Pagarme. Now we can create two products, bread and milk, by using the following GraphQL mutation:

```javascript
mutation {
	createBread: mutateProduct(bakeryId: 1, name: "Pão de Milho", price: 4.5) {
		product {
			id
			name
			price
			bakeryId
			bakery {
				id
				name
			}
		}
	}
  createMilk: mutateProduct(bakeryId: 1, name: "Milk", price: 6.5) {
		product {
			id
			name
			price
			bakeryId
			bakery {
				id
				name
			}
		}
	}
}
```

3. We can now create an order that will use both the bakery's id and the products that we created.

```javascript
mutation {
	mutateOrder(
		cardNumber: "4111111111111111"
		cardCvv: "123"
		cardExpirationDate: "0922"
		cardHolderName: "Morpheus Fishburne"
		name: "Trinity Moss"
		country: "br"
		state: "sp"
		city: "Cotia"
		neighborhood: "Rio Cotia"
		street: "Rua Matrix"
		streetNumber: "9999"
		zipcode: "06714360"
		bakeryId: 1
		items: [{ productId: 1, quantity: 2 }, { productId: 2, quantity: 4 }]
	) {
		order {
			id
			status
			totalPrice
			transactionId
			bakery {
				id
				name
				recipientId
			}
			items {
				id
				quantity
				product {
					id
					name
					price
				}
			}
		}
	}
}
```

4. Since we also sent the card's information we were able to complete our transaction and pay our order right after creating it. If anything went wrong and we want to refund it, we can do it by using the following GraphQL mutation:

```javascript
mutation {
	cancelOrder(orderId: 1) {
		order {
			id
			status
			totalPrice
			transactionId
			bakery {
				id
				name
				recipientId
			}
			items {
				id
				quantity
				product {
					id
					name
					price
				}
			}
		}
	}
}
```

We now completed our payment flow. Since the database has been modeled as a Graph, we are able to query for any entity starting from any query of our database =)

Feel free to explore the GraphQL queries and see you next time! o/

## References

- [How to GraphQL](https://www.howtographql.com/)
- [Graphene docs](https://docs.graphene-python.org/en/latest/)
- [GraphQL vs Rest API architecture](https://medium.com/swlh/graphql-vs-rest-api-architecture-3b95a77512f5)
