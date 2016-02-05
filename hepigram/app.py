import argparse
from hepigram.yaml_parser import YAMLHandler, YAMLParser
from hepigram.mkdocs import MkDocs
from hepigram.linter import HEpigramLinter
from hepigram.utils import call, absolutify, get_extension
from hepigram.git_handler import GitHandler, CLONE_PATH


class HEpigram:

    BUILD_DIR = ''
    SOURCE_PATH = ''
    CONFIG = None

    def __init__(self, pargs):

        # Parse the input
        self.input_data = self.input_parser(pargs)

        # Start the Engine (:
        self.MkDocs = MkDocs()
        self.YAMLHandler = YAMLHandler()
        self.YAMLParser = YAMLParser()
        self.GitHandler = GitHandler()

        # Verify and store input arguments
        self.prepare_input()

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

    def start(self):
        """Main function that coordinates HEpigram's lifecycle."""

        if self.input_data['source']['type'] == 'git':
            self.prepare_git()

        self.prepare_mkdocs()

        # Read hepigram.yml
        self.CONFIG = self.YAMLHandler.read(self.SOURCE_PATH + '/hepigram.yml')

        # Lint config file to make sure everything we need is there.
        HEpigramLinter.lint_config(self.CONFIG, self.input_data)

        # Create build env
        self.MkDocs.create_build_env()

        # Read CHAPTERS.yml & apply HEpigram's rules.
        chapters_data = self.apply_rules(
            self.YAMLParser.parse(
                self.CONFIG['chapters']
            )
        )

        # Prepare stuff for building
        self.MkDocs.create_build_env()
        self.MkDocs.generate_config(
            self.CONFIG, chapters_data, self.input_data
        )
        self.MkDocs.save_config()

        # Pass the ball to MkDocs & start building
        self.MkDocs.build()

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
    HEpigram(pargs=pargs).start()
