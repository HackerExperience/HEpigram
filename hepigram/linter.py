import os
from hepigram.mkdocs import DEFAULT_THEMES
from hepigram.git_handler import CLONE_PATH


class HEpigramLinter:

    @staticmethod
    def display(errors, warnings):
        if errors:
            raise Exception(errors.pop(0))
        for warning in warnings:
            print('[WARNING] - ' + warning)

    @staticmethod
    def lint_config(yaml_data, input_data):

        errors = []
        warnings = []

        # We need a `chapters` entry...
        if 'chapters' not in yaml_data and 'source' not in yaml_data:
            errors.append('Missing chapter layout.')
        elif 'source' in yaml_data:
            return

        # If first chapter is not a single file then we do not have a
        # pre-defined index.html entry; will 404 on default MkDocs webserver.
        elif not isinstance(yaml_data['chapters'][0], str):
            warnings.append('Missing index file (first chapter is a list). '
                            'You might get a 404 on "/". '
                            'To fix this, make sure your webserver redirects '
                            '`index.html` to `<first_chapter>/index.html`')

        # We need a `title` entry...
        if 'title' not in yaml_data:
            errors.append('Missing title entry.')

        # Make sure that he selected an existing theme
        if 'theme' in yaml_data and 'theme_dir' not in yaml_data:
            if yaml_data['theme'].lower() not in DEFAULT_THEMES:
                warnings.append(
                    'Theme {} not found.'.format(yaml_data['theme'])
                )

        # Make sure the specified theme directory exists.
        elif 'theme_dir' in yaml_data:
            if not os.path.isdir(yaml_data['theme_dir']):
                errors.append('The specified theme dir does not exists.')

        elif 'theme' not in yaml_data and not input_data['theme']['name']:
            yaml_data['theme'] = 'readthedocs'
            if not input_data['theme']['path']:
                warnings.append('You should specify a theme; '
                                'defaulting to `readthedocs`.')

        # We need a hepigram.yml at the document source
        if input_data['source']['type'] == 'git':
            source_path = CLONE_PATH
        else:
            source_path = input_data['source']['path']
        if not os.path.exists(source_path + '/hepigram.yml'):
            errors.append('Missing hepigram.yml at document source root.')

        HEpigramLinter.display(errors, warnings)

    @staticmethod
    def lint_input(input_data):

        errors = []
        warnings = []

        # Make sure `source` is a valid path
        if input_data['source']['type'] == 'path':
            if not os.path.isdir(input_data['source']['path']):
                errors.append('Provided source doesn\'t exists')

        # Make sure `source` is a valid git path
        elif input_data['source']['type'] == 'git':
            #raise NotImplementedError
            pass

        # Make sure `theme` and `theme-dir` are valid
        if input_data['theme']['name'] and not \
                input_data['theme']['name'].lower() in DEFAULT_THEMES:
            warnings.append('Specified theme not found.')
        elif input_data['theme']['path'] and not \
                os.path.isdir(input_data['theme']['path']):
            errors.append('Provided theme dir doesn\'t exists')

        # Warn if build-dir already exists
        if os.path.exists(input_data['build']['path']):
            warnings.append('Build directory already exists.')

        HEpigramLinter.display(errors, warnings)
