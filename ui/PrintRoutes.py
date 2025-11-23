# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week8Web )
# Date: (11/13/2025)
# Description: PrintRoutes
# ***************************************************************

from ui.WebUI import WebUI
from flask import render_template, request
from logic.ContinentLists import ContinentLists


class PrintRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/print_continentlists')
    def print_continentlists():
        return render_template("print/print_continentlists.html", continentlists=WebUI.get_all_continentlists())

    @staticmethod
    @__app.route('/print_continentlist')
    def print_continentlist():
        if "continentlist" not in request.args:
            return render_template(
                "error.html",
                message_header="Continentlist not specified!!!",
                message_body="No continentlist was specfied. Please check the URL"
            )
        key = request.args["continentlist"]
        continentlist = ContinentLists.lookup(key)
        if continentlist is None:
            return render_template(
                "error.html",
                message_header="Continentlist not specified!!!",
                message_body=f"The Continentlist named '{key} was not found'. Please check the URL")
        return render_template("print/print_continentlist.html", continentlist=continentlist)

    @staticmethod
    @__app.route('/show_continentlist_contents')
    def show_continentlist_contents():
        return render_template("print/show_continentlist_contents.html",
                               continentlists=WebUI.get_all_continentlists())
