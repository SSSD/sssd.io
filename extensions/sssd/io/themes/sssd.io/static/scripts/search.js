function SearchResult(doc_path, doc_title, doc_content, score) {
    this.path = doc_path;
    this.title = doc_title;
    this.content = doc_content;
    this.score = score;
}

function Search() {
    this.index = null;
    this.wade = null;
    this.onready = null;
}

Search.prototype.setIndex = function(index) {
    this.index = index;
    this.wade = Wade(index.hunks);

    this.executeReadyCallback();
}

Search.prototype.query = function(query) {
    var results = this.wade(query);

    results.sort(function(a, b) {
        return b.score - a.score;
    });

    var search_results = []
    for (var i = 0; i < results.length; i++) {
        var docid = results[i].index;
        search_results[i] = new SearchResult(
            this.index.docs[docid][0],
            this.index.docs[docid][1],
            this.index.hunks[docid],
            results[i].score
        )
    }

    return search_results;
}

Search.prototype.executeReadyCallback = function() {
    if (this.index === null || this.onready === null) {
        /* Not ready yet. */
        return;
    }

    this.onready();
    this.onready = null;
}

Search.prototype.whenReady = function (onReadyCallback) {
    this.onready = onReadyCallback;
    this.executeReadyCallback();
}

function SearchUI(search, limit) {
    this.search = search;
    this.root = null;
    this.el = {overlay: null, field: null, container: null, results: null};
    this.active = 0;
    this.count = 0;
    this.limit = limit;

    if (!this.search) {
        console.error('Search object is not set!');
    }
}

SearchUI.prototype.init = function(input_field, results_container, overlay, root_url) {
    this.root = root_url;
    this.el.overlay = overlay;
    this.el.field = input_field;
    this.el.container = results_container;
    this.el.results = results_container.find('ul');

    if (!this.el.overlay.length || !this.el.field.length || !this.el.container.length || !this.el.results.length) {
        console.error('Required DOM objects do not exist!');
        console.error(this.el);
        return;
    }

    this.hide();
    this.setResults([]);

    /* Show results when we focus the search text field. */
    this.el.field.focus($.proxy(this.show, this));

    /* Disable pressing UP and DOWN on the filed to enable keyboard navigation
     * on the results. Otherwise it will function as HOME and END. */
    this.el.field.keydown(function (event) {
        if (event.keyCode == 38 /* UP */ || event.keyCode == 40 /* DOWN */) {
            event.preventDefault();
        }
    });

    /* Search as you type. */
    this.el.field.keyup($.proxy(this.query, this));
};

SearchUI.prototype.show = function() {
    if (this.el.results.is(':visible')) {
        return;
    }

    this.el.overlay.show();
    this.el.results.show();
    this.el.results.addClass('active');
    this.el.field.addClass('active');
    this.el.overlay.addClass('active');

    /* Setup keyboard navigation. */
    $(document).on('keyup.search', $.proxy(this.onKeyboardNavigation, this));

    /* Close container when clicked outside the box. */
    $(document).on('mouseup.search', $.proxy(this.onCloseOnClick, this));
}

SearchUI.prototype.hide = function() {
    function duration(el) {
        return parseFloat(el.css('transition-duration')) * 1000;
    }

    this.el.overlay.removeClass('active');
    this.el.field.removeClass('active');
    this.el.results.removeClass('active');
    this.el.results.delay(duration(this.el.results)).hide(0);
    this.el.overlay.delay(duration(this.el.overlay)).hide(0);

    /* Remove event handlers. */
    $(document).off('mouseup.search');
    $(document).off('keyup.search');
}

SearchUI.prototype.onKeyboardNavigation = function(event) {
    switch (event.keyCode) {
        case 27: /* Escape */
            this.hide();
            return;

        case 13: /* Enter */
            if (this.active <= 0) {
                return;
            }

            this.el.results.find('.active a')[0].click();
            break;

        case 38: // up
            if (this.active <= 1) {
                this.active = this.count;
            } else {
                this.active--;
            }

            this.markActive();
            break;

        case 40: // down
            if (this.active >= this.count) {
                if (this.count > 0) {
                    this.active = 1;
                }
            } else {
                this.active++;
            }

            this.markActive();
            break;
    }

    event.preventDefault();
}

SearchUI.prototype.onCloseOnClick = function(event) {
    if (this.el.results.is(event.target) || this.el.field.is(event.target)) {
        return;
    }

    if (this.el.results.has(event.target).length) {
        return;
    }

    this.hide();
}

SearchUI.prototype.markActive = function() {
    var items = this.el.results.find('li')

    items.removeClass('active');
    if (this.active > 0 && this.active <= this.count) {
        items.eq(this.active - 1).addClass('active');
    }
}

SearchUI.prototype.query = function() {
    this.search.whenReady($.proxy(function () {
        var needle = this.el.field.val();
        if (!needle) {
            this.setResults([]);
            return;
        }

        this.setResults(this.search.query(needle));
    }, this))
}

SearchUI.prototype.setResults = function(results) {
    results = results.slice(0, this.limit - 1);

    items = '';
    for (var  i = 0; i < results.length; i++) {
        var r = results[i];
        items += '<li><a href="' + this.root + r.path + '">' + r.title + '</a></li>';
    }

    if (!items) {
        items = '<li class="search-no-results">No results found.</li>';
    }

    this.el.results.html(items);
    this.count = results.length;

    if (this.active > this.count) {
        this.active = this.count;
    }

    this.markActive();
}

var search = new Search();
var searchui = new SearchUI(search, 10);

$(document).ready(function () {
    searchui.init(
        $('#search-field'),
        $('#search-results'),
        $('#overlay'),
        $('script[data-root]').attr('data-root')
    );
});
