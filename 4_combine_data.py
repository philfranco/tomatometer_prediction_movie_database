'''
Combines the data from my teammates scraped data sets to my dataset.
Prepare the data to be used for a nueral net to predict the tomatometer.
'''

import string as s
import pandas as pd
import numpy as np

df = pd.DataFrame()

# add view and like column
df['MOVIE_ID'] = 0
df['BUDGET'] = 0
df['REVENUE'] = 0
df['POPULARITY'] = 0
df['RUNTIME'] = 0
df['VOTE_AVERAGE'] = 0
df['VOTE_COUNT'] = 0

# load in dataframes
#genres_df = pd.read_csv("csvs/movieGenres.csv")
money_df = pd.read_csv("csvs/revenue.csv")
awards_df = pd.read_csv("csvs/movies_rottonAwards.csv")
yt_df = pd.read_csv("csvs/allMovies_youtubeData.csv")

money_df = money_df.drop_duplicates()
awards_df = awards_df.drop_duplicates()

# replace nan
awards_df["Nominations"] = awards_df["Nominations"].replace(np.nan, 0)
awards_df["Awards"] = awards_df["Awards"].replace(np.nan, 0)

count = 0

countMissing = 0
for index, row in yt_df.iterrows():
  mask = money_df['MOVIE_ID'].values == row['MOVIE_ID']
  mask2 = awards_df['ID'].values == row['MOVIE_ID']

  # capped the money at 100000000
  if len(money_df[mask]['MOVIE_ID']) > 0 and \
     len(awards_df[mask2]['ID']) > 0 and \
     int(money_df[mask]['VOTE_COUNT']) > 4 and \
     'NaN' not in str(awards_df[mask2]['Rating']) and \
     row['time_trailerToMovie_Days'] > -1 and \
     int(money_df[mask]['REVENUE']) < 100000000:

    df.loc[count,'MOVIE_ID'] = row['MOVIE_ID']
    df.loc[count,'MOVIE_TITLE'] = row['MOVIE_TITLE']
    df.loc[count,'RELEASE_YEAR'] = row['RELEASE_YEAR']
    df.loc[count,'RELEASE_DATE'] = row['RELEASE_DATE']
    df.loc[count,'yt_releaseYear'] = row['yt_releaseYear']
    df.loc[count,'yt_releaseDate'] = row['yt_releaseDate']
    df.loc[count,'yt_likes'] = row['yt_likes']
    df.loc[count,'yt_views'] = row['yt_views']
    df.loc[count,'time_trailerToMovie_Days'] = row['time_trailerToMovie_Days']

    df.loc[count, 'BUDGET'] = int(money_df[mask]['BUDGET'])
    df.loc[count, 'REVENUE'] = int(money_df[mask]['REVENUE'])
    df.loc[count, 'POPULARITY'] = int(money_df[mask]['POPULARITY'])
    df.loc[count, 'RUNTIME'] = int(money_df[mask]['RUNTIME'])
    df.loc[count, 'VOTE_AVERAGE'] = int(money_df[mask]['VOTE_AVERAGE'])
    df.loc[count, 'VOTE_COUNT'] = int(money_df[mask]['VOTE_COUNT'])

    endOfString = str(awards_df[mask2]['Rating']).find('\n')
    rating = str(awards_df[mask2]['Rating'])[8:endOfString]

    if rating == "G":
      ratingNum = 0
    elif rating == "PG":
      ratingNum = 1
    elif rating == "PG-13":
      ratingNum = 2
    elif rating == "G-13":
      ratingNum = 2
    elif rating == "R":
      ratingNum = 3
    elif rating == "":
      ratingNum = 3

    df.loc[count, 'Rating'] = ratingNum
    df.loc[count, 'Tomatometer'] = int(awards_df[mask2]['Tomatometer'])
    df.loc[count, 'Weighted_Score'] = int(awards_df[mask2]['Weighted_Score'])
    df.loc[count, 'Audience_Score'] = int(awards_df[mask2]['Audience_Score'])
    df.loc[count, 'Awards'] = int(awards_df[mask2]['Awards'])
    df.loc[count, 'Nominations'] = int(awards_df[mask2]['Nominations'])
    count = count + 1
  else:
    countMissing = countMissing + 1

print(count)
print(countMissing)

df.to_csv('csvs/comb_money_cap.csv', index = False)
