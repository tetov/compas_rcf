from tkinter import Tk
from tkinter.filedialog import askopenfilename


def open_file_dialog(file_type=('JSON files', '*.json')):
    root = Tk()
    root.filename = askopenfilename(initialdir="/", title="Select file", filetypes=(file_type, ("all files", "*.*")))
    return root.filename


if __name__ == "__main__":
    print(open_file_dialog())
