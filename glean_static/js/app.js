/**
 * Paper-Glean Alpine.js stores
 */

document.addEventListener('alpine:init', () => {
    // Main app store for keyboard navigation
    Alpine.data('appStore', () => ({
        selectedPaperIndex: -1,
        papers: [],

        init() {
            // Collect all paper IDs on the page
            this.updatePapers();
            // Watch for HTMX swaps and update paper list
            document.body.addEventListener('htmx:afterSwap', () => {
                this.updatePapers();
            });
        },

        updatePapers() {
            const cards = document.querySelectorAll('[data-paper-id]');
            this.papers = Array.from(cards).map(el => el.dataset.paperId);
        },

        handleKeydown(event) {
            // Don't intercept if user is typing in an input
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.tagName === 'SELECT') {
                // Allow Escape to blur
                if (event.key === 'Escape') {
                    event.target.blur();
                }
                return;
            }

            switch (event.key) {
                case 'j':
                case 'ArrowDown':
                    event.preventDefault();
                    this.navigatePaper(1);
                    break;
                case 'k':
                case 'ArrowUp':
                    event.preventDefault();
                    this.navigatePaper(-1);
                    break;
                case 'o':
                    event.preventDefault();
                    this.openSelectedPaper();
                    break;
                case 'd':
                    event.preventDefault();
                    this.downloadSelectedPaper();
                    break;
                case '/':
                    event.preventDefault();
                    document.querySelector('input[name="search"]')?.focus();
                    break;
                case '1':
                case '2':
                case '3':
                case '4':
                case '5':
                    if (event.shiftKey) {
                        event.preventDefault();
                        this.rateSelectedPaper('curiosity', parseInt(event.key));
                    } else {
                        event.preventDefault();
                        this.rateSelectedPaper('stars', parseInt(event.key));
                    }
                    break;
            }
        },

        navigatePaper(direction) {
            if (this.papers.length === 0) return;

            this.selectedPaperIndex += direction;
            if (this.selectedPaperIndex < 0) this.selectedPaperIndex = 0;
            if (this.selectedPaperIndex >= this.papers.length) this.selectedPaperIndex = this.papers.length - 1;

            const paperId = this.papers[this.selectedPaperIndex];
            const card = document.querySelector(`[data-paper-id="${paperId}"]`);
            if (card) {
                // Remove previous selection
                document.querySelectorAll('[data-paper-id]').forEach(el => el.classList.remove('selected'));
                // Add selection to current
                card.classList.add('selected');
                // Scroll into view
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Load detail panel
                card.click();
            }
        },

        openSelectedPaper() {
            if (this.selectedPaperIndex >= 0) {
                const paperId = this.papers[this.selectedPaperIndex];
                const card = document.querySelector(`[data-paper-id="${paperId}"]`);
                const link = card?.querySelector('a[href*="arxiv.org"]');
                if (link) {
                    window.open(link.href, '_blank');
                }
            }
        },

        downloadSelectedPaper() {
            if (this.selectedPaperIndex >= 0) {
                const paperId = this.papers[this.selectedPaperIndex];
                // Trigger download via HTMX
                htmx.ajax('POST', `/api/download/${paperId}`, { swap: 'none' });
            }
        },

        rateSelectedPaper(kind, rating) {
            if (this.selectedPaperIndex >= 0) {
                const paperId = this.papers[this.selectedPaperIndex];
                const payload = { id: paperId };
                payload[kind] = rating;
                htmx.ajax('POST', '/api/feedback', {
                    values: payload,
                    swap: 'none'
                });
            }
        }
    }));

    // Digest page specific store
    Alpine.data('digestStore', () => ({
        selectedPaperId: null,

        selectPaper(id) {
            this.selectedPaperId = id;
            // Update visual selection
            document.querySelectorAll('[data-paper-id]').forEach(el => {
                el.classList.toggle('selected', el.dataset.paperId === id);
            });
        }
    }));
});

// Add datetime filter for Jinja2
document.addEventListener('DOMContentLoaded', () => {
    // Any initialization that doesn't depend on Alpine
});
