from googlesearch import search
import requests

query = "When was elden ring released"
search_results = search(query, num_results=1)

url = next(search_results)
response = requests.get(url)
text = response.text

print(text)