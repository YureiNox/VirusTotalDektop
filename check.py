import os
import json
from tkinter import Tk, filedialog
import time

try:
    __import__("requests")
except ImportError:
    os.system("pip install requests")
    __import__("requests")

config_file = "config.json"

def get_xapi():
    return input("Entrez votre clé x-api : ")

def get_output_folder():
    Tk().withdraw()
    output_folder = filedialog.askdirectory(title="Sélectionnez un dossier de sortie pour les logs")
    if not output_folder:
        print("Aucun dossier de sortie sélectionné. Le script s'arrête.")
        exit()
    return output_folder

def save_config(xapi, output_folder):
    with open(config_file, "w") as f:
        f.write(json.dumps({"x-api": xapi, "output_folder": output_folder}))
    print("Configuration sauvegardée avec succès.")

if not os.path.exists(config_file) or os.stat(config_file).st_size == 0:
    print("Fichier config.json introuvable ou vide.")
    api = get_xapi()
    output_folder = get_output_folder()
    save_config(api, output_folder)
else:
    with open(config_file, "r") as f:
        try:
            config_data = json.load(f)
            xapi = config_data.get("x-api")
            output_folder = config_data.get("output_folder")

            if not xapi:
                print("Clé x-api manquante dans config.json.")
                xapi = get_xapi()
            
            if not output_folder:
                print("Dossier de sortie manquant dans config.json.")
                output_folder = get_output_folder()

            if not config_data.get("x-api") or not config_data.get("output_folder"):
                save_config(xapi, output_folder)

        except json.JSONDecodeError:
            print("Le fichier config.json est mal formaté.")
            xapi = get_xapi()
            output_folder = get_output_folder()
            save_config(xapi, output_folder)

print("Clé x-api et dossier de sortie configurés.")
print("Tout est prêt !")

os.system("python menu.py")
