from istorage import IStorage
import csv


class StorageCsv(IStorage):
    """Class created to perform operations with movies storage in CSV format"""
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """The function loads the information from the CSV file and returns the data as a list"""
        movies_list = []
        with open(self.file_path, "r") as file_object:  # takes movies data from CSV file
            reader = csv.reader(file_object)
            for row in reader:  # puts all data into desired format
                movie = {"movie_name": row[0], "rating": row[1], "year": row[2], "poster": row[3]}
                movies_list.append(movie)
        only_movies_list = movies_list[1:]  # cuts first record with headers of columns
        return only_movies_list

    def add_movie(self, title, year, rating, poster):
        """Takes new movie data as a parameters then makes new movie record,
        adds to movie list and write updated movie list back to storage file"""
        movies_list = []
        with open(self.file_path, "r") as file_object:  # takes movies data from CSV file
            reader = csv.reader(file_object)
            for row in reader:  # puts all data into desired format
                movie = {"movie_name": row[0], "rating": row[1], "year": row[2], "poster": row[3]}
                movies_list.append(movie)
        new_movie = {"movie_name": title, "rating": rating, "year": year, "poster": poster}
        movies_list.append(new_movie)
        # records updated movies list to CSV file
        fieldnames = ["movie_name", "rating", "year", "poster"]
        with open(self.file_path, 'w', newline='') as movie_file:
            writer = csv.DictWriter(movie_file, fieldnames=fieldnames)
            writer.writerows(movies_list)
        print(f"Movie {title} successfully added")

    def delete_movie(self, title):
        """Deletes a movie from movies storage by provided title.
        Loads the information from the CSV file, deletes the movie, and saves it."""
        movies_list = []
        with open("movie_test.csv", "r") as file_object:  # takes movies data from CSV file
            reader = csv.reader(file_object)
            for row in reader:  # puts all data into desired format
                movie = {"movie_name": row[0], "rating": row[1], "year": row[2], "poster": row[3]}
                movies_list.append(movie)
        for film in movies_list:  # seeks movie in the list and deletes
            if title == film['movie_name']:
                movies_list.remove(film)
        # records updated movies list to CSV file
        fieldnames = ["movie_name", "rating", "year", "poster"]
        with open('movie_test.csv', 'w', newline='') as movie_file:
            writer = csv.DictWriter(movie_file, fieldnames=fieldnames)
            writer.writerows(movies_list)

    def update_movie(self, title, notes):
        """
            Updates a movie from movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it.(temporary unused)
            """
        movies_list = []
        with open("movie_test.csv", "r") as file_object:  # takes movies data from CSV file
            reader = csv.reader(file_object)
            for row in reader:
                movie = {"movie_name": row[0], "rating": row[1], "year": row[2], "poster": row[3]}
                movies_list.append(movie)
        for movie in movies_list:
            if title in movie.values():
                movie['categories']['rating'] = notes
        fieldnames = ["movie_name", "rating", "year", "poster"]
        with open('movie_test.csv', 'w', newline='') as movie_file:
            writer = csv.DictWriter(movie_file, fieldnames=fieldnames)
            writer.writerows(movies_list)