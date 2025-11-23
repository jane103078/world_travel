# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week7 Web Progress Check)
# Date: (11/6/2025)
# Description:Defines ContinentLists class to group cities
#             by continent, including thumbnail and description.
# ***************************************************************

class ContinentLists:
    """ ContinentLists represents a collection of cities grouped by continent."""
    ALL_CONTINENTS = "All Continents"

    __map = {}

    def __init__(self, name, cities=None, thumbnail="", description="", save=False):
        """Initialize a ContinentLists object."""
        self.__name = name
        self.__cities = cities if cities is not None else []
        self.__thumbnail = thumbnail
        self.__description = description
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, continentlist_dict):
        from logic.TouristCity import TouristCity
        return ContinentLists(
            continentlist_dict["name"],
            [TouristCity.lookup(key) for key in continentlist_dict["cities"]],
            continentlist_dict["thumbnail"],
            continentlist_dict["description"],
        )

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "name": self.__name,
            "thumbnail": self.__thumbnail,
            "description": self.__description,
            "cities": [city.get_key() for city in self.__cities],

        }

    def get_key(self):
        """Return a lowercase key for the continent list."""
        return self.__name.lower()

    def get_printable_key(self):
        return self.__name

    def get_name(self):
        """Return the name of the continent list."""
        return self.__name

    def get_description(self):
        """Return the description of the continent list."""
        return self.__description

    def __str__(self):
        s = f"""ContinentLists : {self.__name}
Thumbnail: {self.__thumbnail}, 
Description: {self.__description}
Cities:
"""
        for city in self.__cities:
            s += "      " + str(city) + "\n"
        return s

    def get_thumbnail(self):
        """Return the thumbnail of the continent list."""
        return self.__thumbnail

    @staticmethod
    def get_continent_lists():
        """Retrieve predefined continent lists from the Database"""
        from database.Database import Database
        return Database.get_continent_lists()

    @classmethod
    def lookup(cls, key):
        """Look up a continent list by name."""
        if key.lower() in cls.__map:
            return cls.__map[key.lower()]
        else:
            return None

    def append(self, city, save=True):
        """Add a city to the list of continents."""

        from database.Database import Database

        self.__cities.append(city)

        if save:
            # Database.save_city(city)
            Database.save_continent_list(self)

    def remove(self, city):
        """Remove a city from the list of continents."""
        from database.Database import Database

        if city in self.__cities:
            self.__cities.remove(city)

        Database.save_city(city)
        Database.save_continent_list(self)

    def delete(self):
        """Delete a city from the list of continents."""
        from database.Database import Database
        del type(self).__map[self.get_key()]
        Database.delete_continent_list(self)

    def __iter__(self):
        """Return an iterator over the cities in the list."""
        return self.__cities.__iter__()

    def __contains__(self, city):
        """Return True if city is in the list of continents."""
        return city in self.__cities

    def __add__(self, other):
        """Combine two ContinentLists into a new one."""
        name = f"{self.get_name()}/{other.get_name()}"
        thumbnail = self.get_thumbnail()
        description = self.get_description() + " "+other.get_description()
        new_continentlist = ContinentLists(name, [], thumbnail, description)

        for city in self.__cities:
            if city not in new_continentlist:
                new_continentlist.append(city, save=False)

        for city in other:
            if city not in new_continentlist:
                new_continentlist.append(city, save=False)
        new_continentlist.save()
        return new_continentlist

    @staticmethod
    def rebuild_data():
        from database.Database import Database

        return Database.rebuild_data()

    @staticmethod
    def read_data():
        from database.Database import Database
        return Database.read_data()

    def save(self):
        from database.Database import Database

        Database.save_continent_list(self)
