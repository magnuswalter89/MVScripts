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
    cookies = {"WC_AUTHENTICATION_01edfb83-25dd-148a-bfa3-e73ccdf76df7": "MDFlZGZiODMtMjVkZC0xNDhhLWJmYTMtZTczY2NkZjc2ZGY3fGNv",
"WC_USERACTIVITY_01edfb83-25dd-148a-bfa3-e73ccdf76df7": "MDFlZGZiODMtMjVkZC0xNDhhLWJmYTMtZTczY2NkZjc2ZGY3fGNvfHBhc3N3b3JkSW52YWxpZGF0aW9uRmxhZ3xhdHRlbXB0ZWRQYXNzd29yZFByb3RlY3RlZENvbW1hbmRzfGxvZ29uVGltZXxleHBpcnlUaW1lfGV4cGlyZWRVc2VySWR8cHJlRXhwaXJ5VVJMfGZvclVzZXJJZHxhY3RpdmVPcmdJZA==|F77xiPcA3X32JQddum+m8p+6vRtBlfi3Q7Was+TZ0csnCyas66ckMDdfieEgs2QtlDwQzSRaKA9SK6Q1EhQEL9mRBw2a4Wd6Jq105x2Y+QiVd8vKTVeTzJL63U9Sos239Iw+UP48lf9kxOcvq4KEavjeMqtceV6KY7sJDXy5vnB7JfaF9imIx+r/uujHSyDrMLrnx3Z/MobQHpVvgE2PH7XEVChOvEY16C0k9B3WFmdTXCW5h8u1Eg=="}

    cartClient = CartClient(cookies=cookies, env="qa-co-01")
    cart = cartClient.get_cart()
    cartClient.add_line(cartClient.get_cart_id(cart), quantity=1)