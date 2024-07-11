import pandas as pd
import json
from datetime import datetime as dt

# read in movies from sql database
df = pd.read_csv("allMovies.csv")
df['MOVIE_TITLE'] = df['MOVIE_TITLE'].apply(str.lower)
#df = df.sort_values(by=['MOVIE_TITLE'])

with open('...\\youtube_scrape\\__combined_youtube_data.json', 'r') as f:
  yt_data = json.load(f)

df2 = pd.DataFrame()

# add view and like column
df2['MOVIE_TITLE'] = 0
df2['MOVIE_ID'] = 0
df2['RELEASE_DATE'] = 0
df2['RELEASE_YEAR'] = 0
df2['yt_releaseDate'] = 0
df2['yt_releaseYear'] = 0
df2['yt_likes'] = 0
df2['yt_views'] = 0
df2['yt_videoTitle'] = ''
df2['time_trailerToMovie_Days'] = 0

# Start of youtube
FILTER_YEAR = 2007

len_ytData= len(yt_data)
idx = 0

while idx < len_ytData :
  year = yt_data[idx]["Published_date"][0:4]
  if int(year) > FILTER_YEAR:
    yt_data[idx]['year'] = int(yt_data[idx]["Published_date"][0:4])
    idx = idx + 1
  else:
    yt_data.pop(idx)
    len_ytData = len_ytData - 1

filteredMoviesList = ['air', '65', '5 years', 'alive', 'x', 'dog', 'generation', 'gold', 'need', 'rise', 'milk', 'fall', 'wood', 'plane', 'her', 'i',
                      '83', '24', '31', '911', 'all', 'after', 'aline', 'anna', 'ascending', 'agaust', 'ava', 'camp', 'fan', 'fire', 'frank', 'it', 'zoo',
                      'war', 'waves', 'wild', 'wonder', 'zoo', 'amsterdam', 'captain', 'cake', 'bumblebee', 'burning', 'brothers', 'bros', 'boss', 'book club',
                      'anon', 'circle', 'charming', 'cats', 'bottle', 'atm', 'music', 'old', 'run', 'the man', 'us', 'walk', 'like', 'life', 'lion', 'little',
                      'love', 'lost', 'i', 'ii', 'iii']

count = 0
for index, row in df.iterrows():
  if(row['RELEASE_YEAR']) > FILTER_YEAR:
    likes = 0
    views = 0

    if row['MOVIE_TITLE'] in filteredMoviesList:
      continue
    for ytRow in yt_data:
      yearDiff = row['RELEASE_YEAR'] - ytRow["year"]

      if yearDiff > -1 and yearDiff < 2 and row['MOVIE_TITLE'] in ytRow['Title'] and views < int(ytRow['Views']):
        views = int(ytRow['Views'])
        likes = int(ytRow['Likes'])
        year = int(ytRow['year'])
        youtubeTitle = ytRow['Title']
        date = ytRow['Published_date']

        #print(row['MOVIE_TITLE'])
        #print(row['RELEASE_YEAR'])
        #print(ytRow['Title'])
        #print(ytRow["year"])
        #print()

    if views > 0:
      databaseDate_dt = dt.strptime(row['RELEASE_DATE'], '%Y-%m-%d')
      ytDate_dt = dt.strptime(date[0:10], '%Y-%m-%d')
      diff = databaseDate_dt - ytDate_dt

      df.loc[index, 'yt_likes'] = likes
      df.loc[index, 'yt_views'] = views

      df2.loc[count,'MOVIE_TITLE'] = row['MOVIE_TITLE']
      df2.loc[count,'MOVIE_ID'] = row['MOVIE_ID']
      df2.loc[count,'RELEASE_YEAR'] = row['RELEASE_YEAR']
      df2.loc[count,'RELEASE_DATE'] = row['RELEASE_DATE']
      df2.loc[count,'yt_releaseYear'] = year
      df2.loc[count,'yt_releaseDate'] = date[0:10]
      df2.loc[count,'yt_likes'] = likes
      df2.loc[count,'yt_views'] = views
      df2.loc[count,'yt_videoTitle'] = youtubeTitle

      df2.loc[count, 'time_trailerToMovie_Days'] = diff.days

      count = count + 1

df2.to_csv('...\\csvs\\database_csvs\\youtube_data.csv', index = False)

print(count)

#####################################################################################
'''
low = 99999
# Check for the earliest youtube (2007 is the answer)
for row in yt_data:
    year = row["Published_date"][0:4]
    year = int(year)
    if year < low:
      low = year
      print(year)


# 5944 movies after 2006
count = 0
for index, row in df.iterrows():
    if(row['RELEASE_YEAR']) > 2006:
        count = count  + 1

print(count)
'''