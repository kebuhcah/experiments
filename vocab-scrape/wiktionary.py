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
    from gazpacho import Soup, utils
    from rich.console import Console

    chime.theme("pokemon")
    console = Console()

    DOMAIN_ROOT = "https://en.wiktionary.org"
    CATEGORY_ROOT = "https://en.wiktionary.org/wiki/Category:Borrowed_terms_by_language"
    return CATEGORY_ROOT, DOMAIN_ROOT, Soup, lru_cache, unquote, utils


@app.cell
def _(Soup, lru_cache, unquote):
    @lru_cache
    def get_soup(url):
        if '%' in url:
            url = unquote(url)
        try:
            return Soup.get(url)
        except Exception as e:
            print(f"Failed to load url {url}")
            raise(e)
    return (get_soup,)


@app.cell
def _(get_soup, utils):
    def get_next_page_urls(url):
        result = [url]
        try:
            soup = get_soup(url)
        except utils.HTTPError:
            return result
        
        next_page_links = [a for a in soup.find("a") if a.text=="next page"]

        while len(next_page_links) > 0:
            next_url = "https://en.wiktionary.org" + next_page_links[-1].attrs["href"]
            result.append(next_url)
            try:
                soup = get_soup(next_url)
            except utils.HTTPError:
                return result
            next_page_links = [a for a in soup.find("a") if a.text=="next page"]

        return result
    
    return (get_next_page_urls,)


@app.cell
def _(DOMAIN_ROOT, get_soup, utils):
    def get_category_item_urls(url):
        try:
            soup = get_soup(url)
        except utils.HTTPError:
            return []
        return [DOMAIN_ROOT + div.find("a")[-1].attrs["href"] for div in soup.find("div", {"class": "CategoryTreeItem"})]
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
    return


@app.cell
def _(root):
    [a for a in root.find("a") if a.text=="next page"][0].attrs['href']
    return


if __name__ == "__main__":
    app.run()
