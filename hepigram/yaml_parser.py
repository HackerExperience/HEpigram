import yaml
import re

TEXT_FILE_EXTENSION = '.md'


class YAMLParser:

    def parse(self, chapters, folder=None):
        """Iterate trough our chapter data and return a list containing each
        chapter and its corresponding children (section, sub-sections, ...)

        It also points each chapter or section to its file location"""

        if not folder:
            folder = []

        # If `chapters` is a string we are at the leaf.
        if isinstance(chapters, str):
            chapter_name = nice_string(chapters)

            if folder[:-1] == chapter_name:
                chapter_name = 'index'

            folder = '' if not folder else '/'.join(folder) + '/'

            return folder + chapter_name + TEXT_FILE_EXTENSION

        # This is a hack :|
        if isinstance(chapters, list):
            chapters = {'chapters': chapters}

        result = []

        for key, value in chapters.items():
            for entry in value:

                # Make sure we have a proper dictionary key. If `entry` is a
                # dict than we have children (chapter -> section or
                # section -> subsection). In that case, we handle the
                # dictionary and `cd` to the correct (sub)section folder.
                if isinstance(entry, dict):
                    title = list(entry.keys())[0]
                    folder.append(nice_string(title))

                # If, however, `entry` is just a string, then we'll just append
                # it to our final result. No need to play with directories.
                else:
                    title = entry

                # Recursively append all the things to the final result.
                result.append(
                    {title: self.parse(entry, folder=folder)}
                )

            # This is the same as `cd ..`
            if len(folder) > 0:
                folder.pop()

            return result


class YAMLHandler:

    @staticmethod
    def read(path):
        """Read the given yaml file and return it as a Python dictionary"""
        with open(path, 'r') as file:
            return yaml.load(file)


def nice_string(input_str):
    """Receive a string input and return it in a clean way.

    The received input must be a string. We must return the same string without
    uppercase letters and replacing all spaces with underscores. We must also
    make sure that no other char is present other than az09_"""
    output_str = input_str.lower().replace(' ', '_')

    # Make sure we only have trusted characters (lowercase, number, underscore)
    if re.findall('[^a-z0-9_\-.+$]', output_str):
        raise Exception("Invalid filename " + output_str)

    return output_str



