import os
import json
import time
import requests
from tkinter import Tk, filedialog
from datetime import datetime

def print_colored(text, color="white"):
    """Fonction pour imprimer le texte en couleur dans la console"""
    colors = {
        "green": "\033[32m",
        "red": "\033[31m",
        "blue": "\033[34m",
        "yellow": "\033[33m",
        "white": "\033[37m"
    }
    print(f"{colors.get(color, colors['white'])}{text}\033[0m", end="")

with open("config.json", "r") as f:
    config_data = json.load(f)
    xapi = config_data["x-api"]
    output_folder = config_data["output_folder"]

url = "https://www.virustotal.com/api/v3/files"

def select_file():
    Tk().withdraw()  
    file_path = filedialog.askopenfilename(title="Sélectionnez un fichier à scanner")
    return file_path

file_path = select_file()
filename = os.path.basename(file_path)
if not file_path:
    print("Aucun fichier sélectionné. Le script s'arrête.")
    exit()

files = {
    "file": (os.path.basename(file_path), open(file_path, "rb"), "application/octet-stream")
}
headers = {
    "accept": "application/json",
    "x-apikey": xapi
}

try:
    response = requests.post(url, files=files, headers=headers)
    response_data = response.json()  

    analysis_link = response_data.get("data", {}).get("links", {}).get("self")
    if analysis_link:
        print("Lien d'analyse trouvé :", analysis_link)

        analysis_response = requests.get(analysis_link, headers=headers)
        if analysis_response:
            analysis_data = analysis_response.json()
            
            status = analysis_data["data"]["attributes"].get("status", "unknown")
            if status == "queued":
                print_colored("\nAnalyse en cours... Le fichier est en file d'attente.\n", "yellow")
                print("Veuillez patienter environ 5 minutes, puis réessayez.")
                exit()

            results = analysis_data["data"]["attributes"]["results"]

            print("\nRésultats de l'analyse :\n")
            formatted_results = ""
            for engine, details in results.items():
                engine_name = details.get("engine_name", "Inconnu")
                category = details.get("category", "none")
                result_cat = details.get("result", "none")

                print_colored(f"{engine_name}: ", "yellow")
                if category == "undetected":
                    print_colored(category, "green")
                elif category == "malicious":
                    print_colored(category, "red")
                    print(f"\n\033[35m{result_cat}\033[0m")
                elif category == "suspicious":
                    print_colored(category, "red")
                    print(f"\n\033[35m{result_cat}\033[0m")
                elif category == "type-unsupported":
                    print(f"An error has occurred: {result_cat}")
                
                print("")  
                time.sleep(0.25)


                formatted_results += f"{engine_name}: {category}\n"

            today = datetime.now().strftime("%Y-%m-%d")
            json_log_file = os.path.join(output_folder, f"{filename}-{today}-reponse-json.log")
            clear_log_file = os.path.join(output_folder, f"{filename}-{today}-reponse-claire.log")

            with open(json_log_file, "w") as json_file:
                json.dump(analysis_data, json_file, indent=4)
            with open(clear_log_file, "w") as clear_file:
                clear_file.write(formatted_results)

            print(f"\nLogs sauvegardés dans {output_folder}.")
            input("Appuyez sur Entrée pour quitter.")
        else:
            print(f"Erreur lors de la récupération des résultats : {analysis_response.status_code}")
            print(analysis_response.text)
    else:
        print("Aucun lien d'analyse trouvé dans la réponse.")
except Exception as e:
    print("Une erreur est survenue :", e)
