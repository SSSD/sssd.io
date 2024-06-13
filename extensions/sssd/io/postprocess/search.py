
import glob
import json

from bs4 import BeautifulSoup


def _parse_page(path):
    with open(path) as f:
        soup = BeautifulSoup(f, 'html.parser')

    searchable = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6̈́', 'p', 'li']
    selectors = [f'#page-content article {x}' for x in searchable]

    s_title = soup.select_one('#page-content article h1')
    s_hunks = soup.select(', '.join(selectors))

    if s_title is None:
        return (None, None)

    title = s_title.text
    hunk = '\n'.join([x.text for x in s_hunks])

    return (title, hunk)


def _build_index(docs):
    index = {
        'docs': [],  # Contains pairs: [path, title]
        'hunks': [],
    }

    for i, doc in enumerate(docs):
        index['docs'].append([doc['path'], doc['title']])
        index['hunks'].append(doc['hunk'])

    return index


def build_search_index(app, exception):
    if exception is not None or app.builder.name != 'html':
        return

    print("Postprocess: Generating search index")

    build_dir = app.builder.outdir
    exclude_pages = [
        'community.html',
        'contents.html',
        'example.html',
        'genindex.html',
        'index.html',
        'search.html',
    ]

    docs = []
    for path in glob.glob(f'{build_dir}/**/*.html', recursive=True):
        relpath = path[len(str(build_dir)) + 1:]
        if relpath in exclude_pages:
            continue

        (title, hunk) = _parse_page(path)
        if not title:
            continue

        docs.append({'path': relpath, 'title': title, 'hunk': hunk})

    index = _build_index(docs)
    serialized = json.dumps(index, separators=(',', ':'))
    for key in index.keys():
        serialized = serialized.replace(f'"{key}":', f'{key}:', 1)

    with open(f'{build_dir}/_static/scripts/search-index.js', 'w') as f:
        f.write(f'search.setIndex({serialized})')

    print("Postprocess: Search index generated successfully")
