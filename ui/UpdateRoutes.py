# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week8Web )
# Date: (11/13/2025)
# Description: UpdateRoutes
# ***************************************************************
from logic.TouristCity import TouristCity
from ui.WebUI import WebUI
from flask import render_template, request
from logic.ContinentLists import ContinentLists


class UpdateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/update_city_attraction', methods=['GET', 'POST'])
    def update_city_attraction():
        return render_template("update/update_city_attraction.html", cities=WebUI.get_all_cities())

    @staticmethod
    @__app.route('/do_update_city_attraction', methods=['GET', 'POST'])
    def do_update_city_attraction():
        key, error = WebUI.validate_field("The city", "city")
        if key is None:
            return error

        city = TouristCity.lookup(key.lower())
        if city is None:
            return render_template(
                "error.html",
                message_header="City does not exist!!!",
                message_body=f"The city '{key}'dose not exist! Please choose another continent and try again.",
            )
        if "attraction" in request.form:
            attraction = request.form["attraction"].strip()
        else:
            attraction = ""

        city.update_attraction(attraction)
        return render_template("update/confirm_attraction_updated.html", city=city)

    @staticmethod
    @__app.route('/add_city_to_continentlist')
    def add_city_to_continentlist():
        return render_template("update/add_city_to_continentlist.html",
                               cities=WebUI.get_all_cities(),
                               continentlists=WebUI.get_all_continentlists()
                               )

    @staticmethod
    @__app.route('/do_add_city_to_continentlist', methods=['GET', 'POST'])
    def do_add_city_to_continentlist():
        city_key, error = WebUI.validate_field("The city", "city")
        if city_key is None:
            return error

        city = TouristCity.lookup(city_key.lower())
        if city is None:
            return render_template(
                "error.html",
                message_header="City does not exist!!!",
                message_body=f"The city '{city_key}'dose not exist! Please choose another continent and try again.",
            )
        continentlist_key, error = WebUI.validate_field("The continent list name",
                                                        "continentlist")
        if continentlist_key is None:
            return error

        continentlist = ContinentLists.lookup(continentlist_key.lower())
        if continentlist is None:
            return render_template(
                "error.html",
                message_header=f"The continent list {continentlist_key} was not found.!",
                message_body=f"A ContinentList '{continentlist_key}' "
                             f"was not found. Please choose another continent list and try again."
            )
        if city in continentlist:
            return render_template(
                "error.html",
                message_header=f"The City Already in the continent list!",
                message_body=f"The City {city.get_printable_key()} is already "
                             f"in the continent list {continentlist.get_printable_key()} !."
            )
        continentlist.append(city)
        return render_template("update/confirm_city_added_to_continentlist.html",
                               city=city, continentlist=continentlist)

    @staticmethod
    @__app.route('/remove_city_from_continentlist')
    def remove_city_from_continentlist():
        return render_template(
            "update/remove_city_from_continentlist.html",
            cities=WebUI.get_all_cities(),
            continentlists=WebUI.get_all_continentlists()
        )

    @staticmethod
    @__app.route('/do_remove_city_from_continentlist', methods=['GET', 'POST'])
    def do_remove_city_from_continentlist():
        city_key, error = WebUI.validate_field("The city", "city")
        if city_key is None:
            return error

        city = TouristCity.lookup(city_key.lower())
        if city is None:
            return render_template(
                "error.html",
                message_header="City does not exist!!!",
                message_body=f"The city '{city_key}'dose not exist! Please choose another continent and try again.",
            )
        continentlist_key, error = WebUI.validate_field("The continent list name",
                                                        "continentlist")
        if continentlist_key is None:
            return error
        continentlist = ContinentLists.lookup(continentlist_key.lower())

        if continentlist is None:
            return render_template(
                "error.html",
                message_header=f"The continent list {continentlist_key} was not found.!",
                message_body=f"A ContinentList '{continentlist_key}' "
                             f"was not found. Please choose another continent list and try again."
            )
        if continentlist.get_name() == ContinentLists.ALL_CONTINENTS:
            return render_template(
                    "error.html",
                    message_header=f"Can't remove the city!",
                    message_body=f"You can't remove the city from the '{ContinentLists.ALL_CONTINENTS}' !"
                )

        if city not in continentlist:
            return render_template(
                "error.html",
                message_header=f"The City is not in the continent list!",
                message_body=f"The City {city.get_printable_key()} is not "
                             f"in the continent list {continentlist.get_printable_key()} !."
            )
        continentlist.remove(city)
        return render_template("update/confirm_city_removed_from_continentlist.html",
                               city=city, continentlist=continentlist)
