#!/usr/local/bin/python3

import os
import sys
import urllib.request as urllib
from socket import timeout
import re
import errno

# global constants
WEB_SOURCE = "http://ftp.ncbi.nih.gov/pubmed/J_Medline.txt"

CACHE_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + "/dat/"
CACHE_FILE = "bibabbrev-cache.txt"
SUPPLEMENT_FILE = os.path.dirname(os.path.realpath(sys.argv[0])) + "/dat/bibabbrev-supplement.txt"
CACHE_SOURCE = CACHE_DIR + CACHE_FILE
ALLOWED_ARGS = ['-w', '--web', '-d', '--download', '-c', '--cache', '-b', '--bibtex']
SOURCE_SIZE = 1024 * 150  # the source is quite large; we allow for up to 15 MB by default
SPECIAL_CHARS = '[\s\\\\,.;\{\}\(\):&]'

def main():
    settings = process_args(sys.argv)
    abbreviations = get_abbreviations(settings)
    inData = read_data(settings)
    notFound = abbreviate_and_output(inData, abbreviations)
    
    print("Journals not found:", file=sys.stderr)
    i = 0
    for nf in notFound.keys():
        print(nf, file=sys.stderr)
        i = i+1
    print("total = ", str(i), file=sys.stderr)
    


def get_abbreviations(settings):
    succeeded = False
    cacheFailed = downloadFailed = supplFailed = False
    
    # first we try cache
    try:
        data = read_cache(settings['cache'])
    except IOError:
        print("Error opening cache from ", settings['cache'], file=sys.stderr)
        cacheFailed = True
        
    # now try download, if necessary
    if cacheFailed or settings['force_download']:
        try:
            data = download_data(settings['web'])
        except (urllib.URLError, timeout):
            print("Error opening site: ",settings['web'], file=sys.stderr)
            downloadFailed = True
        else:
            try:
                write_cache(data, settings['cache'])
            except IOError:
                print("Warning: Could not write cache to ", settings['cache'], file=sys.stderr)        

    # finally grab supplemental data
    try:
        with open(settings['supplement']) as f:
            supData = f.readlines()
    except IOError:
        print("Could not load supplemental list of journal abbrevations: ", F, file=sys.stderr)
        suppFailed = True
    else:
        data.extend(supData)
        
    if cacheFailed and downloadFailed and suppFailed:
        raise RuntimeError ("Unable to read cache, download, or supplemental abbrevaitions; no abbrevaition data!")

    # processedData is a dict with journal names as keys and abbreviations as values
    processedData = process_data(data)
    return(processedData)

    
def download_data(source):
    # open the url, download data to a maximum of SOURCE_SIZE, then convert the byte string to unicode
    print("Trying to download", source, "\nthis may take a few minutes depending on connection speed", file=sys.stderr)
    data = urllib.urlopen(source, timeout=300).read(SOURCE_SIZE).decode()
    data = data.split("\n")
    return data


def process_data(data):
    result = {}
    titleFound = False
    for l in data:
        if not titleFound:
            titleFound = re.search('JournalTitle: (.+)', l)
            if titleFound:
                title = titleFound.group(1)
                # make lowercase and strip special characters and whitespace
                title = re.sub(SPECIAL_CHARS,'',title).lower()
        else:
            abbrev = re.search('MedAbbr: (.+)', l)
            if abbrev:
                result[title] = abbrev.group(1)
                titleFound = False
            elif re.search('-----', l):
                # check for the end of a record, to guard against the possibility of a title not having an abbreviation
                titleFound = False
    return result
        


def read_cache(file):
    with open(file) as f:
        data = f.readlines()
    return data


def write_cache(data, destination):
    # if we are using the default, try to create the directory
    # if an exception is raised, check to see if it is due to the directory already existing
    # if not, re-raise the exception
    if destination == CACHE_SOURCE:
        try:
            os.makedirs(CACHE_DIR)
        except FileExistsError:
            pass
    with open(destination, 'w') as f:
        for l in data:
            print(l, file=f)           


def read_data(settings):
    result = []
    if settings['bibtex'] == 'stdin':
        result = sys.stdin.readlines()
    else:
        with open(settings['bibtex']) as f:
            result = f.readlines()
    return result


def abbreviate_and_output(bibData, abbreviations):
    notFound = {}
    for l in bibData:
        journalMatch = re.search("Journal\s+=\s+(.+),",l, re.IGNORECASE)
        if journalMatch:
            journalName = journalMatch.group(1)
            # remove curly braces
            journalName = re.sub("[\{\}]", "", journalName)
            # strip out special characters
            journalNameSimple = re.sub(SPECIAL_CHARS, "", journalName)
            if journalNameSimple.lower() in abbreviations.keys():
                l = re.sub(journalName, abbreviations[journalNameSimple.lower()], l)
            else:
                notFound[journalName] = True
        print(l, end="")
    return notFound
    

def process_args(args):
    name = args[0]
    args.pop(0)

    if "-h" in args or "--help" in args:
        help(name)
    
    settings = dict()
    # set defaults
    settings['cache'] = CACHE_SOURCE
    settings['force_download'] = False
    settings['web'] = WEB_SOURCE
    settings['bibtex'] = 'stdin'
    settings['supplement'] = SUPPLEMENT_FILE
    
    while args:
        curArg = args[0]
        args.pop(0)
        if curArg not in ALLOWED_ARGS:
            print("Unkown argument ", curArg, "\n")
            help(name, 1)
            
        if curArg == '-d' or curArg == '--download':
            settings['force_download'] = True
        elif curArg == '-w' or curArg == '--web':
            settings['web'] = args[0]
            args.pop(0)
            args.append('-d')
        elif curArg == '-c' or curArg == '--cache':
            settings['cache'] = args[0]
            args.pop(0)
        elif curArg == '-s' or curArg == '--supplement':
            settings['supplement'] = args[0]
            args.pop(0)
        elif curArg == '-b' or curArg == '--bibtex':
            settings['bibtex'] = args[0]
            args.pop(0)
    return settings        
        
def help(name, code=0):
    print("Usage:")
    print(name )
    print("The script will download most data from a web source. However, it will also")
    print("accept abbreviations from a local source (to supplement the web source), which")
    print("is located at {0}.".format(SUPPLEMENT_FILE))
    print("See the file included with this repo for the format.\n")
    print("Optional arguments:")
    print("""  -b, --bibtex: specify a bibtex file to be read and abbreviated; if 
                missing, default is to read from stdin\n""")
    print("  -c, --cache: specify location for the cache; default is \n{0}\n".format(CACHE_SOURCE))
    print("  -c, --supplement: specify location for the additional abbreviations; default is \n{0}\n".format(SUPPLEMENT_FILE))
    print("""  -d, --download: force program to download the file from the web, 
                  overriding any cached version\n""")
    print("""  -w <site>, --web <site>: download abbreviations from the specified site; 
                implies -d as well; default is 
                {0}""".format(WEB_SOURCE))
    sys.exit(code)

if __name__ == '__main__':
    main()

