import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import time
    from functools import lru_cache
    from urllib.parse import unquote

    import chime
    import marimo as mo
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup

    chime.theme("pokemon")

    DOMAIN_ROOT = "https://en.wiktionary.org"
    CATEGORY_ROOT = "https://en.wiktionary.org/wiki/Category:Borrowed_terms_by_language"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    return (
        BeautifulSoup,
        CATEGORY_ROOT,
        DOMAIN_ROOT,
        headers,
        lru_cache,
        pd,
        requests,
    )


@app.cell
def _(BeautifulSoup, headers, lru_cache, requests):
    @lru_cache
    def get_soup(url):
        #if '%' in url:
        #    url = unquote(url)
        try:
            return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        except Exception as e:
            print(f"Failed to load url {url}")
            raise(e)
    return (get_soup,)


@app.cell
def _(CATEGORY_ROOT, get_soup):
    soup = get_soup(CATEGORY_ROOT)
    return


@app.cell
def _(get_soup):
    def get_next_page_urls(url):
        result = [url]
        try:
            soup = get_soup(url)
        except:
            return result
        
        next_page_links = [a for a in soup.find_all("a") if a.text=="next page"]

        while len(next_page_links) > 0:
            next_url = "https://en.wiktionary.org" + next_page_links[-1].attrs["href"]
            result.append(next_url)
            try:
                soup = get_soup(next_url)
            except:
                return result
            next_page_links = [a for a in soup.find_all("a") if a.text=="next page"]

        return result
    
    return (get_next_page_urls,)


@app.cell
def _(DOMAIN_ROOT, get_soup):
    def get_category_item_urls(url):
        try:
            soup = get_soup(url)
        except:
            return []
        return [DOMAIN_ROOT + div.find_all("a")[-1].attrs["href"] for div in soup.find_all("div", class_="CategoryTreeItem")]
    return (get_category_item_urls,)


@app.cell
def _(CATEGORY_ROOT, get_next_page_urls):
    get_next_page_urls(CATEGORY_ROOT)
    return


@app.cell
def _(CATEGORY_ROOT, get_category_item_urls):
    get_category_item_urls(CATEGORY_ROOT)
    return


@app.cell
def _(CATEGORY_ROOT, get_category_item_urls, get_next_page_urls):
    urls = [[get_next_page_urls(level2_url) for level2_url in get_category_item_urls(level1_url)] for level1_url in get_next_page_urls(CATEGORY_ROOT)]
    return (urls,)


@app.cell
def _(urls):
    level3_categories = [level3 for page in urls for level2 in page for level3 in level2 if level3.endswith('borrowed_terms')]
    return (level3_categories,)


@app.cell
def _(get_category_item_urls, level3_categories):
    level4_categories = {level3.split(":")[-1]: get_category_item_urls(level3) for level3 in level3_categories}
    return (level4_categories,)


@app.cell
def _(level4_categories, pd):
    pd.Series({k: len(v) for k,v in level4_categories.items()}).sort_values(ascending=False)
    return


if __name__ == "__main__":
    app.run()
