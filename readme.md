This is a series of short scripts designed to do a few simple manipulations to bibtex files that I found I needed frequently. A short description follows, with some usage examples. For all scripts, running <scriptname.py> -h will show command line arguments and basic usage.

**bibabbrev.py**

This script gathers a list of standard journal abbreviations from the web, then applies them to a .bib file. The output (via stdout) is a new .bib file with the journal names abbreviated. This saves the effort of maintaining two .bib libraries (one with journal names abbreviated and one not).

There is also support for adding your own abbreviations by adding to the file dat/bibabbrev-supplement.txt. bibabbrev will output to stderr the list of any journals that were not found in the abbreviation list; this can be a starting point for which journals to add to the supplement.

usage: 

* `bibabbrev.py -b bibtex_library.bib` *or* 
* `cat bibtex_library.bib | bibabbrev.py`