import fnmatch

from bs4 import BeautifulSoup


def _get_top_navigation(soup):
    navs = soup.select('ul')
    if not navs:
        raise ValueError('There is no top navigation!')

    # The top navigation is always the last navigation in the list - this is
    # important to keep sphinx's prev-next links working, otherwise it gets
    # affected by it.
    return navs[-1]


def picktoptoc(doc):
    soup = BeautifulSoup(doc, 'html.parser')

    return str(_get_top_navigation(soup))


def picktoc(doc, path, toc_pattern):
    def match_caption(caption, allowed):
        if caption in allowed:
            return True

        notallowed = [x[1:] for x in filter(lambda x: x.startswith('!'), allowed)]
        if notallowed:
            return caption not in notallowed

        return False

    soup = BeautifulSoup(doc, 'html.parser')

    allowed_captions = []
    for pattern, captions in toc_pattern.items():
        if fnmatch.fnmatchcase(path, pattern):
            allowed_captions = captions
            break

    if not allowed_captions:
        return ''

    # Remove the top navigation
    _get_top_navigation(soup).extract()

    # All navigations must have captions
    toclist = soup.find_all(['p', 'ul'], recursive=False)
    if not toclist:
        return doc

    for caption, nav in zip(*[iter(toclist)]*2):
        if match_caption(caption.string, allowed_captions):
            continue

        caption.extract()
        nav.extract()

    return str(soup)
