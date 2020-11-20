function CodeTabs() {}

CodeTabs.prototype.init = function() {
    /* Move labels to one container. */
    $('.code-tabs').each($.proxy(function (_, el) {
        el = $(el);

        /* Create container to hold the labels and move them. */
        var container = $('<div class="code-tabs-labels"></div>');
        var dest = el.find('.code-tabs-caption')
        if (dest.length) {
            dest.after(container);
        } else {
            el.prepend(container);
        }

        el.find('.code-tab-label').detach().appendTo(container);

        /* Select the first label. */
        var label = container.children().first().data('label');
        this.select(el, label);
    }, this));

    /* Select label across all code-tabs on click. */
    $('.code-tab-label').click($.proxy(function (event) {
        var label = $(event.target).data('label');
        $('.code-tabs').each($.proxy(function (_, el) {
            this.select($(el), label);
        }, this));
    }, this));
}

CodeTabs.prototype.select = function(ct, label) {
    var els = ct.find('[data-label="' + label + '"]');
    if (!els.length) {
        /* Nothing to do. This code-tabs do not contain desired label. */
        return;
    }

    ct.find('.code-tab-label, .code-tab').removeClass('active');
    els.addClass('active');
}

var codetabs = new CodeTabs();

$(document).ready(function () {
    codetabs.init();
});
