"""Manages JSON files read and write."""

#Native Modules:
import json


def LoadJson(path:str) -> dict:
    """
    Returns dict with loaded JSON file data.
    
    Arguments:
    - path: String indicating what file is to be loaded.
    """

    with open(path, encoding = 'utf-8') as f:
        data = json.load(f)
    
    f.close()
    return data


def SaveJson(data:dict, path:str) -> None:
    """
    Overwrites JSON file store data.

    Arguments:
    - data: dict containing the new data to be store in the file
    - path: String indicating what file is to be overwrited.
    """

    with open(path, 'w') as f:
        json.dump(data, f, indent = 4)

    f.close()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')