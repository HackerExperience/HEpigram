# Introduction

HEpigram documents are identified by a file named `hepigram.yml` at the document root. No other HEpigram document can be created within a document root.

# Required entries

HEpigram requires that your 'hepigram.yml` have the two following arguments:

- **title** - Your document title/name.
- **chapters** - An *accurate* list of chapters and pages within the document.

However, if your `hepigram.yml` is just *pointing* to another HEpigram document, the above entries are not needed. Instead, you'll need to specify a **source** repository, with an optional **source_path** within that source repository.

# Additional entries

### Themes

- **theme** - You can use the `theme` entry to specify a [MkDocs built-in theme](http://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes) or a custom theme. If it's a custom theme, you must have a correct `theme_dir` entry.
- **theme_dir** - Point to a relative folder within that document, or to a remote git repository containing the theme. 


# Example configs

    title: lol
    chapters:
      - 'index'
      - 'Chapter 1':
        - 'Page 1.1'
        - 'Page 1.2'
      - 'Chapter 2':
        - 'Page 2.1'


