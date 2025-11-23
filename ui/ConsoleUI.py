# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week7 Web Progress Check)
# Date: (11/6/2025)
# Description: Provides a console-based user interface
# ***************************************************************

from ui.input_validation import select_item, input_string, y_or_n
from logic.ContinentLists import ContinentLists
from logic.TouristCity import TouristCity
from logic.DreamCity import DreamCity


class ConsoleUI:
    """
        Console-based interface to list cities or exit the program.

        Features:
            - List all cities or continent lists
            - Create, delete, show, or join continent lists
            - Create, add, remove, or update cities

    """
    __all_cities = None
    __all_continents_lists = []

    CHOICES = ["pc", "pco", "cl", "dl", "sl", "cc", "ac", "rc", "uc", "jl", "x"]

    @classmethod
    def init(cls):
        """Initialize all cities from the database"""
        cls.__all_cities, cls.__all_continents_lists = ContinentLists.read_data()

    @classmethod
    def select_continent_list(cls, include_all_cities=False):
        """Prompt user to select a continent list."""
        names = []
        mapping = {}
        pos = 1
        for continent_list in cls.__all_continents_lists:
            if include_all_cities or continent_list.get_name() != ContinentLists.ALL_CONTINENTS:
                names.append(continent_list.get_name())
                mapping[str(pos)] = continent_list.get_name()
                pos += 1

        names.append("None")
        mapping[str(pos)] = "None"

        print("Please select a continent to show:")
        pos = 1
        for name in names:
            print(F"    {pos}: {name}")
            pos += 1

        name = select_item(
            "Enter the continent name to show or 'None' to exit: ",
            choices=names,
            mapping=mapping
        )

        if name.lower() == "none":
            return None

        continent_list = ContinentLists.lookup(name)
        return continent_list

    @classmethod
    def select_city(cls, continent_list=None):
        """Prompt user to select a city from a list."""
        if continent_list is None:
            continent_list = cls.__all_cities
        keys = []
        mapping = {}
        pos = 1
        for city in continent_list:
            keys.append(city.get_key())
            mapping[str(pos)] = city.get_key()
            pos += 1
        keys.append("None")
        mapping[str(pos)] = "None"
        print("Please select a city from the list below: ")
        pos = 1
        for key in keys:
            print(f"    {pos}: {key}")
            pos += 1
        key = select_item("Enter the city or 'None' to exit: ", error="Please type a city!", choices=keys,
                          mapping=mapping)
        if key == "None":
            return None

        city = TouristCity.lookup(key)
        return city

    @classmethod
    def list_cities(cls):
        """Print all cities in the collection"""
        for city in cls.__all_cities:
            print(city.get_key(), ":", city, sep="")

    @classmethod
    def list_continent_lists(cls):
        """Print all continent lists with their descriptions."""
        for continentlist in cls.__all_continents_lists:
            print(f"{continentlist.get_name()}: {continentlist.get_description()}")

    @classmethod
    def create_continent_list(cls):
        """Prompt user to create a new continent list."""
        name = input_string("Please enter the name of the continent list or 'None to exit': ",
                            "name must be non_empty: ")

        if name.strip().lower() == "none":
            return

        continent_list = ContinentLists.lookup(name)
        if continent_list is not None:
            print("Error! Continent list already exists")
            return

        thumbnail = input_string("Please enter the URL for the thumbnail image: ", "name must be non_empty")
        description = input_string("Please enter the description of the continent list: ", valid=lambda s: True)

        continent_list = ContinentLists(name, [], thumbnail, description, save=True)
        cls.__all_continents_lists.append(continent_list)
        print(f"{continent_list.get_name()} is added")

    @classmethod
    def delete_continent_list(cls):
        """delete continent list"""
        continent_list = cls.select_continent_list()
        if continent_list is None:
            return

        cls.__all_continents_lists.remove(continent_list)
        continent_list.delete()
        print(f"{continent_list.get_name()} has been deleted.")

    @classmethod
    def show_continent_list(cls):
        """Display details of a selected continent list."""
        continent_list = cls.select_continent_list(True)
        if continent_list is None:
            return
        print()
        print(f"Name:  {continent_list.get_name()}")
        print(f"Description:  {continent_list.get_description()}")
        print(f"Thumbnail:  {continent_list.get_thumbnail()}")
        print("Continent in the list")
        for continent in continent_list:
            print("    ", continent)

    @classmethod
    def create_city(cls):
        """Prompt user to create a new TouristCity or DreamCity."""

        is_dream_city = y_or_n("Is the new city a DreamCity? (y/n): ")

        # --- basic shared info ---
        city = input_string("Enter city name: ")
        country = input_string("Enter country name: ")
        attraction = input_string("Enter the most famous attraction: ")

        if not is_dream_city:
            key = TouristCity.make_key(city, country)
            city_obj = TouristCity.lookup(key)
            if city_obj is not None:
                print("TouristCity already exists!")
                return
            city_obj = TouristCity(city, country, attraction)

        else:
            # --- Create DreamCity ---
            best_season = input_string("Enter the best season to visit: ")
            language = input_string("Enter the main language spoken: ")

            key = DreamCity.make_dream_key(city, country, attraction, best_season, language)
            city_obj = DreamCity.lookup(key)
            if city_obj is not None:
                print("DreamCity already exists!")
                return

            city_obj = DreamCity(city, country, attraction, best_season, language, save=True)

        city_obj.save()
        cls.__all_cities.append(city_obj)

        all_continents_list = ContinentLists.lookup(ContinentLists.ALL_CONTINENTS)
        if all_continents_list:
            all_continents_list.append(city_obj)

        print(f"{city_obj.get_city()} is created")

    @classmethod
    def add_city(cls):
        """Add a city to a selected continent list."""
        continentlist = cls.select_continent_list()
        if continentlist is None:
            return
        city = cls.select_city()
        if city is None:
            return

        if city in continentlist:
            print("City is already in the list!")
            return
        continentlist.append(city)
        print()
        print("Added city to continent list.")

    @classmethod
    def remove_city(cls):
        """Remove a city from a selected continent list."""
        continent_list = cls.select_continent_list()
        if continent_list is None:
            return
        city = cls.select_city(continent_list)
        if city is None:
            return

        if city not in continent_list:
            print("City is not already in the list!")
            return
        continent_list.remove(city)
        print()
        print("Removed city from continent list.")

    @classmethod
    def update_city(cls):
        """Update the attraction of a selected city."""
        city = cls.select_city()
        if city is None:
            return
        attraction = input_string("Enter the new attraction: ", valid=lambda x: True)
        city.update_attraction(attraction)
        print("Attraction has been updated.")

    @classmethod
    def join_continent_list(cls):
        """Join two continent lists into a new one."""
        continent_list_1 = cls.select_continent_list(include_all_cities=True)
        if continent_list_1 is None:
            return
        continent_list_2 = cls.select_continent_list(include_all_cities=True)
        if continent_list_2 is None:
            return
        new_continent_list = continent_list_1 + continent_list_2
        cls.__all_continents_lists.append(new_continent_list)
        print("Joined continent list.")

    @classmethod
    def run(cls):
        """Main loop for the console UI"""
        while True:
            print()
            cls.print_menu()
            # Ask user for input
            choice = select_item(
                "Please choose an option : ",
                choices=["pc", "pco", "cl", "dl", "sl", "cc", "ac", "rc", "uc", "jl", "x"],
                error="Must select a valid option",
            )
            print()
            choice = choice.lower()
            if choice == "x":
                break
            elif choice == "pc":
                cls.list_cities()
            elif choice == "pco":
                cls.list_continent_lists()
            elif choice == "cl":
                cls.create_continent_list()
            elif choice == "dl":
                cls.delete_continent_list()
            elif choice == "sl":
                cls.show_continent_list()
            elif choice == "cc":
                cls.create_city()
            elif choice == "ac":
                cls.add_city()
            elif choice == "rc":
                cls.remove_city()
            elif choice == "uc":
                cls.update_city()
            elif choice == "jl":
                cls.join_continent_list()
            else:
                print("Invalid option. Please try again.")
        print("Good bye!!!!!!!!!")

    @staticmethod
    def print_menu():
        """Display menu options"""
        print("Please select an option from the list below:")
        print("pc - Print cities")
        print("pco - Print continent lists")
        print("cl - Create continent list")
        print("dl - Delete continent list")
        print("sl - Show continent list")
        print("cc - Create new city")
        print("ac - Add city to continent")
        print("rc - Remove city from continent")
        print("uc - Update city")
        print("jl - Join continent list")
        print("x - Exit program")


if __name__ == "__main__":
    ConsoleUI.init()
    ConsoleUI.run()
