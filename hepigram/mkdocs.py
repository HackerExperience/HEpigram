import shutil
import yaml
import os
from hepigram.utils import call, absolutify
from hepigram.git_handler import is_git_uri


DOCUMENTS_FOLDER = 'docs'
MKDOCS_CONF_NAME = 'mkdocs.yml'
DEFAULT_THEMES = ['mkdocs', 'readthedocs', 'bootstrap', 'amelia', 'cerulean',
                  'cosmo', 'cyborg', 'flatly', 'journal', 'readable',
                  'simplex', 'slate', 'spacelab', 'united', 'yeti']


class MkDocs:

    CONFIG = None
    BUILD_DIR = ''
    DOCS_DIR = ''
    OUTPUT_DIR = ''

    def generate_config(self, hepigram_yaml, chapters_data, input_data):
        """This function will generate the final MkDocs configuration
        according to whatever was specificed on hepigram.yaml. It consists of
        two dicts: `base_config` and `optional_config`. `base_config` is
        filled with expected/important data while `optional_config` is
        generated according to extra parameters."""

        base_config = {
            'site_name': hepigram_yaml['title'],
            'docs_dir': self.BUILD_DIR,
            'pages': chapters_data,
            'theme': hepigram_yaml['theme']
        }

        optional_config = dict()

        # Custom theme support (if specified)
        if 'theme_dir' in hepigram_yaml:
            optional_config['theme_dir'] = absolutify(
                hepigram_yaml['theme_dir']
            )
        elif input_data['theme']['path']:
            optional_config['theme_dir'] = absolutify(
                input_data['theme']['path']
            )

        # Merge `base_config` and `optional_config`
        config_data = base_config.copy()
        config_data.update(optional_config)

        self.CONFIG = config_data

    def save_config(self):
        """Save the generated config to MKDOCS_CONF_NAME located on our tmp
        build environment."""

        with open(self.config_file(), 'w') as file:
            file.write(yaml.dump(self.CONFIG, default_flow_style=False))

    def create_build_env(self):

        # Create the build dir, if it doesnt exists.
        os.makedirs(self.BUILD_DIR, exist_ok=True)

        # Copy theme to build location

        # Copy source files to build dir.
        if self.DOCS_DIR != self.BUILD_DIR:
            cmd = 'cp -r {source}/* {build} >> /dev/null'.format(
                source=self.DOCS_DIR, build=self.BUILD_DIR
            ).replace('//*', '/*')
            call(cmd, shell=True)

    def destroy_build_env(self):
        """Removes the temporary environment used to build/compile the docs."""
        shutil.rmtree(self.BUILD_DIR, ignore_errors=True)

    def build(self):

        cmd = 'mkdocs build -f {config} -d {output} --clean'.format(
            config=self.config_file(), output=self.OUTPUT_DIR
        ).split(' ')
        call(cmd)

    def serve(self):

        cmd = 'mkdocs serve -f {config} --livereload'.format(
            config=self.config_file(),
        ).split(' ')
        call(cmd)

    def config_file(self):
        return self.BUILD_DIR + '/' + MKDOCS_CONF_NAME
