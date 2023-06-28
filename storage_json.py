from istorage import IStorage
import json


class StorageJson(IStorage):
    """Class created to perform operations with movies storage in JSON format"""
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """The function loads the information from the JSON file and returns the data as a list"""
        with open(self.file_path, "r") as fileobject:
            movies_list = json.loads(fileobject.read())
            return movies_list

    def add_movie(self, title, year, rating, poster):
        """Takes new movie data as a parameters then makes new movie record,
        adds to movie list and write updated movie list back to storage file"""
        with open(self.file_path, "r") as file_object:  # takes movies data from JSON file
            movies_list = json.loads(file_object.read())
        new_movie = {"movie_name": title, "rating": rating, "year": year, "poster": poster}
        movies_list.append(new_movie)
        # records updated movies list to JSON file
        json_str = json.dumps(movies_list)
        with open(self.file_path, "w") as new_file_object:
            new_file_object.write(json_str)
        print(f"Movie {title} successfully added")

    def delete_movie(self, title):
        """Deletes a movie from movies storage by provided title.
        Loads the information from the JSON file, deletes the movie, and saves it."""
        with open(self.file_path, "r") as file_object:  # takes movies data from JSON file
            movies_list = json.loads(file_object.read())
        for movie in movies_list:  # seeks movie in the list and deletes
            if title == movie['movie_name']:
                movies_list.remove(movie)
        # records updated movies list to JSON file
        json_str = json.dumps(movies_list)
        with open(self.file_path, "w") as new_file_object:
            new_file_object.write(json_str)

    def update_movie(self, title, notes):
        """
            Updates a movie from movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it.(temporary unused)
            """
        with open(self.file_path, "r") as file_object:
            movies_list = json.loads(file_object.read())
        for movie in movies_list:
            if title in movie.values():
                movie['rating'] = notes
        json_str = json.dumps(movies_list)
        with open(self.file_path, "w") as new_file_object:
            new_file_object.write(json_str)
