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

    with open(path, encoding = 'utf-8') as f:
        data = json.load(f)
    f.close()

    return data


def SaveJson(data:dict, path:str) -> None:
    """
    Manages Json file writing.

    Arguments:
        - data: A dictionary containing the updated data to be stored.
        - path: String indicating what file should be overwrited.
    """

    with open(path, 'w') as f:
        json.dump(data, f, indent = 4)
    f.close()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')