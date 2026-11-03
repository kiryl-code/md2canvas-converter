import os
import subprocess


class StdoutKit:
    """
    Just some helper methods to style/format
    text in the console.
    """

    @staticmethod
    def yellow_bg(text: str):
        print(f"\033[30;103m{text}\033[0;0m")

    @staticmethod
    def yellow(text: str):
        print(f"\033[93m{text}\033[0;0m")

    @staticmethod
    def red(text: str):
        print(f"\033[91m{text}\033[0m")

    @staticmethod
    def green(text: str):
        print(f"\033[92m{text}\033[0m")

    @staticmethod
    def cyan(test: str):
        print(f"\033[96m{test}\033[0m")

    @staticmethod
    def magnetta(text: str):
        print(f"\033[95m{text}\033[0m")

    @staticmethod
    def clear():
        if os.name == "nt":
            subprocess.call("cls", shell=True)
        else:
            subprocess.call("clear", shell=True)

    @staticmethod
    def delimiter():
        print("=" * 40)

    @staticmethod
    def simple_delimiter():
        print("-" * 40)

    @staticmethod
    def test_header(text: str):
        StdoutKit.magnetta(f"Test {text}")

    @staticmethod
    def error(message: str):
        StdoutKit.red(f"Error: {message}")
