import requests

url = "https://api.github.com/repos/SvenHinrichs/GitLabCI/branches"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

import requests

url = "https://api.github.com/repos/SvenHinrichs/GitLabCI/branches/google_charts"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
