# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week9 CyberSecurity)
# Date: (11/21/2025)
# Description: WebUI
# ***************************************************************
import bcrypt
from flask import Flask, render_template, request, session
from flask_session import Session
from logic.ContinentLists import ContinentLists
import os



class WebUI:
    __all_cities = None
    __all_continentlists = []
    __app = Flask(__name__)
    MENU = {
        "Print": {
            "print_continentlist?continentlist=All%20Continents": "Print a list of all cities",
            "print_continentlists": "Print a list of all continentlists",
            "show_continentlist_contents": "Select a continentlist and show the contents",
        },
        "Create": {
            "create_tourist_city": "Create a new tourist city",
            "create_dream_city": "Create a new dream city",
            "create_continentlist": "Create a new continentlist",
            "join_continentlists": "Join two continentlists together",
        },
        "Update": {
            "update_city_attraction": "Update the attraction for the city",
            "add_city_to_continentlist": "Add the city to the continentlist",
        },
        "Delete": {
            "delete_continentlist": "Delete the continentlist",
            "remove_city_from_continentlist": "Remove the city from the continentlist",
        },
    }

    @classmethod
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_all_continentlists(cls):
        return cls.__all_continentlists

    @classmethod
    def get_all_cities(cls):
        return cls.__all_cities

    @classmethod
    def init(cls):
        """Initialize all cities from the database"""
        cls.__all_cities, cls.__all_continentlists = ContinentLists.read_data()

    @classmethod
    def validate_field(cls, object_name, field_name):
        if field_name not in request.form:
            return None, render_template(
                "error.html",
                message_header=f"{object_name} was not specified!!!",
                message_body=f"{object_name} was not specified. Please check the form and try again."
            )
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template(
                "error.html",
                message_header=f"{object_name} was not specified!!!",
                message_body=f"{object_name} was not specified. Please check the form and try again."
            )
        return field_value, None

    @staticmethod
    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)

    @classmethod
    def run(cls):
        from ui.PrintRoutes import PrintRoutes
        from ui.CreateRoutes import CreateRoutes
        from ui.UpdateRoutes import UpdateRoutes
        from ui.DeleteRoutes import DeleteRoutes

        if "APPDATA" in os.environ:
            path = os.environ["APPDATA"]
        elif "HOME" in os.environ:
            path = os.environ["HOME"]
        else:
            raise Exception("Couldn't find config folder")

        cls.__app.secret_key = bcrypt.gensalt()
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        Session(cls.__app)

        cls.__app.run(host="0.0.0.0",
                      port=8443,
                      ssl_context=(path + "/travel_world/cert.pem", path + "/travel_world/key.pem"),
                      debug=True)


if __name__ == '__main__':
    WebUI.init()
    WebUI.run()
