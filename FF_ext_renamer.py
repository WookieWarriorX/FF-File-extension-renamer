import os
import sys


HELP = """
"Free and Flexible File extension renamer"
By Anton Sukhanov, 2023
Released under a "Simplified BSD" license
 ------
This program allows to add, change and delete file extensions.
Use case:
   "Enter an extension to search in the current folder and rename files: avi
    Enter a new extension for matched files: dat
    Matched files:
    myvideo.avi renamed to myvideo.dat
    myvideo2.avi renamed to myvideo2.dat
    myvideo3.avi renamed to myvideo3.dat"
In the first field you enter the search criteria in the current folder: 
    1) your extension 
    2) "all" to select all files in folder
    3) "add" to add extension to all files in folder
In the second field enter the new extension for the selected files:
    1) your extension
    2) "none" to remove extension
"""
GREETING = """Welcome to "FF File renamer" - print "help" for 
more info, "quit" or "exit" to quit program."""


class ExtRenamer:
    """
    "Free and Flexible File extension renamer"
    Use Python 3.10

    Allows to add, change and delete file extensions.
    """
    def __init__(self):
        self.dir_path = 'not located'
        self.curr_ext = ''
        self.new_ext = ''
        self.dir_content = []
        self.search_criteria = ''
        self.matched_files = []

    @staticmethod
    def help():
        """
        Prints help info.
        :return: None
        """
        print(HELP)

    @staticmethod
    def isfile(dir_path, file):
        return os.path.isfile(os.path.join(dir_path, file))

    @staticmethod
    def user_agreed():
        while True:
            user_input = input("Rename files? Enter Y or N:\n").lower()
            if user_input in ('y', 'yes', 'yep', 'yeah'):
                return True
            elif user_input in ('n', 'no', 'not', 'nope'):
                sys.exit()

    def get_workdir_path(self):
        """
        Finds a path to the working directory.
        Uses sys.argv[0] for compatibility in "frozen" (.exe) state.
        :return: None
        """
        path = os.path.normpath(sys.argv[0])
        self.dir_path = os.path.dirname(path)
        print('Working directory -', self.dir_path, end='\n\n')

    def input_extension(self, message):
        """
        Get a task from user - current and new file extensions.
        :return: None
        """
        ext = ''
        while ext in ('help', ''):
            ext = input(message).lower()
            if ext == 'help':
                self.help()
            elif ext in ('quit', 'exit'):
                sys.exit()
        return ext

    def handle_task(self):
        """
        Handles user input, sets search criteria (entered extension
        or all files), formats current and new extensions.
        :return: None
        """
        if self.curr_ext.lower() == 'add':
            self.search_criteria = ''
            self.curr_ext = None
        elif self.curr_ext.lower() == 'all':
            self.search_criteria = ''
            self.curr_ext = '.'
        else:
            self.search_criteria = self.curr_ext
            self.curr_ext = '.' + self.curr_ext

        if self.new_ext.lower() == 'none':
            self.new_ext = ''
        else:
            self.new_ext = '.' + self.new_ext

    def make_search(self):
        """
        Searches for files in current folder that matches the search criteria.
        :return: None
        """
        self.dir_content = [file for file in os.listdir(self.dir_path)
                            if self.isfile(self.dir_path, file)]
        file_counter = 0
        print('Matched files:')

        for name in self.dir_content:
            if name.endswith(self.search_criteria):
                self.matched_files.append(name)
                new_name = name.rsplit(self.curr_ext, 1)[0] + self.new_ext
                print(name, 'rename to', new_name)
                file_counter += 1
        print(" ----- ", "\nTotal files found:", file_counter)

    def execute_task(self):
        """
        Renames matched files in working drectory.
        :return: None
        """
        file_counter = 0
        error_counter = 0
        print('Processed files:')

        for name in self.matched_files:
            try:
                new_name = name.rsplit(self.curr_ext, 1)[0] + self.new_ext
                os.rename(src=os.path.join(self.dir_path, name),
                          dst=os.path.join(self.dir_path, new_name))
                print(name, 'renamed to', new_name)
                file_counter += 1
            except Exception as exc:
                print("** ERROR:", name, "-", exc)
                error_counter += 1
        print(" ----- ",
              "\nTotal files renamed:", file_counter,
              "\nErrors:", error_counter)

    def run(self):
        """
        Launches extension rename sequence.
        :return: None
        """
        print(GREETING)
        self.get_workdir_path()
        self.curr_ext = self.input_extension(
            "Enter an extension to search in the current folder and "
            "rename files: ")
        self.new_ext = self.input_extension(
            "Enter a new extension for matched files: ")

        self.handle_task()
        self.make_search()
        if self.user_agreed():
            self.execute_task()


if __name__ == '__main__':
    renamer = ExtRenamer()
    renamer.run()
    input("* Press enter *")
