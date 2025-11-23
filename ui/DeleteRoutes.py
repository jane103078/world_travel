# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week8Web )
# Date: (11/13/2025)
# Description: PrintRoutes
# ***************************************************************

from ui.WebUI import WebUI
from flask import render_template, request
from logic.ContinentLists import ContinentLists


class DeleteRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/delete_continentlist")
    def delete_continentlist():
        return render_template("delete/delete_continentlist.html",
                               continentlists=WebUI.get_all_continentlists())

    @staticmethod
    @__app.route("/do_delete_continentlist", methods=["GET", "POST"])
    def do_delete_continentlist():
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
                message_header=f"Can't delete the continentlist!",
                message_body=f"You can't delete the '{ContinentLists.ALL_CONTINENTS}' !"
            )

        WebUI.get_all_continentlists().remove(continentlist)
        continentlist.delete()
        return render_template("delete/confirm_continentlist_delete.html", continentlist=continentlist)
