""""""

#Internal Modules:
from HAF.Constants import Paths
from HAF.FileHandler.JsonHandler import *


def SortDictionary(unsorteddict:dict = LoadJson(Paths.DICTIONARY_JSON_PATH)) -> None:
    """
    Reorganizes template dictionary in alphabetical order.
    
    Arguments:
        - unsorteddict: a loaded template dictionary, defaults on loading the file,
        but can be passed as an argument for recent changes.
    """

    sorteddict = {}
    sortedkeys = sorted(unsorteddict.keys(), key = lambda x:x.lower())

    for i in sortedkeys:
        sorteddict[i] = unsorteddict[i]
    SaveJson(sorteddict, Paths.DICTIONARY_JSON_PATH)


def __ValidateTemplate(new_template:dict) -> bool:
    return True


def RegisterTeamplate(new_template:dict) -> bool:
    if __ValidateTemplate(new_template):
        template_dictionary = LoadJson(Paths.DICTIONARY_JSON_PATH)
        template_dictionary.update(new_template)
        SaveJson(template_dictionary, Paths.DICTIONARY_JSON_PATH)
        return True
    else:
        return False
