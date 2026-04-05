"""
Fix canonical duplication & add hreflang tags across all HTML pages.

This script:
1. Fixes EN pages canonical/og:url/twitter:url to point to themselves (not ES)
2. Adds hreflang tags (es, en, x-default) to ALL pages
3. Fixes structured data URLs on EN pages
"""

import re
import os

BASE = "https://zisquito.github.io"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Map of ES page slug -> EN page slug (extensionless, relative to site root)
PAGE_PAIRS = {
    "sobre-mi": "en/sobre-mi",
    "blog": "en/blog",
    "contacto": "en/contacto",
    "articulos/auditoria-seo": "en/articulos/auditoria-seo",
    "articulos/herramientas-analitica": "en/articulos/herramientas-analitica",
    "articulos/unibite": "en/articulos/unibite",
    "articulos/que-es-cro": "en/articulos/que-es-cro",
    "articulos/optimizacion-seo-wordpress": "en/articulos/optimizacion-seo-wordpress",
    "articulos/agentes-ia-mcp": "en/articulos/agentes-ia-mcp",
    "articulos/el-dilema-del-checkout": "en/articulos/el-dilema-del-checkout",
}

# Reverse map: EN slug -> ES slug
EN_TO_ES = {v: k for k, v in PAGE_PAIRS.items()}


def get_page_slug(filepath):
    """Get the extensionless slug from a file path relative to project dir."""
    rel = os.path.relpath(filepath, PROJECT_DIR).replace("\\", "/")
    # Remove .html extension
    if rel.endswith(".html"):
        rel = rel[:-5]
    return rel


def build_hreflang_tags(es_slug, en_slug):
    """Build hreflang link tags for a page pair."""
    es_url = f"{BASE}/{es_slug}"
    en_url = f"{BASE}/{en_slug}"
    return (
        f'<link rel="alternate" hreflang="es" href="{es_url}">\n'
        f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{es_url}">'
    )


def fix_file(filepath):
    """Apply all fixes to a single HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    slug = get_page_slug(filepath)
    is_en = slug.startswith("en/")

    # Determine ES and EN slugs for this page
    if is_en:
        en_slug = slug
        es_slug = EN_TO_ES.get(slug)
    else:
        es_slug = slug
        en_slug = PAGE_PAIRS.get(slug)

    if es_slug is None or en_slug is None:
        print(f"  SKIP: No pair found for {slug}")
        return False

    own_url = f"{BASE}/{slug}"

    # --- 1. Fix canonical tag on EN pages ---
    if is_en:
        es_url_pattern = f"{BASE}/{es_slug}"
        # Fix canonical
        content = content.replace(
            f'<link rel="canonical" href="{es_url_pattern}">',
            f'<link rel="canonical" href="{own_url}">'
        )
        # Fix og:url
        content = re.sub(
            r'<meta property="og:url" content="' + re.escape(es_url_pattern) + r'">',
            f'<meta property="og:url" content="{own_url}">',
            content
        )
        # Fix twitter:url
        content = re.sub(
            r'<meta name="twitter:url" content="' + re.escape(es_url_pattern) + r'">',
            f'<meta name="twitter:url" content="{own_url}">',
            content
        )

    # --- 2. Fix structured data URLs on EN pages ---
    if is_en:
        # Fix "url" fields in JSON-LD that point to ES version
        es_url = f"{BASE}/{es_slug}"
        # Replace url fields in JSON-LD (be careful to only match JSON "url" fields)
        content = content.replace(
            f'"url": "{es_url}"',
            f'"url": "{own_url}"'
        )
        # Also fix "item" fields in breadcrumbs that reference the page itself
        # But NOT the homepage/root breadcrumb items

    # --- 3. Add hreflang tags (on ALL pages, ES and EN) ---
    hreflang_block = build_hreflang_tags(es_slug, en_slug)

    # Check if hreflang tags already exist
    if 'hreflang=' not in content:
        # Insert after the canonical tag
        canonical_pattern = r'(<link rel="canonical" href="[^"]*">)'
        match = re.search(canonical_pattern, content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n" + hreflang_block + content[insert_pos:]
        else:
            print(f"  WARNING: No canonical tag found in {filepath}")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("Fixing canonical tags, og:url, twitter:url, hreflang, and structured data")
    print("=" * 60)

    # Collect all HTML files (excluding node_modules, temp files, index.html, google verification)
    html_files = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip node_modules
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            if fname.startswith("temp_") or fname.startswith("google"):
                continue
            if fname == "index.html":
                continue
            fpath = os.path.join(root, fname)
            html_files.append(fpath)

    modified = 0
    skipped = 0
    for fpath in sorted(html_files):
        rel = os.path.relpath(fpath, PROJECT_DIR)
        print(f"\nProcessing: {rel}")
        if fix_file(fpath):
            print(f"  ✓ Modified")
            modified += 1
        else:
            print(f"  - No changes")
            skipped += 1

    print(f"\n{'=' * 60}")
    print(f"Done! Modified: {modified}, Skipped: {skipped}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
