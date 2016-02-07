# Installation

HEpigram requires Python 3 and its package manager, PyPi. To install them on Ubuntu/Debian, use
    
    apt-get install python3 python3-pip

On different linux distributions the command might be different, but usually the package name is the same.

After Python 3 and pip are installed, simply install HEpigram with

    pip3 install hepigram
    
That's it! pip will take care of all HEpigram's dependencies.

# Usage

    usage: hepigram [-h] [--theme THEME] [--theme-dir THEME_DIR] [--debug]
                    [--build-dir BUILD_DIR] [--remove-build-dir] [--serve]
                    source output

HEpigram requires two arguments, an `source` and `output` location. `source` is a folder or git repository that contains your documents. `output` is the place that HEpigram will save the final, compiled HTML files.

You can specify a custom theme with `--theme` and `--theme-dir`. Use `--theme` to choose between [MkDocs built-in themes](http://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes) or `--theme-dir` to specify your custom theme (local folder or remote git repository). If a theme is specified on the document configuration file, and another on the CLI command, the CLI command will take over.

Use the `--build-dir` flag to specify a custom directory for building. By default HEpigram uses `/tmp/hepigram`.

The `--serve` flag will start MkDocs' HTTP server at `127.0.0.1:8000`. Useful for development and a quick glance of the final result, but not recommended for production.

