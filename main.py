from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    """Creates storage object and movie app object and call the run function to start program execution"""
    storage = StorageJson('movies_data.json')
    movie_app = MovieApp(storage)
    movie_app.run()
    # storage = StorageCsv('movie_test.csv')
    # movie_app = MovieApp(storage)
    # movie_app.run()


if __name__ == "__main__":
    main()