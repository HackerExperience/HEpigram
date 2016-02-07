import argparse
from copy import deepcopy
from hepigram.yaml_parser import YAMLHandler, YAMLParser
from hepigram.mkdocs import MkDocs
from hepigram.linter import HEpigramLinter
from hepigram.utils import call, absolutify, get_extension, path_exists, walk, \
    thread
from hepigram.git_handler import GitHandler, CLONE_PATH


class HEpigram:

    DOCNAME = ''
    BUILD_DIR = ''
    SOURCE_PATH = ''
    CONFIG = None

    def __init__(self, pargs, in_thread=False):
        # Parse the input
        self.input_data = self.input_parser(pargs) if not in_thread else pargs

        # Start the Engine (:
        self.MkDocs = MkDocs()
        self.YAMLHandler = YAMLHandler()
        self.YAMLParser = YAMLParser()
        self.GitHandler = GitHandler()

        # Verify and store input arguments
        self.prepare_input()

        self.in_thread = True if in_thread else False

        # Start
        self.start()

    def prepare_input(self):
        """Lint the command-line arguments (input) & store it."""

        HEpigramLinter.lint_input(self.input_data)

        self.SOURCE_PATH = absolutify(self.input_data['source']['path'])
        self.BUILD_DIR = absolutify(self.input_data['build']['path'])

        self.GitHandler.ORIGIN_PATH = self.SOURCE_PATH

    def prepare_git(self):

        self.SOURCE_PATH = CLONE_PATH
        self.BUILD_DIR = CLONE_PATH

        # Clone repository to `CLONE_PATH`
        self.GitHandler.clone(CLONE_PATH)

    def prepare_mkdocs(self):
        self.MkDocs.BUILD_DIR = self.BUILD_DIR
        self.MkDocs.DOCS_DIR = self.SOURCE_PATH
        self.MkDocs.OUTPUT_DIR = absolutify(self.input_data['output'])

    def read_hepigram_config(self):

        # Read hepigram.yml that should exist on folder root
        if path_exists(self.SOURCE_PATH + '/hepigram.yml'):
            self.CONFIG = self.YAMLHandler.read(
                self.SOURCE_PATH + '/hepigram.yml'
            )
            return

        if self.in_thread:
            raise StopIteration

        # Since there is no hepigram.yml on root folder, this might be an
        # umbrella-like repository that contains others documents. Let's
        # iterate through all folders inside it and check for hepigram.yml.

        valid_hepigram_paths = []

        for root, dirs, files in walk(self.SOURCE_PATH, topdown=True):

            # Skip CVS-related files
            if self.SOURCE_PATH + '/.git' in root:
                continue

            if 'hepigram.yml' in files:
                valid_hepigram_paths.append(root)

        # Start a child HEpigram thread on each hepigram.yml found
        for root in valid_hepigram_paths:
            child_input = deepcopy(self.input_data)
            child_input['source']['type'] = 'path'
            child_input['source']['path'] = root
            child_input['serve'] = False

            thread(cmd=HEpigram, args=(child_input, {'in_thread': True}))

        self.CONFIG = {'delegated': True}

    def fetch_from_source(self, source):
        self.GitHandler.ORIGIN_PATH = source
        self.DOCNAME = str(self.SOURCE_PATH.split('/')[-1])
        self.SOURCE_PATH = CLONE_PATH + self.DOCNAME
        self.GitHandler.clone(self.SOURCE_PATH)

    def start(self):
        """Main function that coordinates HEpigram's lifecycle."""

        if self.input_data['source']['type'] == 'git':
            self.prepare_git()

        self.prepare_mkdocs()

        # Read hepigram.yml
        self.read_hepigram_config()

        if 'delegated' in self.CONFIG:
            return self.teardown()

        # Lint config file to make sure everything we need is there.
        HEpigramLinter.lint_config(self.CONFIG, self.input_data)

        # Check if the hepigram file points to another hepigram book.
        # In that case, we'll fetch that repository and its hepigram.yml
        if 'source' in self.CONFIG:
            self.fetch_from_source(self.CONFIG['source'])
            self.read_hepigram_config()
            HEpigramLinter.lint_config(self.CONFIG, self.input_data)

        if self.in_thread:
            self.MkDocs.OUTPUT_DIR += '/' + self.DOCNAME

        # Create build env
        self.MkDocs.create_build_env()

        # Read CHAPTERS.yml & apply HEpigram's rules.
        chapters_data = self.apply_rules(
            self.YAMLParser.parse(
                self.CONFIG['chapters']
            )
        )

        # Prepare stuff for building
        self.MkDocs.generate_config(
            self.CONFIG, chapters_data, self.input_data
        )
        self.MkDocs.save_config()

        # Pass the ball to MkDocs & start building
        self.MkDocs.build()

        self.teardown()

    def teardown(self):
        print('td')
        print(self.input_data)
        # Remove build env (if requested)
        if self.input_data['build']['flag_remove']:
            self.MkDocs.destroy_build_env()

        # Start MkDocs's own HTTP server (if requested)
        if self.input_data['serve']:
            self.MkDocs.serve()

    def apply_rules(self, chapters):
        """HEpigram-specific rules that must be applied to the given
        HEpigram.yml and then passed to MkDocs"""

        # Rule 1 - If first chapter is a single entry, rename it to index.

        if isinstance(chapters[0], dict):
            return chapters

        first_page = list(chapters[0].keys())[0]
        if first_page == 'index':
            return chapters

        # Change `first_page.md` to `index.md` on our build dir
        cmd = 'mv {build}/{fp}.md {build}/index.md'.format(
            build=self.BUILD_DIR, fp=first_page
        ).replace('//', '/')
        call(cmd, shell=True)

        # Change `first_page.md` to `index.md` on our chapters list.
        chapters[0][first_page] = 'index.md'

        return chapters

    @staticmethod
    def input_parser(pargs):

        # Source

        source = {
            'path': pargs.source
        }

        if '.' in pargs.source and get_extension(pargs.source) == 'git':
            source['type'] = 'git'
        else:
            source['type'] = 'path'

        theme = {
            'name': pargs.theme,
            'path': pargs.theme_dir
        }

        build = {
            'path': pargs.build_dir,
            'flag_remove': pargs.remove_build_dir
        }

        return {
            'source': source,
            'output': pargs.output,
            'debug': pargs.debug,
            'theme': theme,
            'build': build,
            'serve': pargs.serve
        }


def hepigram_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('output', type=str)
    parser.add_argument('--theme', type=str, default=None)
    parser.add_argument('--theme-dir', type=str, default=None)
    parser.add_argument('--debug', action='store_const', const=True,
                        default=False)
    parser.add_argument('--build-dir', type=str, default='/tmp/hepigram')
    parser.add_argument('--remove-build-dir', action='store_const', const=True,
                        default=False)
    parser.add_argument('--serve', action='store_const', const=True,
                        default=False)
    return parser


def cli():
    pargs = hepigram_parser().parse_args()
    HEpigram(pargs=pargs)
