from context_model_loader import LoadModel
from top_song_matcher import RetrieveSongs
import pandas as pd

loader = LoadModel('knn_200_model.pkl')
knn_200_model = loader.model

loader = LoadModel('knn_query_model.pkl')
knn_query_model = loader.model

loader = LoadModel('knn_vectorizer.pkl')
knn_vectorizer = loader.model

data_folder = '/Users/cep4u/JingEdward/tunen/data/content_rawdata'
filename = 'spotify_audio_content_db_2M_standardized.csv'
file_path = f"{data_folder}/{filename}"

df = pd.read_csv(file_path)

with open("x_train_columns.txt", "r") as f:
    x_train_columns = f.readlines()

x_train_column_list = [feature.strip() for feature in x_train_columns]

x_data = df[x_train_column_list]

def main():
    retriever = RetrieveSongs(df, x_data, knn_200_model, knn_query_model, knn_vectorizer)

    query = input("Please type in the song and artist: ")
    
    song = retriever.search_song(query)
    song_id = song.index.tolist()[0]
    nn_200_indices = retriever.get_nearest_neighbors_ids(song_id)

    print(df.loc[nn_200_indices.tolist()[0]].head())

if __name__ == "__main__":
    main()