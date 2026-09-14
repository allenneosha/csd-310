""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

import dotenv  # to use .env file
from dotenv import dotenv_values  # using our .env file

secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    # output the connection status
    print(
        f"\n  Database user {config['user']} connected to MySQL on host {config['host']} with database {config['database']}\n")

    # Create a cursor object to execute queries
    cursor = db.cursor()

    # Select all fields for the studio table
    print("-" * 50)
    print("-- Displaying All Studios: --")
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    for studio in studios:
        print(studio)

    # Select all fields for the genre table
    print("\n" + "-" * 50)
    print("-- Displaying All Genres: --")
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    for genre in genres:
        print(genre)


    # Select movie names with runtime less than 2 hours (120 minutes)
    print("\n" + "-" * 50)
    print("-- Displaying Movies Under Two Hours: --")
    # Assuming runtime column is named 'runtime' or 'duration' in minutes
    cursor.execute("SELECT title FROM movie WHERE runtime < 120;")
    short_movies = cursor.fetchall()
    for movie in short_movies:
        print(movie)  # Print just the name string from the tuple

    # Get film names and directors grouped by director
    print("\n" + "-" * 50)
    print("-- Displaying Director RECORDS in Order: --")
    cursor.execute("SELECT director, title FROM movies WHERE director IS NOT NULL;")
    films = cursor.fetchall()

    # Grouping using a dictionary for a clean display
    grouped_by_director = {}
    for director, title in films:
        if director not in grouped_by_director:
            grouped_by_director[director] = []
        grouped_by_director[director].append(title)

    for director, movie_titles in grouped_by_director.items():
        print(f"Director: {director}")
        for title in movie_titles:
            print(f"  - {title}")

    print("-" * 50)
    input("\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    """ close cursor and connection to MySQL """
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()
        print("\n  MySQL connection safely closed.")