import json

import requests


class CartClient:
    def __init__(self, cookies, env):
        self.cookies = cookies
        self.base_url_cart = f"https://app-cart-{env}.azurewebsites.net/"

    def make_request(self, url, method, payload=None):
        response = requests.request(method, url, json=payload, cookies=self.cookies)
        return response

    def get_cart_id(self, cart):
        return cart["carts"][0]["id"]

    def get_lines(self, cart):
        return cart["carts"][0]["lines"]

    def get_first_line_id(self, cart):
        return self.get_lines(cart)[0]['lineId']

    def create_cart(self, quantity):
        url = f"{self.base_url_cart}/carts"
        #with open('cart_payload.json', 'r') as openfile:
            #Reading from json file
            #payload = json.load(openfile)

        payload = {
            "lines": [
                {
                    "itemNumber": "00460285",
                    "itemType": "ART",
                    "quantity": quantity
                },
            ],
            "reduceInvalidQuantity": True
        }

        response = self.make_request(url, "POST", payload=payload)
        with open(f"created_cart.json", "w", encoding="utf-8") as f:
            # Write the JSON object to the file
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        return self.get_cart()

    def delete_cart(self, cart_id):
        url = f"{self.base_url_cart}carts/{cart_id}"
        return self.make_request(url, "DELETE")

    def get_cart(self):
        url = f"{self.base_url_cart}carts?includePrices=true&skipSync=true&includeMaxQuantity=true"
        response = self.make_request(url, "GET")
        cart = response.json()
        with open(f"cart.json", "w", encoding="utf-8") as f:
            # Write the JSON object to the file
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        return cart

    def add_line(self, cart_id, quantity):
        url = f"{self.base_url_cart}carts/{cart_id}/lines"
        payload = {
            "itemNumber": "10487816",
            "itemType": "ART",
            "quantity": quantity,
            "reduceInvalidQuantity": False
        }
        response = self.make_request(url, "POST", payload=payload)
        with open(f"add_line.json", "w", encoding="utf-8") as f:
            # Write the JSON object to the file
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

    def add_line_batch(self, cart_id):
        url = f"{self.base_url_cart}carts/{cart_id}/lines/batch"
        with open('cart_payload.json', 'r') as openfile:
            # Reading from json file
            payload = json.load(openfile)

        response = self.make_request(url, "POST", payload=payload)
        with open(f"add_line_batch.json", "w", encoding="utf-8") as f:
            # Write the JSON object to the file
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return response

    def line_quantity_change(self, cart_id, line_id, quantity):
        url = f"{self.base_url_cart}carts/{cart_id}/lines/{line_id}/quantity-change"
        payload = {
            "quantity": quantity
        }
        response = self.make_request(url, "POST", payload=payload)
        if response.status_code != 201:
            error = F"line_quantity_change response code is: {response.status_code}, with error {response.text}"
            raise Exception(error)
        with open(f"quantity_change.json", "w", encoding="utf-8") as f:
            # Write the JSON object to the file
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return response

if __name__ == "__main__":
    cookies = {"WC_AUTHENTICATION_01edfb83-25dd-148a-bfa3-e73ccdf76df7": "<value>",
"WC_USERACTIVITY_01edfb83-25dd-148a-bfa3-e73ccdf76df7": "<value>"}

    cartClient = CartClient(cookies=cookies, env="qa-co-01")
    cart = cartClient.get_cart()
    cartClient.add_line(cartClient.get_cart_id(cart), quantity=1)
