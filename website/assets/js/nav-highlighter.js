'use strict';

import { $, $$ } from './util.js';

export default class NavHighlighter {
    /**
     * Hightlight section in viewport in sidebar, using in-view library.
     * @param {string} sectionAttr - Data attribute of sections.
     * @param {string} navAttr - Data attribute of navigation items.
     * @param {string} activeClass – Class name of active element.
     */
    constructor(sectionAttr, navAttr, activeClass = 'is-active') {
        this.sections = [...$$(`[${navAttr}]`)];
        this.navAttr = navAttr;
        this.sectionAttr = sectionAttr;
        this.activeClass = activeClass;
        if (window.inView) inView(`[${sectionAttr}]`)
            .on('enter', this.highlightSection.bind(this));
    }

    /**
     * Check if section in view exists in sidebar and mark as active.
     * @param {node} section - The section in view.
     */
    highlightSection(section) {
        const id = section.getAttribute(this.sectionAttr);
        const el = $(`[${this.navAttr}="${id}"]`);
        if (el) {
            this.sections.forEach(el => el.classList.remove(this.activeClass));
            el.classList.add(this.activeClass);
        }
    }
}
