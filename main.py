
from bs4 import BeautifulSoup
from statistics import mean, pvariance, median
import math
import psycopg2
from decouple import config


data = []

file_name = "python_class_question.html"

with open(file_name) as html_file:
    soup = BeautifulSoup(html_file, 'lxml')


table_rows = soup.find_all("tr")

for row in table_rows:
    day_data = {}
    day = row.find_all("td")[0]
    row_colours = row.find_all("td")[1]
    day_data[day.text] = row_colours.text.split(", ")

    data.append(day_data)


def set_colors(data:list) -> None:
    """
     . Takes in a list of formatted data .Ex [
         {
             "day" : [...colours]
         },
     ]
     iterates over this data extracts the colors for each day then returns a set of unique colors and all colors
    """
    colors = []
    for day in data:
        colors += list(day.values())[0]

    return list(set(colors)), colors


def get_frequency(unique_colors, universal_colors):
    data = {}

    for unique in unique_colors:
        frequency = 0

        for universal in universal_colors:
            if unique == universal:
                frequency += 1

        data[unique] = frequency

    return data


def get_number_of_workers(data):

    workers_per_day = map(lambda day: len(day.values()), data)
    print(workers_per_day)


# POSTGRESQL DATABASE INTEGRATION

def save_frequencies(colors_frequency):

    connection = psycopg2.connect(
        config("DATABASE_URL"),
        sslmode="require"
    )

    try:
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS colors (
                        id SERIAL PRIMARY KEY,
                        color VARCHAR(50) UNIQUE NOT NULL,
                        frequency INTEGER NOT NULL
                    )
                """)

                for color, frequency in colors_frequency.items():

                    cursor.execute("""
                        INSERT INTO colors (color, frequency)
                        VALUES (%s, %s)
                        ON CONFLICT (color)
                        DO UPDATE SET
                            frequency = EXCLUDED.frequency
                    """, (color, frequency))

        print("Colors saved successfully to PostgreSQL!")

    finally:
        connection.close()


if __name__ == '__main__':
    unique_colors, all_colours = set_colors(data)
    colors_frequency = get_frequency(
        unique_colors,
        universal_colors=all_colours
    )

    # Save colors and frequencies to PostgreSQL
    save_frequencies(colors_frequency)

    # Which color is mostly worn throughout the week?
    mode_color = max(colors_frequency, key=colors_frequency.get)

    red_probability = colors_frequency['RED'] / len(all_colours)

    average = mean(colors_frequency.values())

    smallest_difference = min(
        abs(count - average)
        for count in colors_frequency.values()
    )

    closest_colors = [
        color for color, count in colors_frequency.items()
        if abs(count - average) == smallest_difference
    ]

    variance = pvariance(colors_frequency.values())

    median_frequency = median(colors_frequency.values())

    rounded_mean = math.floor(median_frequency + 0.5)

    for color, count in colors_frequency.items():
        if count == rounded_mean:
            print(color)

    # Variance
    print(round(variance, 2))

    # Mean color
    print(closest_colors)

    # Probability of selecting red at random
    print(red_probability)

    # Mostly worn throughout the week
    print(mode_color)
