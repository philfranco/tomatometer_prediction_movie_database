OVERVEIW
The goal of this project was to have each person below collect data from a database, and combine it with the team. We decided to make a move database. This repository shows how the youtube data was scraped, then how the data cleaned, and used to predict the tomatometer (Successfully) and the Revenue (Unsuccessfully).

Conda was used for this code, use the requirements.txt to replicate all that I have done.

The order the files are ran follows:
1_scrape_youtube.py
2_combineJSON.py
3_filter_youtube_data.py
4_combine_data.py
5_predictions.ipynb

File paths will have to be adjusted to run the code.

If you want the .sql database file used, email me at pcfranco05@gmail.com. It is too big to upload to github.

Below are the people on my team, and the APIs we used.

Team Mate | Database | Link
------------------------------------------------------------------------------
Phil Franco	(ME) | Youtube          | https://developers.google.com/youtube/v3
Mike Stewart	   | Box office Mojo  | https://github.com/lamlamngo/Box-Office-Mojo-API
Arbaz Pathan	   | Billboard Charts | https://github.com/guoguo12/billboard-charts
Mike Stewart	   | Metacritic       | https://github.com/ChrisMichaelPerezSantiago/metacritic  – I could not get this work
Arthur Schenker	 | RottenTomatoes   | pip install rottentomatoes-python
Eric Reitinger	 | Oscars           | https://github.com/leandcesar/theawards
                 |                  | https://github.com/zedchance/oscars
Lou Lagonik	     | The Movie DB     | https://developer.themoviedb.org/docs
