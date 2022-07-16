"""Manages template creation for Ticket Dictionary file update."""

#Internal Modules:
from Constants import Paths
from TemplateCreator.TCGUI import *
from FileHandler.JsonHandler import *


def TemplateCreator() -> None:
    ticket_dictionary = LoadJson(Paths.DICTIONARY_JSON_PATH)
    new_template:dict

    ticket_dictionary.update(new_template)
    #! SaveJson(ticket_dictionary, Paths.DICTIONARY_JSON_PATH)


#Script file.
if __name__ == "__main__":
    TemplateCreator(LoadJson(Paths.DICTIONARY_JSON_PATH))