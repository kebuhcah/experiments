"""
Wiktionary Etymology Scraper

A reusable module for scraping etymological terms (borrowed and derived) from Wiktionary.
Supports scraping category hierarchies and extracting term URLs for linguistic analysis.
"""

import json
import time
from functools import lru_cache
from typing import Dict, List, Optional
from urllib.parse import unquote

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Constants
DOMAIN_ROOT = "https://en.wiktionary.org"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

# Default root categories for different term types
DEFAULT_ROOTS = {
    "borrowed": "https://en.wiktionary.org/wiki/Category:Borrowed_terms_by_language",
    "derived": "https://en.wiktionary.org/wiki/Category:Terms_derived_from_other_languages_by_language"
}


@lru_cache(maxsize=1000)
def get_soup(url: str) -> BeautifulSoup:
    """
    Fetch and parse HTML from a URL using BeautifulSoup.

    Uses LRU cache to avoid redundant requests for the same URL.

    Args:
        url: The URL to fetch

    Returns:
        BeautifulSoup object containing parsed HTML

    Raises:
        Exception: If the request fails
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Failed to load url {url}")
        raise e


def get_next_page_urls(url: str) -> List[str]:
    """
    Follow pagination links to collect all page URLs in a category.

    Wiktionary uses "next page" links to paginate large categories.
    This function follows all pagination links to collect the complete list.

    Args:
        url: The starting category URL

    Returns:
        List of all page URLs including the starting URL
    """
    result = [url]

    try:
        soup = get_soup(url)
    except:
        return result

    next_page_links = [a for a in soup.find_all("a") if a.text == "next page"]

    while len(next_page_links) > 0:
        next_url = DOMAIN_ROOT + next_page_links[-1].attrs["href"]
        result.append(next_url)

        try:
            soup = get_soup(next_url)
        except:
            return result

        next_page_links = [a for a in soup.find_all("a") if a.text == "next page"]

    return result


def get_category_item_urls(url: str) -> List[str]:
    """
    Extract subcategory URLs from a category page.

    Wiktionary uses CategoryTreeItem divs to display subcategories.
    This extracts the links from these elements.

    Args:
        url: The category page URL

    Returns:
        List of subcategory URLs
    """
    try:
        soup = get_soup(url)
    except:
        return []

    items = soup.find_all("div", class_="CategoryTreeItem")
    return [DOMAIN_ROOT + div.find_all("a")[-1].attrs["href"] for div in items]


def get_category_term_urls(url: str) -> List[str]:
    """
    Extract term/word URLs from a category page.

    Terms are displayed in mw-category-group divs. This function extracts
    the links from the last such div (which contains the actual terms).

    Args:
        url: The category page URL

    Returns:
        List of term URLs
    """
    try:
        soup = get_soup(url)
    except:
        return []

    category_divs = soup.find_all("div", class_="mw-category-group")

    if len(category_divs) == 0:
        return []

    # Last div contains the actual terms
    return [DOMAIN_ROOT + a.attrs.get("href", "ERROR")
            for a in category_divs[-1].find_all("a")]


def scrape_etymological_terms(
    category_type: str = "borrowed",
    root_category_url: Optional[str] = None,
    save_path: Optional[str] = None,
    verbose: bool = True
) -> Dict[str, List[str]]:
    """
    Scrape etymological terms (borrowed or derived) from Wiktionary.

    This function navigates through Wiktionary's category hierarchy to find
    all terms of a specific etymological type (borrowed or derived) and their
    source languages.

    The category hierarchy is:
    - Level 1: Root category (e.g., "Borrowed_terms_by_language")
    - Level 2: Language categories (e.g., "English_borrowed_terms")
    - Level 3: Language pair categories (e.g., "English_terms_borrowed_from_French")
    - Level 4: Individual term pages

    Args:
        category_type: Either "borrowed" or "derived"
        root_category_url: Optional override for root category URL
        save_path: Optional path to save JSON results
        verbose: Whether to show progress bars

    Returns:
        Dictionary mapping category names to lists of term URLs
        Example: {
            "English_terms_borrowed_from_French": [
                "https://en.wiktionary.org/wiki/restaurant",
                "https://en.wiktionary.org/wiki/cafe",
                ...
            ],
            ...
        }

    Raises:
        ValueError: If category_type is not "borrowed" or "derived"
    """
    # Validate category type
    if category_type not in ["borrowed", "derived"]:
        raise ValueError(f"category_type must be 'borrowed' or 'derived', got '{category_type}'")

    # Set root category URL
    if root_category_url is None:
        root_category_url = DEFAULT_ROOTS[category_type]

    if verbose:
        print(f"Scraping {category_type} terms from: {root_category_url}\n")

    # Step 1: Get all pages at the root level (Level 1)
    if verbose:
        print("Step 1: Collecting root category pages...")
    level1_pages = get_next_page_urls(root_category_url)
    if verbose:
        print(f"  Found {len(level1_pages)} page(s)\n")

    # Step 2: Get all language categories (Level 2)
    if verbose:
        print("Step 2: Collecting language categories...")
    level2_categories = []
    for level1_url in tqdm(level1_pages, disable=not verbose, desc="Level 1 pages"):
        level2_urls = []
        for page_url in get_next_page_urls(level1_url):
            level2_urls.extend(get_category_item_urls(page_url))
        level2_categories.append(level2_urls)
    if verbose:
        total_level2 = sum(len(cats) for cats in level2_categories)
        print(f"  Found {total_level2} language categorie(s)\n")

    # Step 3: Filter for language-pair categories (Level 3)
    if verbose:
        print("Step 3: Collecting language-pair categories...")

    # Flatten level2 and expand all pages
    all_level3_urls = []
    for level2_list in level2_categories:
        for level2_url in level2_list:
            all_level3_urls.extend(get_next_page_urls(level2_url))

    # Filter for categories that end with the appropriate pattern
    filter_pattern = f"{category_type}_terms"
    level3_categories = [url for url in all_level3_urls if url.endswith(filter_pattern)]

    if verbose:
        print(f"  Found {len(level3_categories)} language-pair categorie(s)\n")

    # Step 4: Collect all language-pair category pages and their subcategories (Level 4)
    if verbose:
        print("Step 4: Expanding language-pair categories to find all subcategories...")

    level4_categories = {}
    split_pattern = f"_terms_{category_type}_from_"

    for level3_url in tqdm(level3_categories, disable=not verbose, desc="Language pairs"):
        level4_urls = []
        next_pages = get_next_page_urls(level3_url)
        for page in next_pages:
            level4_urls.extend(get_category_item_urls(page))

        # Extract category name from URL
        category_name = level3_url.split(":")[-1]
        level4_categories[category_name] = level4_urls

    # Flatten level4 categories
    level4_categories_flat = [url for urls in level4_categories.values() for url in urls]

    if verbose:
        print(f"  Found {len(level4_categories_flat)} subcategorie(s)\n")

    # Step 5: Extract terms from categories
    if verbose:
        print("Step 5: Extracting terms from categories...")

    terms_dict = {}

    # Process both level3 (direct term categories) and level4 (subcategories)
    all_categories_to_process = list(level3_categories) + level4_categories_flat

    for category_url in tqdm(all_categories_to_process, disable=not verbose, desc="Extracting terms"):
        # Only process categories with the correct pattern
        if split_pattern not in category_url:
            continue

        term_urls = []
        category_pages = get_next_page_urls(category_url)

        for category_page in category_pages:
            results = get_category_term_urls(category_page)
            term_urls.extend(results)

        # Extract category name from URL
        category_name = category_url.split(":")[-1]

        if term_urls:  # Only add if we found terms
            terms_dict[category_name] = term_urls

    if verbose:
        total_terms = sum(len(urls) for urls in terms_dict.values())
        print(f"\nDone! Collected {len(terms_dict)} categories with {total_terms} total terms")

    # Save to JSON if requested
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(terms_dict, f, indent=2, ensure_ascii=False)
        if verbose:
            print(f"Saved results to: {save_path}")

    return terms_dict


def load_terms_from_json(file_path: str) -> Dict[str, List[str]]:
    """
    Load previously scraped terms from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary mapping category names to lists of term URLs
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_language_heatmap(
    terms_dict: Dict[str, List[str]],
    category_type: str = "borrowed",
    top_n: int = 50
):
    """
    Create a heatmap showing term flow between languages.

    For borrowed terms, this shows which languages (debtors) borrowed terms
    from which other languages (creditors).

    For derived terms, this shows which languages (recipients) have terms
    derived from which other languages (sources).

    Args:
        terms_dict: Dictionary from scrape_etymological_terms()
        category_type: "borrowed" or "derived" (affects axis labels)
        top_n: Number of top languages to include (default 50)

    Returns:
        Styled pandas DataFrame for visualization with log-scaled color gradient
    """
    # Determine split pattern and labels based on category type
    if category_type == "borrowed":
        split_pattern = "_terms_borrowed_from_"
        row_label = "debtor"
        col_label = "creditor"
    elif category_type == "derived":
        split_pattern = "_terms_derived_from_"
        row_label = "recipient"
        col_label = "source"
    else:
        raise ValueError(f"category_type must be 'borrowed' or 'derived', got '{category_type}'")

    # Create a Series with term counts per category
    term_counts = pd.Series({k: len(v) for k, v in terms_dict.items()})

    # Build the heatmap data
    df = (term_counts
          .sort_values(ascending=False)
          .rename("terms")
          .rename_axis("category")
          .reset_index()
          # Extract language pairs
          .assign(**{row_label: lambda x: (x.category
                                           .str.split(split_pattern).str[0]
                                           .apply(unquote)
                                           .str.replace("_", " "))})
          .assign(**{col_label: lambda x: (x.category
                                           .str.split(split_pattern).str[-1]
                                           .apply(unquote)
                                           .str.replace("_", " "))})
          # Create pivot table
          .set_index([row_label, col_label])
          .terms
          .unstack(fill_value=0)
          )

    # Get top N languages by total (row sums)
    df_with_row_totals = df.assign(total=lambda x: x.sum(axis=1)).sort_values("total", ascending=False)
    top_rows = df_with_row_totals.head(top_n).index

    # Get top N languages by total (column sums)
    df_with_col_totals = df.T.assign(total=lambda x: x.sum(axis=1)).sort_values("total", ascending=False)
    top_cols = df_with_col_totals.head(top_n).index

    # Filter to top N x top N
    df_filtered = df.loc[top_rows, top_cols]

    # Apply styling with log scale
    styled = (df_filtered
              .fillna(0).astype(int)
              .style.background_gradient(
                  cmap="viridis",
                  vmin=0,
                  axis=None,
                  gmap=df_filtered.fillna(1).astype(int).pipe(np.log)
              )
              .set_table_styles([
                  dict(selector='th', props=[('text-align', 'center')]),
                  dict(selector='td', props=[('text-align', 'center')])
              ]))

    return styled


if __name__ == "__main__":
    # Example usage
    print("Example: Scraping borrowed terms")
    borrowed = scrape_etymological_terms(
        category_type="borrowed",
        save_path="borrowed_terms_test.json"
    )
    print(f"\nFound {len(borrowed)} categories")
    print("\nSample categories:")
    for i, (cat, urls) in enumerate(list(borrowed.items())[:5]):
        print(f"  {cat}: {len(urls)} terms")
