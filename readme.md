This is a series of short scripts designed to do a few simple manipulations to bibtex files that I found I needed frequently. A short description follows, with some usage examples. For all scripts, running <scriptname.py> -h will show command line arguments and basic usage.

**bibabbrev.py**

This script gathers a list of standard journal abbreviations from the web, then applies them to a .bib file. The output (via stdout) is a new .bib file with the journal names abbreviated. This saves the effort of maintaining two .bib libraries (one with journal names abbreviated and one not).

There is also support for adding your own abbreviations by adding to the file dat/bibabbrev-supplement.txt. bibabbrev will output to stderr the list of any journals that were not found in the abbreviation list; this can be a starting point for which journals to add to the supplement.

Usage: 

* `bibabbrev.py -b bibtex_library.bib` *or* 
* `cat bibtex_library.bib | bibabbrev.py`

**bibtally.py**

Parses one or more latex files for citations, then outputs a list of the citation keys. Input can be via a list of files or from stdin; output is to stdout.

Usage:

* `bibtally.py file1.tex file2.tex file3.tex` *or*
* `cat file.tex | bibtally.py`

**bibextract.py**

Given a bibtex library and a list of keys (for example, the output of `bibtally.py`), `bibextract.py` finds the citations in the library matching the list of keys and extracts them into a new bibtex library containing only those keys. Output is via stdout. If the list of keys is omitted, it is read from stdin.

Usage:

* `bibextract.py bibtex_library.bib list_of_keys` *or*
* `bibtally.py file.tex | bibextract.py bib_library.bib`

**bibcount.py**
With a latex file and a list of keys (for example, the output of `bibtally.py`), this will count how many times each citation key is cited and output the results via stdout. If the list of keys is omitted, it is read from stdin.

Usage:

* `bibcount.py file.tex list_of_keys` *or*
* `bibtally.py file1.tex | bibcount.py file1.tex`