import json
import os

def load_prods(file_produtos):
    if os.path.exists(file_produtos):
        with open(file_produtos, 'r') as f:
            return json.load(f)
    return file_produtos

def save_prods(produtos, file_produtos):
    with open(file_produtos, 'w') as f:
        json.dump(produtos, f)


def load_compras(file_compras):
    if os.path.exists(file_compras):
        with open(file_compras, 'r') as f:
            return json.load(f)
    return {}


def save_compras(compras, file_compras):
    with open(file_compras, 'w') as f:
        json.dump(compras, f)
