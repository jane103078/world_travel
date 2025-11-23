# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week7 Web Progress Check)
# Date: (11/6/2025)
# Description:  Defines the TouristCity class with city name,
#               country, and main attraction.
# ***************************************************************

class TouristCity:
    """Tourist city with its name, country, and main attraction."""
    __map = {}

    def __init__(self, city, country, attraction, save=False):
        """Initialize a city and store it in the class map."""
        self.__city = city
        self.__country = country
        self.__attraction = attraction
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, city_dict):
        from logic.DreamCity import DreamCity
        if city_dict["type"] == "TouristCity":
            return TouristCity(
                city_dict["city"],
                city_dict["country"],
                city_dict["attraction"],
            )
        elif city_dict["type"] == "DreamCity":
            return DreamCity(
                city_dict["city"],
                city_dict["country"],
                city_dict["attraction"],
                city_dict["best_season"],
                city_dict["language"],
            )

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "type": "TouristCity",
            "city": self.__city,
            "country": self.__country,
            "attraction": self.__attraction,
        }

    def get_key(self):
        """Return a unique key for the city."""
        return f"{self.__city}-{self.__country}".lower()

    def get_printable_key(self):
        return f"{self.__city}-{self.__country}"

    @staticmethod
    def make_key(city, country):
        """Generate a unique key from city and country."""
        return f"{city.strip().lower()}-{country.strip().lower()}"

    def get_city(self):
        """Return the city name."""
        return self.__city

    def get_country(self):
        """Return the country name."""
        return self.__country

    def get_attraction(self):
        """Return the city's main attraction."""
        return self.__attraction

    def update_attraction(self, attraction):
        """Update the main attraction of the city."""
        self.__attraction = attraction
        self.save()

    @classmethod
    def lookup(cls, key):
        """ Look up a city by its unique key."""
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def __str__(self):
        """Return a readable description of the city."""
        return f"{self.__city} in {self.__country} has {self.__attraction}. "

    def to_html(self):
        return f"{self.__city}, {self.__country} has {self.__attraction}."

    @staticmethod
    def get_cities():
        """Retrieve a list of city objects from the database."""
        from database.Database import Database
        return Database.get_continent_lists()

    @staticmethod
    def rebuild_data():
        from database.Database import Database

        return Database.rebuild_data()

    def save(self):
        from database.Database import Database
        from logic.ContinentLists import ContinentLists

        Database.save_city(self)

        all_continents_list = ContinentLists.lookup(ContinentLists.ALL_CONTINENTS)
        if all_continents_list and self not in all_continents_list:
            all_continents_list.append(self)
