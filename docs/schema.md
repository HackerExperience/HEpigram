# Enabling HEpigram

In order to make HEpigram know about your documents, you must create a file called `hepigram.yml` to its root. All folders within the document root are considered to be part of that HEpigram repository.

# Chapters vs Pages

HEpigram supports both Chapters and Pages. The only purpose of Chapters is to assign a namespace to Pages. Using a simple analogy, Chapters are like folders, and Pages are like files.

### Adding a chapter

A chapter is represented by a folder. Create a folder with the PATH-safe chapter name. Now, add the chapter full name to `hepigram.yml` at section `chapters`.

##### Example 1 - Creating chapter "Getting Started"

1. At the document root, create a folder named `getting_started`.
2. Open HEpigram.yml, and add `- 'Getting Started':` to the `chapters` section, like below:

    
    chapters:
        - 'Getting Started':

Note that the configuration file above is not valid, because a chapter **requires** pages. Keep reading to learn how to add a page.

### Adding a page

A page is represented by a text file. Create a file with the PATH-safe page name, plus a HEpigram-enabled extension, like `.md`. Finally, add the page full name to `hepigram.yml`, under the `chapters` section. If the file is under a chapter (i.e. not on the root), then you must specify the file under that exact chapter.

##### Example 2 - Adding page "Introduction" to root document.

1. At the document root, create a page called `introduction.md`.
2. Open `hepigram.yml` and add `- 'Introduction'` right below the `chapters` section.

    
    chapters:
        - 'Introduction'
        
Note that on `hepigram.yml` a page does not have a `:` at the end. Only chapters do.

##### Example 3 - Adding page "Installation" under "Getting Started" chapter.

1. At the `getting_started` folder (example 1), add the file `installation.md`.
2. Open `hepigram.yml` and add `- 'Installation'` right below `- 'Getting Started':`. Example:


    chapters:
        - 'Getting Started':
            - 'Installation'
            
        
Note: as you can see, there is no need to specify the page extension at the configuration file.

### Ordering

The order of Chapters and Pages is the same as defined on `hepigram.yml`, so it doesn't matter if your chapters look out-of-order in your document root.

