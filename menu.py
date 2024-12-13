import os
import platform
from time import sleep

ascii = """                                                                             
*(((((((((((((((((((((((((((((((((((((((((((((((             
    ((((((((((((((((((((((((((((((((((((((((((((             
     ,((((((                               (((((             
       (((((*                              (((((             
          ,((((((                          (((((             
             ((((((/                       (((((             
               ,((((((                     (((((             
                  ((((((                   (((((             
                    (((((,                 (((((             
                  /((((((                  (((((             
                 (((((/                    (((((             
             /((((((                       (((((             
            (((((,                         (((((             
          /((((((                          (((((             
       (((((                               (((((             
    ((((((/////////////////////////////////(((((             
((((((((((((((((((((((((((((((((((((((((((((((((             
"""

red = "\033[91m"
blue = "\033[94m"
dblue = "\033[38;2;78;96;246m"
purple = "\033[95m"
green = "\033[92m"
yellow = "\033[93m"
reset = "\033[0m"

username = os.getlogin()
current_dir = os.getcwd()
computer_name = platform.uname().node

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{dblue}{ascii}{reset}")
    sleep(1.5)
    print(f"""
{purple}Welcome to the VirusTotal API script.

{yellow}Made with love and passion by @YureiNox --> https://github.com/yureinox
{blue}
[1] - Scan a file
[2] - Scan a URL
[3] - Search (hash, domain, IP)
[4] - Exit

""")
    sleep(0.5)
    choice = input(f""" {blue}
┌──({red}VirusTotal{blue}@{red}{username}{blue}) ~ [{red}{computer_name}{blue} Ϟ {red}{current_dir}{blue}]
└─> """)
    
    if choice == "1":
        os.system("python file.py")
        menu()
    elif choice == "2":
        os.system("python url.py")
        menu()
    elif choice == "3":
        os.system("python report.py")
        menu()
    elif choice == "4":
        print(f"{red}Exiting...{reset}")
        sleep(1)    
        exit()

if __name__ == "__main__":
    menu()