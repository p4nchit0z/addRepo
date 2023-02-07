#/usr/bin/python3

from tabulate import tabulate
import argparse
import sys
import shutil
import textwrap
from pathlib import Path
import csv

# ANSI escape codes dictionary
colors = {
        "BLACK": '\033[30m',
        "RED": '\033[31m',
        "GREEN": '\033[32m',
        "BROWN": '\033[33m',
        "BLUE": '\033[34m',
        "PURPLE": '\033[35m',
        "CYAN": '\033[36m',
        "WHITE": '\033[37m',
        "GRAY": '\033[1;30m',
        "L_RED": '\033[1;31m',
        "L_GREEN": '\033[1;32m',
        "YELLOW": '\033[1;33m',
        "L_BLUE": '\033[1;34m',
        "PINK": '\033[1;35m',
        "L_CYAN": '\033[1;36m',
        "NC": '\033[0m'
        }

# Define a simple character to print steps
sb: str = f'{colors["L_CYAN"]}[*]{colors["NC"]}'
whitespaces: str = " "*(len('[*]')+1)

def parse_args() -> argparse.Namespace:
    """
    Simple function to get flags given by the user
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an argument called "--flag" with action "store_true"
    parser.add_argument("-f", "--filename", type=str, default = "repositories.txt",
                        help="Filename containing repositories to display (usually the file generated by addRepo.py)")
    parser.add_argument("--no-color", action="store_true",
                        help="Do not display the table with colors")

    # Parse the command-line arguments
    args = parser.parse_args(sys.argv[1:])

    return args


def create_table_elements(flags_var):
    """
    Creates items that will be stored inside 'tabulate' object
    """
    original_header = ["Repository Name", "OS", "Language", "Description"]
    if flags_var.no_color:
        headers_table = original_header

    else:
        # To print in color inside the table you have to use 'colorama'. Using ANSI codes bugs the table
        headers_table = [f"{colors['RED']}Repo Name{colors['NC']}",
                         f"{colors['RED']}OS{colors['NC']}",
                         f"{colors['RED']}Language{colors['NC']}",
                         f"{colors['RED']}Description{colors['NC']}"]

        print(headers_table)
    body = [["test", "Linux", "Python", "Da best"]]
    return headers_table, body
    

def check_file_to_read(flags_var) -> None:
    """
    Check if the file that stores all the repositories exists
    """

    # Get the path where the script is being executed (current path, not where the script is stored)
    file_to_read = Path.cwd().joinpath(flags_var.filename)

    # Get file path
    file_path = Path(file_to_read)

    # Check if the file containing the repositories exists
    if not file_path.exists():
        if not flags_var.no_color:
            print(f"{sb} {colors['RED']}Warning{colors['NC']}: '{file_to_read}' does not exist. Try using 'addRepo.py' to create a file and retry")
        else:
            print(f"[+] Warning: '{file_to_read}' does not exist. Try using 'addRepo.py' to create a file and retry")
        sys.exit(1)

    return None


def main():
    """MAIN"""
    # Get the flags from the user input
    flags = parse_args()
    # Check if the file that contains the repositories data exists (if not, exits)
    check_file_to_read(flags)
    # Define the headers for the table
    width = shutil.get_terminal_size()[0]
    print(f"Current terminal size -> width: {width}")
    headers_table, body_table = create_table_elements(flags)

    # Print the table
    print(tabulate(body_table, headers=headers_table, tablefmt="grid"))



if __name__ == "__main__":
        main()

