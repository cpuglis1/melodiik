from fuzzywuzzy import fuzz, process

class RetrieveSongs:
    def __init__(self, data_df, x_data, knn_200_model, knn_query_model, knn_vectorizer):
        self.data_df = data_df
        self.knn_200_model = knn_200_model
        self.knn_query_model = knn_query_model
        self.knn_vectorizer = knn_vectorizer
        self.x_data = x_data

    def search_song(self, query):
        query_vector = self.knn_vectorizer.transform([query])
        distance, index = self.knn_query_model.kneighbors(query_vector)
        return self.data_df.iloc[index[0]]

    def get_nearest_neighbors_ids(self, song_id):
        query_point = self.x_data.iloc[song_id].values.reshape(1, -1)
        distances, indices = self.knn_200_model.kneighbors(query_point)
        return indices