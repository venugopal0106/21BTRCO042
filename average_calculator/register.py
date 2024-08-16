import requests

url = "http://20.244.56.144/test/register"
data = {
    "companyName": "affordmed",
    "ownerName": "praveen",
    "rollNo": "21btrco030",
    "ownerEmail": "21btrco030@jainuniversity.ac.in",
    "accessCode":"nfFxGc"
}

response = requests.post(url, json=data)
print(response.json())
