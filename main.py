import json
import requests
from http import client

from twilio.rest import Client

product_name = "ZWEIREIHIGER WOLLMANTEL"
product_id = "0917097"

wanted_sizes = ["34", "36", "38"]
wanted_variants = ["Schwarz"]

variants = {
    "003": "Dunkelbraun",
    "001": "Schwarz",
}
sizes = {
    "001": "32",
    "002": "34",
    "003": "36",
    "004": "38",
    "005": "40",
    "006": "42",
    "007": "44",
}

req = requests.get("https://www.cos.com/webservices_cos/service/product/cos-europe/availability/{pid}.json".format(pid=product_id), headers={
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; de-DE)'})

data = json.loads(req.text)

body = ""

for key in data.keys():
    for code in data[key]:
        c_name = code[0: len(product_id)]
        var = variants[code[len(product_id):len(product_id) + 3]]
        size = sizes[code[len(product_id) + 3: len(product_id) + 6]]
        if (var in wanted_variants and size in wanted_sizes):
            body += " ".join([product_name, ":", var,
                             size, "[", key, "]", '\n'])


print(body)
if body == "":
    exit()

account_sid = 'AC9bd34e5eadbd93cc008a643c2e298b53'
auth_token = '03972a1fb932bf2616f0bccd00a0560e'
client = Client(account_sid, auth_token)


message = client.messages.create(
    messaging_service_sid='MG7260a7192c1839ead7a753c89df0c6ce',
    body=body,
    to='+491749300842'
)
