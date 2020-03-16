from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from os import name
from os import system
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pygments
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from pygments.lexers.data import YamlLexer

try:
    from pathlib import Path
except ImportError:
    try:
        from pathlib2 import Path
    except ImportError:
        pass

__all__ = ["open_file_dialog", "pygment_yaml", "clear_screen"]

root = Tk()
root.withdraw()


def open_file_dialog(
    title="Select file",
    initial_dir="/",
    file_type=("JSON files", "*.json"),
    return_pathobj=False,
):
    filename = askopenfilename(
        initialdir=initial_dir,
        title=title,
        filetypes=(file_type, ("all files", "*.*")),
    )
    if return_pathobj:
        filename = Path(filename)
    return filename


def pygment_yaml(yaml):
    lexed_yaml = list(pygments.lex(yaml, lexer=YamlLexer()))
    print_formatted_text(PygmentsTokens(lexed_yaml))


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")
