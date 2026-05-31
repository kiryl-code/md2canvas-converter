from tkinter import filedialog


class FileSelectorDialog:
    """
    A reusable class that allows to select a file
    """
    def __init__(self, filetypes: list[tuple[str, str]] | None):
        """
        Constructs a FileSelectorDialog that allows to select
        provided types of files
        :param filetypes: defines which types of files to select
        """
        self.filetypes = filetypes

    def get_path(self, initial_directory: str = "/") -> str | None:
        """
        Asks user to select a file via tkinter.filedialog and
        returns the path of selected file or None if no file
        was selected
        :param initial_directory: a directory to start a dialog with
        :return: selected file or None
        """
        initial_directory = initial_directory.strip()
        initial_directory = initial_directory if initial_directory else "/"
        if self.filetypes:
            filepath = filedialog.askopenfilename(
                filetypes = self.filetypes,
                initialdir = initial_directory,
            )
        else:
            filepath = filedialog.askdirectory(
                initialdir = initial_directory
            )
        if filepath:
            return filepath
        return None