#!/usr/bin/env python
# -*- coding: utf-8 -*-
from IPython import embed
"""
This script takes a BibTeX .bib file and outputs a series of .md files for use
in the Goa theme for Hugo, a general-purpose, static-site generating web
framework. Each file incorporates the data for a single publication.

Written for and tested using python 2.7

Requires: bibtexparser

Copyright (C) 2017 Mark Coster
Copyright (C) 2017 Raghav Khanna
"""

import argparse
import os

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bib_file", help="BibTeXfile to convert")
    parser.add_argument('dir', nargs='?', default='publication',
                        help="output directory")
    parser.add_argument("-s", "--selected", help="publications 'selected = true'",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    if args.verbose:
        print("Verbosity turned on")
        print("Opening {}".format(args.bib_file))

    try:
        with open(args.bib_file) as bib_file:
            parser = BibTexParser()
            parser.customization = customizations
            parser.alt_dict = {} # also important, otherwisee url's are not read as strings
            bib_data = bibtexparser.load(bib_file, parser=parser)
    except IOError:
        print('There was a problem opening the file.')

    if not os.path.exists(args.dir):
        if args.verbose:
            print("Creating directory '{}'".format(args.dir))
        os.makedirs(args.dir)
    os.chdir(args.dir)

    for index, entry in enumerate(bib_data.entries):
        if args.verbose:
            print("Making entry {0}: {1}".format(index + 1, entry['ID']))
#        if entry['ENTRYTYPE'] != 'article':
#            continue
        info = ['+++']
        if 'categories' in entry:
            categories = []
            for category in entry['categories'].split(", "):
                categories.append('"{}"'.format(category))
            info.append('categories = [{}]'.format(', '.join(categories)))
        else:
            info.append('categories = []')
        info.append('comments = false')
        if 'year' in entry:
            info.append('date = "{}-01-01"'.format(entry['year']))
#            info.append('image_preview = ""')
        info.append('draft = false')
        info.append('showpagemeta = true')
        info.append('showcomments = false') # important, otherwise category links don't work properly
        info.append('slug = ""')
        info.append('tags = []')    # important, otherwise content does not appear
#        if 'abstract' in entry:
#            abstract_clean = entry['abstract'].replace('"', '\\"')
#            info.append('abstract = "{}"'.format(abstract_clean))
#            info.append('abstract_short = "{}"'.format(abstract_clean))
        info.append('title = "{}"'.format(entry['title']))
        if 'author' in entry:    
            authors = []
            for idx, author in enumerate(entry['author']):
                if "," in author:
                    name = author.split(', ')
                    if idx == (len(entry['author'])-1) and idx !=0:
                        authors.append('and {} {}'.format(name[1], name[0]))
                    else:
                        if "Khanna" in author:
                            authors.append('{} {}'.format(name[1], name[0]))
                        else:
                            authors.append('{} {}'.format(name[1], name[0]))
            info.append('description = "{}"'.format(', '.join(authors)))
#        if 'journal' in entry:
#            journal_name = entry['journal']['name'].replace('\\', '')
#            info.append('publication = "{}"'.format(journal_name))
#        if 'volume' in entry:
#            volume = entry['volume'] + ', '
#        else:
#            volume = ''
#        if all (k in entry for k in ('year', 'pages')):    
#            info.append('publication_short = "{journal} {year}, {vol}{pages}"'.format(
#                journal=journal_name,
#                year=entry['year'],
#                vol=volume,
#                pages=entry['pages']))
#        info.append('selected = {}'.format(str(args.selected).lower()))
        info.append('+++\n')
        if 'abstract' in entry:
            info.append(entry['abstract'])
        if 'url' in entry:
            info.append("\n>[[full text]]({})".format(entry['url']))
        if 'code' in entry:
            info.append("\n>[[code]]({})".format(entry['code']))
        pub_info = '\n'.join(info)
        file_name = entry['ID'] + '.md'

        try:
            if args.verbose:
                print("Saving '{}'".format(file_name))
            with open(file_name, 'w') as pub_file:
                pub_file.write(pub_info)
        except IOError:
            print('There was a problem writing to the file.')


def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = doi(record)
    record = convert_to_unicode(record)
    record = abstract(record)
    record = pages(record)
    return record


def abstract(record):
    """
    Clean abstract string.

    :param record: a record
    :type record: dict
    :return: dict -- the modified record
    """
    return record


def pages(record):
    """
    Convert double hyphen page range to single hyphen,
    eg. '4703--4705' --> '4703-4705'

    :param record: a record
    :type record: dict
    :return: dict -- the modified record
    """
    if 'pages' in record:
        record['pages'] = record['pages'].replace('--', '-')
    return record


if __name__ == '__main__':
    main()
