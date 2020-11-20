from bs4 import BeautifulSoup


def fixindex(doc):
    """
        Remove document title from the index page.
    """
    soup = BeautifulSoup(doc, 'html.parser')
    soup.select_one('h1').extract()

    return str(soup)


def fixbody(doc):
    """
        Generates nicer HTML output.

        <div class="section" id="anchor">
            <h1>title <a class="headerlink" href="#anchor" title="Permalink to this headline">¶</a></h1>
            ...
        </div>
        ====>
        <h1 class="header-permalink" id="anchor"><a href="#anchor" title="Permalink to this headline">title</a></h1>

        Similar to code block captions.
    """
    soup = BeautifulSoup(doc, 'html.parser')

    def fix_permalink(tags, cssclass):
        for t in tags:
            if not t.select_one('a.headerlink'):
                continue

            # Get the anchor and remove it from contents
            anchor = t.select_one('a.headerlink')
            anchor_id = anchor['href'][1:]
            anchor.extract()

            # Remove backref if it was generated
            backref = t.select_one('a.toc-backref')
            if backref:
                backref.unwrap()

            replacement = BeautifulSoup(
                f'<{t.name} class="{cssclass}" id="{anchor_id}">'
                f'<a href="#{anchor_id}" title="Permalink to this headline">{t.string}</a>'
                f'</{t.name}>',
                'html.parser'
            )

            # Remove container and replace header with nicer permalink
            soup.find(id=anchor_id).unwrap()
            t.replace_with(getattr(replacement, t.name))

    fix_permalink(
        soup.find_all([f'h{x}' for x in list(range(1, 7))]),
        'permalink'
    )
    fix_permalink(
        soup.select('.code-block-caption'),
        'permalink code-block-caption'
    )

    return str(soup)


def filter_js(files):
    """
        Remove unwanted javascript files added by sphinx.
    """
    remove_these = [
        '_static/doctools.js',
        '_static/jquery.js',
        '_static/language_data.js',
        '_static/underscore.js',
    ]

    return [f for f in files if f not in remove_these]
