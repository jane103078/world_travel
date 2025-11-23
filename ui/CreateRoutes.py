# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week8Web )
# Date: (11/13/2025)
# Description: CreateRoutes
# ***************************************************************
from ui.WebUI import WebUI
from flask import render_template, request
from logic.ContinentLists import ContinentLists
from logic.TouristCity import TouristCity
from logic.DreamCity import DreamCity


class CreateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_continentlist')
    def create_continentlist():
        return render_template("create/create_continentlist.html")

    @staticmethod
    @__app.route('/do_create_continentlist', methods=['GET', 'POST'])
    def do_create_continentlist():
        name, error = WebUI.validate_field("The continent list name", "name")
        if name is None:
            return error
        key = name.lower()
        continentlist = ContinentLists.lookup(key)
        if continentlist is not None:
            return render_template(
                "error.html",
                message_header="Continentlist already exists!!!",
                message_body=f"A continentlist with name '{name}' "
                             f"already exists. Please choose another continent and try again."
            )
        if "thumbnail" in request.form:
            thumbnail = request.form["thumbnail"].strip()
        else:
            thumbnail = ""
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""
        continent_list = ContinentLists(name, [], thumbnail, description, save=True)
        WebUI.get_all_continentlists().append(continent_list)

        return render_template("create/confirm_continentlist_created.html", continentlist=continent_list)

    @staticmethod
    @__app.route('/create_tourist_city')
    def create_tourist_city():
        return render_template("create/create_tourist_city.html")

    @staticmethod
    @__app.route('/do_create_tourist_city', methods=['GET', 'POST'])
    def do_create_tourist_city():
        # city, country, attraction
        city, error = WebUI.validate_field("The tourist city name", "city")
        if city is None:
            return error
        country, error = WebUI.validate_field("The tourist city's country", "country")
        if country is None:
            return error
        if "attraction" in request.form:
            attraction = request.form["attraction"].strip()
        else:
            attraction = ""
        key = TouristCity.make_key(city, country).lower()
        existing_city = TouristCity.lookup(key)
        if existing_city is not None:
            return render_template(
                "error.html",
                message_header="A tourist city already exists!!!",
                message_body=f"A tourist city '{existing_city.get_city()}' in '{existing_city.get_country()}' "
                             f"already exists. Please choose another city and try again."
            )
        url, error = WebUI.validate_field("The tourist city url", "url")
        if url is None:
            return error

        tourist_city = TouristCity(city, country, attraction, save=True)
        WebUI.get_all_cities().append(tourist_city)

        return render_template("create/confirm_tourist_city_created.html", city=tourist_city)

    @staticmethod
    @__app.route('/create_dream_city')
    def create_dream_city():
        return render_template("create/create_dream_city.html")

    @staticmethod
    @__app.route('/do_create_dream_city', methods=['GET', 'POST'])
    def do_create_dream_city():
        city, error = WebUI.validate_field("The dream city name", "city")
        if city is None:
            return error
        country, error = WebUI.validate_field("The dream city's country", "country")
        if country is None:
            return error
        best_season, error = WebUI.validate_field("The dream city best season to visit",
                                                  "best_season")
        if best_season is None:
            return error
        language, error = WebUI.validate_field("The dream city speak", "language")
        if language is None:
            return error
        if "attraction" in request.form:
            attraction = request.form["attraction"].strip()
        else:
            attraction = ""
        key = DreamCity.make_dream_key(city, country, attraction, best_season, language).lower()
        existing_city = DreamCity.lookup(key)
        if existing_city is not None:
            return render_template(
                "error.html",
                message_header="A dream city already exists!!!",
                message_body=f"A dream city '{existing_city.get_city()}' in '{existing_city.get_country()}' "
                             f"already exists. Please choose another city and try again."
            )

        dream_city = DreamCity(city, country, attraction, best_season, language, save=True)
        WebUI.get_all_cities().append(dream_city)

        return render_template("create/confirm_dream_city_created.html", city=dream_city)

    @staticmethod
    @__app.route("/join_continentlists")
    def join_continentlists():
        return render_template("create/join_continentlists.html", continentlists=WebUI.get_all_continentlists())

    @staticmethod
    @__app.route("/do_join_continentlists", methods=['GET', 'POST'])
    def do_join_continentlists():
        first_key, error = WebUI.validate_field("The first continent list name",
                                                "first_continentlist")
        if first_key is None:
            return error
        second_key, error = WebUI.validate_field("The second continent list name",
                                                 "second_continentlist")
        if second_key is None:
            return error
        first_continentlist = ContinentLists.lookup(first_key.lower())
        if first_continentlist is None:
            return render_template(
                "error.html",
                message_header=f"The continent list {first_key} was not found.!",
                message_body=f"A ContinentList '{first_key}' "
                             f"was not found. Please choose another continent list and try again."
            )
        second_continentlist = ContinentLists.lookup(second_key.lower())
        if second_continentlist is None:
            return render_template(
                "error.html",
                message_header=f"The continent list {second_key} was not found.!",
                message_body=f"A ContinentList '{second_key}' "
                             f"was not found. Please choose another continent list and try again."
            )
        new_key = f"{first_continentlist.get_name()}/{second_continentlist.get_name()}"
        new_continentlist = ContinentLists.lookup(new_key.lower())
        if new_continentlist is not None:
            return render_template(
                "error.html",
                message_header=f"The continent list {new_key} already exists.!",
                message_body=f"A ContinentList '{new_key}' "
                             f"already exists. Please choose another continent list and try again."
            )

        new_continentlist = first_continentlist + second_continentlist
        WebUI.get_all_continentlists().append(new_continentlist)
        return render_template("create/confirm_join_continentlist_created.html",
                               first_continentlist=first_continentlist,
                               second_continentlist=second_continentlist,
                               new_continentlist=new_continentlist
                               )
