import pickle
from datetime import datetime

class ResultPickleHandler:
    def __init__(self):
        pass

    def _get_filename(self, base_name):
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{date_time}.pkl"

    def dump_result(self, data, base_name):
        filename = self._get_filename(base_name)
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
        print(f"Data dumped to {filename}")

    def load_result(self, base_name):
        filename = self._get_filename(base_name)
        with open(filename, 'rb') as file:
            data_loaded = pickle.load(file)
        return data_loaded

'''
# Example usage:
handler = ResultPickleHandler()

# Dumping the results
handler.dump_result(discography_result, "discography_result")
handler.dump_result(artist_stats_result, "artist_stats_result")

# Loading the results
loaded_discography = handler.load_result("discography_result")
loaded_artist_stats = handler.load_result("artist_stats_result")
'''