import requests

# Function to get auth token
def get_auth_token():
    url = "http://20.244.56.144/test/auth"
    data = {
        "companyName": "affordmed",
        "clientID": "3ab0264f-ed01-416e-86a6-3dfe9a5a4f82",
        "clientSecret": "IgxtvNQocMtzwmyP",
        "ownerName": "praveen",
        "ownerEmail": "21btrco030@jainuniversity.ac.in",
        "rollNo": "21btrco030"
    }

    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Authentication failed:", response.status_code, response.text)
        return None
