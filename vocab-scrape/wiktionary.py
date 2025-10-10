import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import time
    import chime
    from gazpacho import Soup
    from rich.console import Console
    import pandas as pd
    import marimo as mo

    from functools import lru_cache

    chime.theme("pokemon")
    console = Console()
    return Soup, lru_cache


@app.cell
def _(Soup, lru_cache):
    @lru_cache
    def get_soup(url):
        return Soup.get(url)
    return (get_soup,)


@app.cell
def _(get_soup):
    def get_next_page_urls(url):
        result = [url]
        soup = get_soup(url)
        next_page_links = [a for a in soup.find("a") if a.text=="next page"]

        while len(next_page_links) > 0:
            next_url = "https://en.wiktionary.org" + next_page_links[-1].attrs["href"]
            result.append(next_url)
            soup = get_soup(next_url)
            next_page_links = [a for a in soup.find("a") if a.text=="next page"]

        return result
    
    return (get_next_page_urls,)


@app.cell
def _(get_next_page_urls):
    get_next_page_urls("https://en.wiktionary.org/wiki/Category:Borrowed_terms_by_language")
    return


@app.cell
def _(get_soup):
    root = get_soup("https://en.wiktionary.org/wiki/Category:Borrowed_terms_by_language")
    return (root,)


@app.cell
def _(root):
    [div.find("a")[-1] for div in root.find("div", {"class": "CategoryTreeItem"})]
    return


@app.cell
def _(root):
    [a for a in root.find("a") if a.text=="next page"][0].attrs['href']
    return


if __name__ == "__main__":
    app.run()
