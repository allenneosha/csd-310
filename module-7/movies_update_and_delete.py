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

# --- DEFINE FUNCTIONS ---

def show_films(cursor, title):
    query = """
        SELECT 
            film.film_name AS Name, 
            film.film_director AS Director, 
            genre.genre_name AS Genre, 
            studio.studio_name AS Studio
        FROM film 
        INNER JOIN genre ON film.genre_id = genre.genre_id 
        INNER JOIN studio ON film.studio_id = studio.studio_id
        """
    cursor.execute(query)
    films = cursor.fetchall()

    print(f"\n  -- {title}  --\n")

    for film in films:
        print(f"Film Name:   {film[0]}")
        print(f"Director:    {film[1]}")
        print(f"Genre Name:  {film[2]}")
        print(f"Studio Name: {film[3]}\n")


def update_film_director(db, cursor, film_name, new_director):
    """Updates the director of a specific film."""

    query = "UPDATE film SET film_director = %s WHERE film_name = %s"
    cursor.execute(query, (new_director, film_name))
    db.commit()  # Saves change to the database


def delete_film(db, cursor, film_name):
    """Deletes a specific film from the table."""
    query = "DELETE FROM film WHERE film_name = %s"
    cursor.execute(query, (film_name,))
    db.commit()  # Saves change to the database


# --- MAIN EXECUTION BLOCK ---
try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database
    cursor = db.cursor()  # Create the cursor object

    # Output the connection status
    print(
        f"\n  Database user {config['user']} connected to MySQL on host {config['host']} with database {config['database']}\n")

    # 1. Display original data
    show_films(cursor, "DISPLAYING ORIGINAL FILMS")

    target_movie = "Inception"
    print(f"--- Updating director for '{target_movie}' ---")
    update_film_director(db, cursor, target_movie, "Christopher Nolan")

    # 3. Display data again to show the update took effect
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # 4. Delete a film record
    print(f"--- Deleting '{target_movie}' from database ---")
    delete_film(db, cursor, target_movie)

    # 5. Display data one final time to prove it was deleted
    show_films(cursor, "DISPLAYING FILMS AFTER DELETION")

    # Clean up connections
    cursor.close()
    db.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
