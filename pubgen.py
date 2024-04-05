#!/usr/bin/python3

import io
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

with open('publications.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

parser = BibTexParser()
parser.ignore_nonstandard_types = True
parser.homogenise_fields = True

bib_database = bibtexparser.loads(bibtex_str, parser).entries

preprint = list(
    filter(lambda x: 'note' in x and 'Review' in x['note'], bib_database))

bib_database = list(filter(lambda x: x not in preprint, bib_database))
bib_database.sort(key=lambda x: x['year'], reverse=True)

journals = filter(lambda x: x['ENTRYTYPE'] == 'article', bib_database)
books = filter(lambda x: x['ENTRYTYPE'] == 'inbook', bib_database)
conferences = filter(
    lambda x: x['ENTRYTYPE'] == 'inproceedings' or x['ENTRYTYPE'] ==
    'incollection', bib_database)
thesis = filter(lambda x: 'thesis' in x['ENTRYTYPE'], bib_database)

from yattag import Doc

doc, tag, text = Doc().tagtext()


def processAuthors(authors):
    global doc, tag, text
    authors = authors.split(' and ')
    if len(authors) > 1:
        for i, author in enumerate(authors):
            if '*' in author:
                author = author.replace('*', '')
                author = author.strip()

            if 'Zachary' in author:
                with tag('nobr'):
                    with tag('b'):
                        text(author)
            else:
                author = author.replace("{\\'a}", 'aacute;')
                with tag('nobr'):
                    text(author)
            if i < len(authors) - 1:
                text(', ')
            if i == len(authors) - 2:
                text('and ')
    else:
        with tag('b'):
            text(authors[0])


def formatArchive(archive, label=""):
    global doc, tag, text

    archive = list(archive)
    high = len(archive)

    year = None

    for num, entry in enumerate(archive):
        with tag('a', klass="anchor", id=entry['ID']):
            pass

        with tag('dl', klass="row"):
            if not year or year != entry['year']:
                year = entry['year']
                with tag('h3', klass="col-lg-12 col-xl-1"):
                    text(year)

            else:
                with tag('div', klass="col-lg-12 col-xl-1"):
                    pass

            with tag('dt', klass="col-1", style="text-align:right;"):
                text('{:s}{:d}.'.format(label, high - num))

            with tag('dd', klass="col-md-11 col-xl-10"):
                with tag('p'):
                    if 'chapter' in entry:
                        with tag('font', klass='title'):
                            text(entry['chapter'] + ", ")
                        with tag('font', klass='book'):
                            text(entry['title'])
                    else:
                        with tag('font', klass='title'):
                            text(entry['title'])
                    with tag('br'):
                        processAuthors(entry['author'])

                    if 'note' in entry:
                        text(" ({})".format(entry['note']))

                with tag('p'):
                    with tag('a',
                             href="#{}bibtex".format(entry['ID']),
                             data_toggle="collapse"):
                        text('Bibtex')

                    if 'abstract' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a',
                                 href="#{}abstract".format(entry['ID']),
                                 data_toggle="collapse"):
                            text('Abstract')

                    if 'pdf' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a', href=entry['pdf']):
                            with tag('i', klass="fa fa-file-pdf"):
                                pass
                            text(' PDF')

                    if 'doi' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a',
                                 href='https://doi.org/{}'.format(
                                     entry['doi'])):
                            with tag('i', klass="ai ai-doi"):
                                pass
                            text(' Publisher')

                    if 'url' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a', href=entry['url']):
                            with tag('i', klass="fa fa-link"):
                                pass
                            text(' Publisher')

                    if 'video' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a',
                                 href="#{}video".format(entry['ID']),
                                 data_toggle="collapse"):
                            with tag('i', klass="fa fa-video"):
                                pass
                            text(' Video')

                    if 'youtube' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a', href=entry['youtube']):
                            with tag('i', klass="fa fa-video"):
                                pass
                            text(' Video')

                    if 'talk' in entry:
                        with tag('b'):
                            text(' / ')
                        with tag('a', href=entry['talk']):
                            with tag('i', klass="fa fa-video"):
                                pass
                            text(' Talk')

                if 'abstract' in entry:
                    with tag('div',
                             id="{}abstract".format(entry['ID']),
                             klass="collapse"):
                        with tag('div', klass="well"):
                            with tag('p'):
                                text(entry['abstract'])
                        with tag('br'):
                            with tag('p'):
                                with tag('a',
                                         href="#{}abstract".format(
                                             entry['ID']),
                                         data_toggle="collapse"):
                                    text('Close')

                with tag('div',
                         id="{}bibtex".format(entry['ID']),
                         klass="collapse"):
                    with tag('div', klass="well"):
                        with tag('pre'):
                            db = BibDatabase()
                            entry2 = {k: v for k, v in entry.items()}
                            entry2['author'] = entry2['author'].replace(
                                '*', '')
                            entry2.pop('abstract', None)
                            entry2.pop('video', None)
                            entry2.pop('pdf', None)
                            entry2.pop('talk', None)
                            entry2.pop('note', None)
                            db.entries = [entry2]
                            text(bibtexparser.dumps(db)[:-1])
                        with tag('br'):
                            with tag('p'):
                                with tag('a',
                                         href="#{}bibtex".format(entry['ID']),
                                         data_toggle="collapse"):
                                    text('Close')

                if 'video' in entry:
                    content = entry['video']
                    with tag('div',
                             id="{}video".format(entry['ID']),
                             klass="collapse"):
                        with tag('div', klass="well"):
                            with tag(
                                    'div',
                                    klass=
                                    "embed-responsive embed-responsive-16by9"):
                                if "vimeo" in content:
                                    doc.asis(content)
                                else:
                                    with tag('video',
                                             klass="embed-responsive-item",
                                             preload="none"):
                                        with tag('source',
                                                 src=entry['video'],
                                                 type='video/webm'):
                                            pass
                            with tag('br'):
                                with tag('p'):
                                    with tag('a',
                                             href="#{}video".format(
                                                 entry['ID']),
                                             data_toggle="collapse"):
                                        text('Close')


with tag('a', id="publications", klass="anchor"):
    pass
with tag('h1'):
    text('Publications')
with tag('div', style="padding: 10px"):

    # Pre-prints

    if len(preprint):
        with tag('a', id="preprints", klass="anchor"):
            pass
        with tag('h2'):
            text('Preprints')

        with tag('div'):
            formatArchive(preprint, 'P')

    # Journals
    with tag('a', id="journals", klass="anchor"):
        pass
    with tag('h2'):
        text('Peer-Reviewed Journal Articles')

    with tag('div'):
        formatArchive(journals, 'J')

    # Conferences
    with tag('a', id="conference", klass="anchor"):
        pass
    with tag('h2'):
        text('Peer-Reviewed Conference Papers')

    with tag('div'):
        formatArchive(conferences, 'C')

    # Books
    with tag('a', id="bookchapters", klass="anchor"):
        pass
    with tag('h2'):
        text('Book Chapters')

    with tag('div'):
        formatArchive(books, 'B')

    # Thesis
    # with tag('a', id="theses", klass="anchor"):
    #     pass
    # with tag('h2'):
    #     text('Theses')

    # with tag('div'):
    #     formatArchive(thesis, 'T')

result = doc.getvalue()
result = result.replace('data_toggle', 'data-toggle')
result = result.replace('<video', '<video controls')
result = result.replace("aacute;", '&aacute;')

with io.open('index.in.html', mode='r') as f:
    result = f.read().replace('@publications@', result)
    with io.open('index.html', mode='w', encoding="utf-8") as i:
        i.write(result)
