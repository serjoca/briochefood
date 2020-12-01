import os
import json
import requests

pagarme_url = "https://api.pagar.me"

def create_recipient(data):
    result = requests.post(pagarme_url + "/1/recipients", data=json.dumps({
        "anticipatable_volume_percentage": "85", 
        "api_key": os.environ["PAGARME_API_KEY"],
        "automatic_anticipation_enabled": "true", 
        "bank_account": {
            "bank_code": data["bank_code"],
            "agencia": data["agencia"],
            "agencia_dv": data["agencia_dv"],
            "conta": data["conta"],
            "type": data["type"],
            "conta_dv": data["conta_dv"],
            "document_number": data["document_number"],
            "legal_name": data["legal_name"],
        }, 
        "transfer_day": "5", 
        "transfer_enabled": "true", 
        "transfer_interval": "weekly",
        "postback_url": "https://requestb.in/tl0092tl"
    }), headers={"content-type": "application/json"})

    return result.json()

def create_transaction(recipient_id, total_price, payment_items, data):
    result = requests.post(pagarme_url + '/1/transactions', data=json.dumps({
        "api_key": os.environ["PAGARME_API_KEY"],
        "amount": total_price,
        "card_number": data["card_number"],
        "card_cvv": data["card_cvv"],
        "card_expiration_date": data["card_expiration_date"],
        "card_holder_name": data["card_holder_name"],
        "billing": {
            "name": data["name"],
            "address": {
                "country": data["country"],
                "state": data["state"],
                "city": data["city"],
                "neighborhood": data["neighborhood"],
                "street": data["street"],
                "street_number": data["street_number"],
                "zipcode": data["zipcode"],
            }
        },
        "items": payment_items,
        "split_rules": [
            {
                "recipient_id": recipient_id,
                "percentage": 85,
                "liable": True,
                "charge_processing_fee": True
            },
            {
                "recipient_id": os.environ["PAGARME_DEFAULT_RECIPIENT_ID"],
                "percentage": 15,
                "liable": True,
                "charge_processing_fee": True
            }
        ]
    }), headers={"content-type": "application/json"})

    return result.json()

def cancel_transaction(transaction_id):
    result = requests.post(pagarme_url + "/1/transactions/" + transaction_id + "/refund", data=json.dumps({
        "api_key": os.environ["PAGARME_API_KEY"],
    }), headers={"content-type": "application/json"})

    return result.json()
