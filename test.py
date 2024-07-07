import requests

url = 'http://<ip>4:5000/add-question'
payload = {
    "company": "Google",
    "type": "String Manipulation",
    "description": "Reverse a string without using built-in functions.",
    "aas": 7,
    "difficulty_score": 5
}
response = requests.post(url, json=payload)
print(response.json())d