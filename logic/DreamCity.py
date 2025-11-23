# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week7 Web Progress Check)
# Date: (11/6/2025)
# Description:  Defines the DreamCity class, a subclass of
#               TouristCity, which adds the best season and language
#               information for the city.
# ***************************************************************

from logic.TouristCity import TouristCity


class DreamCity(TouristCity):
    """DreamCity extends TouristCity with additional information:
    - Best season to visit
    - Main language spoken"""
    __best_season = ""
    __language = ""
    _TouristCity__city = ""
    _TouristCity__country = ""
    _TouristCity__attraction = ""
    __map = {}

    def __init__(self, city, country, attraction, best_season, language, save=False):
        """ Initialize a DreamCity object."""
        self.__best_season = best_season
        self.__language = language
        super().__init__(city, country, attraction, save=save)
        self.__class__.__map[self.get_key()] = self

    def to_dict(self):
        dreamcity_dict = super().to_dict()
        dreamcity_dict["type"] = "DreamCity"
        dreamcity_dict['best_season'] = self.__best_season
        dreamcity_dict['language'] = self.__language
        return dreamcity_dict

    @classmethod
    def lookup(cls, key):
        """ Look up a city by its unique key."""
        return cls.__map.get(key.lower())

    def get_key(self):
        """ Return unique key for city info"""
        return (f"{self._TouristCity__city}-{self._TouristCity__country}-"
                f"{self._TouristCity__attraction}-{self.__best_season}-{self.__language}").lower()

    def get_printable_key(self):
        return (f"{self._TouristCity__city}-{self._TouristCity__country}-"
                f"{self._TouristCity__attraction}-{self.__best_season}-{self.__language}")

    @staticmethod
    def make_dream_key(city, country, attraction, best_season, language):
        """Generate a unique key for DreamCity without creating an object."""
        return f"{city}-{country}-{attraction}-{best_season}-{language}"

    def __str__(self):
        s = super().__str__()
        return s + f"in the {self.__best_season} in {self.__language}"

    def to_html(self):
        html = super().to_html()
        return html + f" A best season to visit is {self.__best_season} and they speak {self.__language}."

    def get_best_season(self):
        """Return the best season to visit this city."""
        return self.__best_season

    def get_language(self):
        """Return the main language spoken in this city."""
        return self.__language
