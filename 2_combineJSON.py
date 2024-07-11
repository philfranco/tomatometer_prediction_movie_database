'''
Combine the data scraped from youtube.
'''

import json

def combineJsonData(path, channel):
  with open(path, 'r') as f:
    data = json.load(f)
  for i in data:
    i['Channel'] = channel
    i['Title'] = i['Title'].lower()
  return data

youtubeChannelsPaths = ['youtube_scrape//DC.json',
                        'youtube_scrape//20th Century Studios.json',
                        'youtube_scrape//Lionsgate Movies.json',
                        'youtube_scrape//MGM.json',
                        'youtube_scrape//Netflix.json',
                        'youtube_scrape//Paramount Pictures.json',
                        'youtube_scrape//Pixar.json',
                        'youtube_scrape//Sony Pictures Entertainment.json',
                        'youtube_scrape//Universal Pictures.json',
                        'youtube_scrape//Walt Disney Studios.json',
                        'youtube_scrape//Warner Bros. Pictures.json']

youtubeChannels = ['DC',
                   '20th Century Studios',
                   'Lionsgate Movies',
                   'MGM Studios',
                   'Netflix',
                   'Paramount Pictures',
                   'Pixar',
                   'Sony Pictures Entertainment',
                   'Universal Pictures',
                   'Walt Disney Studios',
                   'Warner Bros. Pictures']

data_all = []
for i, channel in enumerate(youtubeChannelsPaths):
  data_out = combineJsonData(channel, youtubeChannels[i])
  data_all = data_all + data_out

with open('__combined_youtube_data.json', 'w') as f:
  json.dump(data_all, f)

# See how many of the videos is a trailer
trailerCount = 0
for title in data_all:
  if "trailer" in title['Title']:
    #print(title['Title'])
    trailerCount = trailerCount + 1
  else:
    print(title['Title'])

print(trailerCount)
#print(len(data_all))
print('complete')

# Prints the length of the data scraped
'''
with open('youtube_scrape//DC.json', 'r') as f:
  DC_data = json.load(f)
print(len(DC_data))

with open('youtube_scrape//20th Century Studios.json', 'r') as f:
  cent_data = json.load(f)
print(len(cent_data))

with open('youtube_scrape//Lionsgate Movies.json', 'r') as f:
  lion_data = json.load(f)
print(len(lion_data))

with open('youtube_scrape//MGM.json', 'r') as f:
  mgm_data = json.load(f)
print(len(mgm_data))

with open('youtube_scrape//Netflix.json', 'r') as f:
  netflix_data = json.load(f)
print(len(netflix_data))

with open('youtube_scrape//Paramount Pictures.json', 'r') as f:
  paramount_data = json.load(f)
print(len(paramount_data))

with open('youtube_scrape//Pixar.json', 'r') as f:
  pixar_data = json.load(f)
print(len(pixar_data))

with open('youtube_scrape//Sony Pictures Entertainment.json', 'r') as f:
  sony_data = json.load(f)
print(len(sony_data))

with open('youtube_scrape//Universal Pictures.json', 'r') as f:
  universa_data = json.load(f)
print(len(universa_data))

with open('youtube_scrape//Walt Disney Studios.json', 'r') as f:
  disney_data = json.load(f)
print(len(disney_data))

with open('youtube_scrape//Warner Bros. Pictures.json', 'r') as f:
  warner_data = json.load(f)
print(len(warner_data))
'''