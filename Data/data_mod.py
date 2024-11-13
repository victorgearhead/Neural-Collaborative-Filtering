import pandas as pd
import numpy as np
from pymongo import MongoClient

df = pd.read_csv('merged_data.csv')

client = MongoClient("MONGODB-URL")
db = client["DATABSE-NAME"]

df["energy"] = pd.to_numeric(df["energy"], errors="coerce")

users_data = [
    {
        "user_id": int(i),
        "user_password": str(i),
        "user_song_language": "English",
        "user_gender": int(np.random.choice([1, 0])),
        "user_age": int(np.random.randint(13, 101))
    }
    for i in range(1, 1000)
]
db.users.insert_many(users_data)

songs_data = [
    {
        "track_id": idx + 1,
        "track": row["Track"],
        "artist": row["Artist"],
        "genre": row["Genre"],
        "language": "english",
        "valence": float(row["Valence"]),
    }
    for idx, row in df.iterrows()
]


y = pd.to_numeric(df["energy"], errors="coerce")

for idx in range(0,len(y)):
    songs_data[idx].update(
        {
            "energy": y[idx],

        }
    )


print("HII")
db.songs.insert_many(songs_data)

user_activity_data = []
ratings_data = []

for i in range(1, 1000):
    track_ids = np.random.choice(range(1, len(df) + 1), size=np.random.randint(10, 5000), replace=False).tolist()

    listened_songs = df.iloc[[track_id - 1 for track_id in track_ids]]
    
    mood_energy = float(listened_songs["energy"].std())
    mood_valence = float(listened_songs["Valence"].std())
    preferred_genre = listened_songs["Genre"].mode()[0]

    user_activity_data.append({
        "user_id": int(i),
        "tracks": track_ids,
        "mood_energy": mood_energy,
        "mood_valence": mood_valence,
        "preferred_genre": preferred_genre,
        "preferred_language": "English",
        "age": int(users_data[i - 1]["user_age"]),
        "language": users_data[i - 1]["user_song_language"]
    })

    for track_id in track_ids:
        ratings_data.append({
            "user_id": int(i),
            "track_id": int(track_id),
            "rating": 1
        })

db.user_activity.insert_many(user_activity_data)
db.ratings.insert_many(ratings_data)

print("Data inserted successfully into MongoDB.")
