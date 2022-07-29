"""Manages JSON files read and write."""

#Native Modules:
import json


def LoadJson(path:str) -> dict:
    """
    Manages Json file reading.\n
    Returns a dict with loaded JSON file data.
    
    Arguments:
        - path: A string indicating what file should be loaded.
    """

    with open(path, encoding = 'utf-8') as file:
        data = json.load(file)
    file.close()

    return data


def SaveJson(data:dict, path:str) -> None:
    """
    Manages Json file writing.

    Arguments:
        - data: A dictionary containing the updated data to be stored.
        - path: String indicating what file should be overwrited.
    """

    with open(path, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)
    file.close()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')