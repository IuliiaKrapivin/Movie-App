from random import choice
import requests

import storage_csv
import storage_json


KEY = '34571e1b'


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_greeting(self):
        """Prints greeting at first enter"""
        print("********** My Movies Database **********")

    def _command_menu(self):
        """Prints the menu at first time and after every operation occurring, returns number of menu that user chose """
        print("\nMenu:\n"
              "0. Exit\n"
              "1. List movies\n"
              "2. Add movie\n"
              "3. Delete movie\n"
              "4. Update movie\n"
              "5. Stats\n"
              "6. Random movie\n"
              "7. Search movie\n"
              "8. Movies sorted by rating\n"
              "9. Generate website\n")

        the_choice = input("Enter choice (0-9): ")
        return the_choice

    def _command_list_movies(self):
        """Prints all the movies with ratings and years, total amount of movies in the instance list"""
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total")
        for movie in movies:
            print(f"{movie['movie_name']} ({movie['year']}): {movie['rating']}")

    def _command_add_movie(self):
        """Makes a request to API with provided movie name to get a movie data,
        filters the response to take only needed data, provides new movie data to storage class method"""
        try:
            movies = self._storage.list_movies()  # loads all movies list from storage
            new_movie_name = input("Enter a movie: ")  # takes a movie name from user
            for movie in movies:  # checks if movie already in list
                if new_movie_name in movie.values():
                    print(f"{new_movie_name} already exist!")
                    return
            url = f'https://www.omdbapi.com/?apikey={KEY}&t={new_movie_name}'  # makes request to API
            response = requests.get(url)
            data = response.json()  # saves the response
            # filters the response
            title = data['Title']
            year = data['Year']
            rating = float(data['Ratings'][0]['Value'][:-3])
            poster = data['Poster']
            # depending on storage type calls the add command of storage class
            if type(self._storage) == storage_json.StorageJson:
                storage_json.StorageJson.add_movie(self._storage, title, year, rating, poster)
            elif type(self._storage) == storage_csv.StorageCsv:
                storage_csv.StorageCsv.add_movie(self._storage, title, year, rating, poster)
        except KeyError:
            print("Movie is not found ")  # prints an error message if movie wasn't found
        except requests.exceptions.ConnectionError:
            print("Connection issue")  # prints an error message if connection problem is appeared

    def _command_delete_movie(self):
        """Makes a request to instance movies storage to find and delete the movie that user entered"""
        movies = self._storage.list_movies()  # loads all movies list from storage
        del_movie = input("Enter a movie: ")  # takes a movie name from user
        for movie in movies:  # checks if movie is in the list
            if del_movie in movie.values():
                # depending on storage type calls the delete command of storage class
                if type(self._storage) == storage_json.StorageJson:
                    storage_json.StorageJson.delete_movie(self._storage, del_movie)
                elif type(self._storage) == storage_csv.StorageCsv:
                    storage_csv.StorageCsv.delete_movie(self._storage, del_movie)
                print(f"Movie {del_movie} successfully deleted")
                return
        print(f"Error! {del_movie} not in the list")  # prints an error message if movie is not in the list

    def _command_update_movie(self):
        """Changes rating in chosen movie(temporary unused)"""
        movies = self._storage.list_movies()  # loads all movies list from storage
        movie_name = input("Enter a movie: ")
        for movie in movies:
            if movie_name in movie.values():
                movie_rating = float(input("Enter new movie rating: "))
                # depending on storage type calls the update command of storage class
                if type(self._storage) == storage_json.StorageJson:
                    storage_json.StorageJson.update_movie(self._storage, movie_name, movie_rating)
                elif type(self._storage) == storage_csv.StorageCsv:
                    storage_csv.StorageCsv.update_movie(self._storage, movie_name, movie_rating)
                print(f"Movie {movie_name} successfully updated")
                return
        print(f"Error! {movie_name} is not in the list")

    def _command_movie_stats(self):
        """Operates with movies ratings from the list, prints the average and median rating,
        the best and worst movie """
        movies = self._storage.list_movies()  # loads all movies list from storage
        rating_list = []
        for movie in movies:  # composes movies rating list
            rating = float(movie['rating'])
            rating_list.append(rating)
        rating_list.sort()

        summ = 0  # counts average rating
        for rating in rating_list:
            summ += rating
        average_rat = summ / len(rating_list)
        print(f"Average rating: {(round(average_rat, 1))}")

        if len(rating_list) % 2 == 0:  # counts median rating
            a = int((len(rating_list) / 2) - 1)
            b = int(len(rating_list) / 2)
            median_rating = (rating_list[a] + rating_list[b]) / 2
        else:
            a = int(len(rating_list) // 2)
            median_rating = rating_list[a]
        print(f"Median rating: {(round(median_rating, 1))}")

        max_val = rating_list[-1]  # seeks the best movie
        for movie in movies:
            if float(movie['rating']) == max_val:
                print(f"The best movie is {movie['movie_name']}: {movie['rating']}")

        min_val = rating_list[0]  # seeks the worst movie
        for movie in movies:
            if float(movie['rating']) == min_val:
                print(f"The worst movie is {movie['movie_name']}: {movie['rating']}")

    def _command_random_movie(self):
        """Chooses a random movie from the list"""
        movies = self._storage.list_movies()  # loads all movies list from storage
        movies_list = []  # composes list of movies names
        for movie in movies:
            movie_name = movie['movie_name']
            movies_list.append(movie_name)
        a_random_movie = str(choice(movies_list))  # choosing a random movie from the list
        print(f"Your movie: {a_random_movie}")

    def _command_search_movie(self):
        """Searching for entered movie name(or a piece of name) in the list"""
        movies = self._storage.list_movies()  # loads all movies list from storage
        search = input("Search a movie: ")
        search = search.lower()  # makes entered name in a lowercase to compare
        for movie in movies:
            if search in movie['movie_name'].lower():  # checks all movies names in lowercase
                print(f"{movie['movie_name']} ({movie['year']}): {movie['rating']}")

    def _command_rating_sorted_movies(self):
        """Prints all movies sorted by rating in descending order"""
        movies = self._storage.list_movies()   # loads all movies list from storage
        rating_list = []
        for movie in movies:  # composes ratings list
            rating = movie['rating']
            rating_list.append(rating)
        # deletes double ratings, sorting and reversing ratings list
        rating_list = list(set(rating_list))
        rating_list.sort()
        rating_list.reverse()
        for i in rating_list:  # picks up movies from movies list by ratings to print
            for movie in movies:
                if i == movie['rating']:
                    print(movie['movie_name'], movie['rating'])

    def _generate_website(self):
        """Takes the movies list from the instance movie storage and creates a website"""
        movies = self._storage.list_movies()  # loads all movies list from storage
        output = ''
        for movie in movies:  # composes movies grid to put into HTML template
            title = movie['movie_name']
            poster = movie['poster']
            year = movie['year']
            output += '<li>\n'
            output += '<div class="movie">\n'
            output += f'<img class="movie-poster" src="{poster}"/>\n'
            output += f'<div class="movie-title">{title}</div>\n'
            output += f'<div class="movie-year">{year}</div>\n'
            output += '</div>\n'
            output += '</li>\n'
        # takes HTML template from the file
        with open("index_template.html", "r") as file_object:
            html_string = file_object.read()
        #  replaces placeholders to movies data
        movie_html_string = html_string.replace("__TEMPLATE_TITLE__", "My movie App")
        movie_html_string = movie_html_string.replace("__TEMPLATE_MOVIE_GRID__", output)
        # creates an HTML final file
        with open("index.html", "w") as new_file:
            new_file.write(movie_html_string)
        print("Website was generated successfully.")

    def run(self):
        """Calls menu function, takes user number to call matched function. Works until user exit the program"""
        self._command_greeting()
        while True:
            number = int(self._command_menu())
            if number == 0:
                print("Bye!")
                exit()
            elif number == 1:
                self._command_list_movies()
            elif number == 2:
                self._command_add_movie()
            elif number == 3:
                self._command_delete_movie()
            elif number == 4:
                self._command_update_movie()
            elif number == 5:
                self._command_movie_stats()
            elif number == 6:
                self._command_random_movie()
            elif number == 7:
                self._command_search_movie()
            elif number == 8:
                self._command_rating_sorted_movies()
            elif number == 9:
                self._generate_website()
            print("\n")
            next_step = input("Press Enter to continue ")
            if next_step == " ":
                continue


