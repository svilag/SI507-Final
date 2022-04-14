import json
import os

CACHE = ["test", "list"]

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2, add=False):
    """ Serializes object as JSON. Writes content to the provided filepath.
        Appends to the end of the file. Checks if filepath exists.
        If not, appends file creating a new one if the file does not exists,
        else writes over the file. If add=True, appends to the end of the file.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON
        add (optional): optional parameter to tell the function to append to the end of the file

    Returns:
        None
    """
    if not os.path.exists(filepath):
        with open(filepath, 'a', encoding=encoding) as file_obj:
            json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
    else:
        if add is False:
            with open(filepath, 'w', encoding=encoding) as file_obj:
                json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
        else:
            with open(filepath, 'a', encoding=encoding) as file_obj:
                json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

write_json('./cache/test.json', CACHE)
