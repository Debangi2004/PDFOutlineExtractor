import json
import os

def load_persona(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)