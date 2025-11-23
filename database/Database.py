# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week7 Web Progress Check)
# Date: (11/6/2025)
# Description: Provides a Database class to create and retrieve
#              TouristCity and DreamCity objects.
# ***************************************************************
import os

from logic.TouristCity import TouristCity
from logic.DreamCity import DreamCity
from logic.ContinentLists import ContinentLists
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configparser import ConfigParser


class Database:
    __connection = None
    __database = None
    __cities_collection = None
    __ContinentLists_collection = None
    APP_NAME = "travel_world"


    @classmethod
    def connect(cls):
        if cls.__connection is None:
            if "APPDATA" in os.environ:
                path = f"{os.environ["APPDATA"]}\\{cls.APP_NAME}\\{cls.APP_NAME}.ini"
            elif "HOME" in os.environ:
                path = f"{os.environ["HOME"]}/{cls.APP_NAME}/{cls.APP_NAME}.ini"
            else:
                raise Exception("Couldn't find config directory.")

            config_parser = ConfigParser()
            config_parser.read(path)
            username = config_parser["Database"]["username"]
            password = config_parser["Database"]["password"]
            cluster = config_parser["Database"]["cluster"]

            uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.WorldCity
            cls.__cities_collection = cls.__database.Cities
            cls.__ContinentLists_collection = cls.__database.ContinentLists

            # print("Client:", cls.__connection)
            # print("Database:", cls.__database)
            # print("Cities:", cls.__cities_collection)
            # print("ContinentLists:", cls.__ContinentLists_collection)

    @classmethod
    def rebuild_data(cls):
        cls.connect()

        # Remake both collections
        cls.__cities_collection.drop()
        cls.__cities_collection = cls.__database.Cities
        cls.__ContinentLists_collection.drop()
        cls.__ContinentLists_collection = cls.__database.ContinentLists

        all_cities, all_continentlists = cls.get_continent_lists()

        city_dicts = [city.to_dict() for city in all_cities]
        cls.__cities_collection.insert_many(city_dicts)

        continentlists = [continentlist.to_dict() for continentlist in all_continentlists]
        cls.__ContinentLists_collection.insert_many(continentlists)

    @classmethod
    def read_data(cls):
        cls.connect()
        city_dicts = list(cls.__cities_collection.find())
        cities = [TouristCity.build(city_dict) for city_dict in city_dicts]

        continentlist_dicts = list(cls.__ContinentLists_collection.find())
        continentlists = [ContinentLists.build(continentlist_dict) for continentlist_dict in continentlist_dicts]

        return cities, continentlists

        # return ContinentLists.lookup(ContinentLists.ALL_CONTINENTS), continentlists

    @classmethod
    def get_continent_lists(cls):
        """  Create TouristCity and DreamCity objects"""
        paris = TouristCity("Paris", "France", "Eiffel Tower")
        kyoto = TouristCity("Tokyo", "Japan", "Tokyo Tower")
        new_york = TouristCity("New York", "USA", "Statue of Liberty")

        taipei = DreamCity("Taipei", "Taiwan", "Taipei 101", "Autumn", "Mandarin")
        bangkok = DreamCity("Bangkok", "Thailand", "Grand Palace", "Winter", "Thai")

        """Create continent Lists"""
        asia_cities = ContinentLists(
            "Asia",
            [kyoto, taipei, bangkok],
            "https://www.worldatlas.com/img/areamap/continent/asia_map.gif",
            "A continent full of delicious cuisines and vibrant cultures."
        )
        europe_cities = ContinentLists(
            "Europe",
            [paris],
            "https://www.worldatlas.com/img/areamap/continent/europe_map.gif",
            "A continent rich in history, art, and culture, known for its diverse architecture."
        )

        north_america_cities = ContinentLists(
            "North America",
            [new_york],
            "https://www.worldatlas.com/img/areamap/continent/north_america_map.gif",
            "A diverse land of cities and natural wonders."
        )

        all_continents = ContinentLists(ContinentLists.ALL_CONTINENTS, [paris, kyoto, new_york, taipei, bangkok],
                                        "https://www.worldatlas.com/r/w960-h540-q80/img/ncore/continent_model_7.jpg",
                                        "explore beauty and diversity around the world.")

        return all_continents, [asia_cities, europe_cities, north_america_cities, all_continents]

    @classmethod
    def save_continent_list(cls, continentlist):
        cls.connect()
        cls.__ContinentLists_collection.update_one({"_id": continentlist.get_key()}, {"$set": continentlist.to_dict()},
                                                   upsert=True)

    @classmethod
    def save_city(cls, city):
        cls.connect()
        cls.__cities_collection.update_one({"_id": city.get_key()}, {"$set": city.to_dict()}, upsert=True)

    @classmethod
    def delete_continent_list(cls, continentlist):
        cls.connect()
        cls.__ContinentLists_collection.delete_one({"_id": continentlist.get_key()})


if __name__ == "__main__":
    Database.connect()

    # """
    # Display all city keys and details
    # """
    # cities = Database.get_continent_lists()
    # for city in cities:
    #     print(city.get_key(), ":", city, sep="")
