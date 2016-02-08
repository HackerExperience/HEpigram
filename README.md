# HEpigram

HEpigram is a tool that handles your documents automation, allowing your repositories to stay clean and organized.

On top of that, HEpigram adds a programmable and extensible layer to your documents, making its output fully customizable.

# Examples

### Simple use-case

Below is a simple example of HEpigram's usage. It receives as input your documents directory (or remote git path), and outputs to `/var/www` the compiled version with `MyTheme`.

    hepigram /etc/MyDocs /var/www --theme /etc/MyTheme --serve
    
### Better use-case

Suppose you have several git repositories (or directories) for your documents, like:

- MyDoc1
- MyDoc2
- MyDoc3

Then, you create an umbrella repository, called `Documents`, to point to each document. Something like:

    DOCS
    |-- MyDocs1 -> MyDocs1.git
    |-- MyDocs2 -> MyDocs2.git
    `-- MyDocs3 -> MyDocs3.git


(Note that we have 4 different repositories; 3 for documents and 1 for keeping them together).

Now, with HEpigram, you can assemble them in the following way:

    hepigram /path/to/Docs.git /var/www --theme /path/to/Theme.git
    
HEpigram will follow the reference, fetch each MyDocs repository, compile each one and output them to `/var/www`, like:

    /var/www
    |-- MyDocs1
    |-- MyDocs2
    `-- MyDocs3

Now, with a webserver, you can navigate and surf trough your documentation. For a quick webserver setup, use the `--serve` flag (not recommended for production).


# License

HEpigram is licensed under the MIT license.  

Copyright (c) 2016 Neoart Labs, LLC
