import os
import json


def fixture(filename, asjson=True):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", f"{filename}.json")
    with open(path, encoding="utf-8") as fptr:
        if asjson:
            return json.loads(fptr.read())
        return fptr.read()
