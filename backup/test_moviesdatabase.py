# Not used, but one of my teammates got an API key for the movie data base.
# file used for testing

import requests

url = "https://moviesdatabase.p.rapidapi.com/titles/search/akas/Rocky"

headers = {
	"X-RapidAPI-Key": "get your own",
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
}
s
response = requests.get(url, headers=headers)

print(response.json())