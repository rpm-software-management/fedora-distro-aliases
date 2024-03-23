import os
import json
from unittest.mock import patch, MagicMock


here = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(here, "data")


def mock_responses(files):
    """
    We can use this function to comfortably mock responses from saved files.
    """
    responses = []
    for name in files:
        path = os.path.join(datadir, name)
        with open(path, "r") as fp:
            data = json.load(fp)
        response = MagicMock()
        response.json.return_value = data
        responses.append(response)
    return responses
