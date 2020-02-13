from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from os import name
from os import system
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from colorama import Fore
from colorama import Style
from colorama import init
from confuse import ConfigTypeError


def open_file_dialog(initial_dir="/", file_type=("JSON files", "*.json")):
    root = Tk()
    root.filename = askopenfilename(
        initialdir=initial_dir,
        title="Select file",
        filetypes=(file_type, ("all files", "*.*")),
    )
    return root.filename


def print_conf_w_colors(conf):
    """Prints dicts styled based on hierarchy, supports 1 level of nested dicts."""

    init(autoreset=True)
    print()

    for key in conf.keys():
        try:
            print(Fore.BLUE + Style.BRIGHT + "* " + str(key) + ":")
            for subkey in conf[key].keys():
                print(
                    Fore.GREEN
                    + Style.DIM
                    + "    - "
                    + str(subkey)
                    + ": "
                    + Fore.YELLOW
                    + str(conf[key][subkey])
                )
        except ConfigTypeError:
            print(
                Fore.BLUE
                + Style.BRIGHT
                + "* "
                + str(key)
                + ": "
                + Fore.GREEN
                + Style.DIM
                + str(conf[key])
            )

    print()


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")
