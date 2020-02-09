from tkinter import Tk
from tkinter.filedialog import askopenfilename

from colorama import init, Fore, Style


def open_file_dialog(initial_dir="/", file_type=('JSON files', '*.json')):
    root = Tk()
    root.filename = askopenfilename(initialdir=initial_dir, title="Select file",
                                    filetypes=(file_type, ("all files", "*.*")))
    return root.filename


def print_dict_w_colors(dict_):
    init(autoreset=True)

    for key in dict_:
        print(Fore.BLUE + Style.BRIGHT +
              "* " + str(key) + ": " +
              Style.RESET_ALL + Fore.GREEN + Style.DIM +
              str(dict_[key]))

    print()


if __name__ == "__main__":
    print(open_file_dialog())
