import json

def save_to_json(output, filename):
    """
    Sauvegarde une sortie API dans un fichier JSON.
    """
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)