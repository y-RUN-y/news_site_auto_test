"""Explore home page more thoroughly - tabs, interactions"""
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://news.qq.com/omn/author/8QMc339c6YMcuD%2Fb5Qdz', timeout=30000, wait_until='load')
    page.wait_for_timeout(8000)
    
    print("=== URL ===")
    print(page.url)
    
    # Get all role="tab" and other tab-like elements
    tabs_info = page.evaluate("""() => {
        const results = [];
        // Find all tab-like elements
        const tabSelectors = ['[role="tab"]', '[class*="tab"]', '[class*="Tab"]'];
        tabSelectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    results.push({
                        tag: el.tagName,
                        selector: sel,
                        class: el.className,
                        text: (el.textContent || '').trim().substring(0, 100),
                        href: el.getAttribute('href') || '',
                        role: el.getAttribute('role') || '',
                    });
                }
            });
        });
        return results;
    }""")
    
    print("\n=== TAB ELEMENTS ===")
    for t in tabs_info:
        print(f"  tag={t['tag']} class='{t['class']}' text='{t['text']}' href='{t['href']}'")
    
    # Look for the tab bar specifically inside author-article-info
    tab_bar = page.evaluate("""() => {
        const container = document.querySelector('.author-article-info');
        if (!container) return null;
        const firstDiv = container.children[0];
        return {
            class: firstDiv ? firstDiv.className : '',
            tag: firstDiv ? firstDiv.tagName : '',
            html: firstDiv ? firstDiv.outerHTML.substring(0, 2000) : ''
        };
    }""")
    print("\n=== AUTHOR-ARTICLE-INFO FIRST CHILD ===")
    print(json.dumps(tab_bar, ensure_ascii=False, indent=2))
    
    # Get the full tab area HTML
    tab_html = page.evaluate("""() => {
        const el = document.querySelector('.author-article-info');
        if (!el) return '';
        return el.innerHTML.substring(0, 5000);
    }""")
    print("\n=== AUTHOR-ARTICLE-INFO HTML ===")
    print(tab_html)
    
    # Try to click different tabs and observe URL changes
    # First, find all clickable tab elements
    tab_links = page.evaluate("""() => {
        const container = document.querySelector('.author-article-info');
        if (!container) return [];
        const links = container.querySelectorAll('a, [role="tab"], span[class*="tab"]');
        return Array.from(links).map(el => ({
            tag: el.tagName,
            class: el.className,
            text: el.textContent.trim().substring(0, 50),
            href: el.getAttribute('href') || '',
        }));
    }""")
    print("\n=== TAB LINKS ===")
    for l in tab_links:
        print(f"  {l['tag']} class='{l['class']}' text='{l['text']}' href='{l['href']}'")
    
    # Get author stats structure
    stats_html = page.evaluate("""() => {
        const el = document.querySelector('.author-info-data');
        if (!el) return '';
        return el.outerHTML.substring(0, 2000);
    }""")
    print("\n=== AUTHOR STATS HTML ===")
    print(stats_html)
    
    # Get author basic info structure
    basic_info_html = page.evaluate("""() => {
        const el = document.querySelector('.author-basic-info');
        if (!el) return '';
        return el.outerHTML.substring(0, 3000);
    }""")
    print("\n=== AUTHOR BASIC INFO HTML ===")
    print(basic_info_html)
    
    browser.close()
