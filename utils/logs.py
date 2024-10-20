from colorama import Fore, init

init(autoreset=True)

def info(message):
    print(f"{Fore.YELLOW} ~INFO~ {message}")

def error(message):
    print(f"{Fore.RED} ~ERROR~ {message}")

def warning(message):
    print(f"{Fore.LIGHTYELLOW_EX} ~WARNING~ {message}")

def success(message):
    print(f"{Fore.GREEN} ~SUCCESS~ {message}")  

def debug(message):
    print(f"{Fore.MAGENTA} ~DEBUG~ {message}")
