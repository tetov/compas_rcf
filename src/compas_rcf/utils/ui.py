"""User interface elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tkinter import Tk
from tkinter.filedialog import askopenfilename

try:
    from pathlib import Path
except ImportError:
    try:
        from pathlib2 import Path
    except ImportError:
        pass


root = Tk()
root.withdraw()


def open_file_dialog(
    title="Select file",
    initial_dir="/",
    file_type=("All types", "*.*"),
    return_pathobj=False,
):
    """Get filepath using open file dialog.

    Uses :any:`tkinter`.

    Parameters
    ----------
    title : :class:`str`, optional
        Window title.
    initial_dir : :class:`os.PathLike` or :class:`str`, optional
        Start directory.
    file_type : :class:`tuple`, optional
        File type filter. Define using a tuple where first value is a
        descriptor and the second a file glob. Defaults to ``("All types", "*.*")``
    return_pathobj : :class:`bool`, optional
        Return :class:`pathlib.Path` object instead of :class:`str`

    Returns
    -------
    :class:`str` or :class:`pathlib.Path`
    """
    filename = askopenfilename(
        initialdir=str(initial_dir),
        title=title,
        filetypes=(file_type, ("All types", "*.*")),
    )
    if return_pathobj:
        filename = Path(filename)
    return filename
