import pandas as pd 
import random

from pandas.core.frame import DataFrame

def get_movies():
    df = pd.read_csv("rovot/dataset/netflix_titles.csv")

    df = df.loc[df['type'] == 'Movie']

    return df

def dataframe_to_ctx(dataframe: pd.DataFrame) -> dict:
    ctx = {
        'movies': []
    }

    for index, rows in dataframe.iterrows():
        temp = {}
        temp['title'] = rows['title']
        temp['diretor'] = rows['director']
        temp['cast'] = rows['cast']
        temp['country'] = rows['country']
        temp['date_added'] = rows['date_added']
        temp['release_year'] = rows['release_year']
        temp['rating'] = rows['rating']
        temp['duration'] = rows['duration']
        temp['listed_in'] = rows['listed_in']
        temp['description'] = rows['description']

        ctx['movies'].append(temp)
    
    return ctx

def generate_recommendation(genre, size=3):
    genre_map = {
        "fear": ("Sci-Fi & Fantasy",
            "Thrillers",
            "Independent Movies",
            "Documentaries",
            "Anime Features,"
            "Cult Movies",
            "International Movies",
            "Horror Movies",
            "LGBTQ Movies",
            "Action & Adventure",
            "Music & Musicals"
        ),
        "sadness": ("Independent Movies",
            "Documentaries",
            "Classic Movies",
            "Anime Features",
            "Cult Movies",
            "International Movies",
            "Dramas",
            "LGBTQ Movies",
            "Music & Musicals"
        ),
        "anger": ("Independent Movies",
            "Documentaries",
            "Anime Features",
            "Cult Movies",
            "International Movies",
            "Music & Musicals"
        ),
        "love": ("Children & Family Movies",
            "Independent Movies",
            "Documentaries",
            "Classic Movies",
            "Romantic Movies",
            "Anime Features",
            "Stand-Up Comedy & Talk Shows",
            "Cult Movies",
            "International Movies",
            "Sports Movies",
            "Dramas",
            "LGBTQ Movies",
            "Music & Musicals",
            "Faith & Spirituality"
        ),
        "joy": ("Children & Family Movies",
            "Independent Movies",
            "Documentaries",
            "Stand-Up Comedy",
            "Anime Features",
            "Comedies",
            "Stand-Up Comedy & Talk Shows",
            "Cult Movies",
            "International Movies",
            "LGBTQ Movies",
            "Action & Adventure",
            "Music & Musicals",
            "Faith & Spirituality"
        ),
        "surprise": ("Sci-Fi & Fantasy",
                "Thrillers",
                "Independent Movies",
                "Documentaries",
                "Anime Features",
                "Stand-Up Comedy & Talk Shows",
                "Cult Movies",
                "International Movies",
                "Sports Movies",
                "Dramas",
                "Horror Movies",
                "LGBTQ Movies",
                "Action & Adventure",
                "Music & Musicals"
        )
    }

    df = get_movies()

    dataframes = []
    for _ in range(size):
        df_genre = df.loc[df['listed_in'].str.contains(random.choice(genre_map[genre]))]

        dataframes.append(df_genre.sample())
    
    df_recommendation = pd.concat(dataframes)
    
    return df_recommendation