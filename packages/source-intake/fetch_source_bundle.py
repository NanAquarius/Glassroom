#!/usr/bin/env python3
import argparse
import html
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

USER_AGENT = "Mozilla/5.0 (Glassroom Source Intake)"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[\[Page\s+\d+\]\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_between(pattern: str, html_text: str) -> str | None:
    m = re.search(pattern, html_text, re.I | re.S)
    return m.group(1) if m else None


def detect_provider(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    if "history.state.gov" in netloc:
        return "frus"
    if "wikileaks.org" in netloc and "/plusd/" in url.lower():
        return "wikileaks-plusd"
    return "generic-html"


def extract_frus(html_text: str) -> dict:
    title = ""
    subject = ""
    m = re.search(r"<h3[^>]*>(.*?)</h3>", html_text, re.I | re.S)
    if m:
        title = clean_text(m.group(1))
    subj = extract_between(r"<h4[^>]*>\s*SUBJECT\s*</h4>([\s\S]*?)<p", html_text)
    if subj:
        subject = clean_text(subj)
    main = extract_between(r"<main[^>]*id=\"content\"[^>]*>([\s\S]*?)</main>", html_text)
    text = clean_text(main or html_text)
    return {
        "canonicalTitle": title,
        "subject": subject,
        "fullText": text,
        "extractionMethod": "frus-main-content",
    }


def extract_wikileaks_plusd(html_text: str) -> dict:
    title = ""
    date = ""
    subject = ""
    canonical_id = ""

    m = re.search(r"<title>\s*Cable:\s*([^<]+)</title>", html_text, re.I)
    if m:
        title = clean_text(m.group(1))
    subj = re.search(r"SUBJECT:\s*([^\n<]+)", html_text, re.I)
    if subj:
        subject = subj.group(1).strip()
    cid = re.search(r"Canonical ID:\s*</[^>]+>\s*([^<\n]+)", html_text, re.I)
    if cid:
        canonical_id = cid.group(1).strip()
    d = re.search(r"Date:\s*</[^>]+>\s*([0-9]{4}[^<\n]+)", html_text, re.I)
    if d:
        date = d.group(1).strip()

    body = extract_between(r"<div[^>]+id=\"tagged-text\"[^>]*>([\s\S]*?)</div>", html_text)
    if not body:
        body = extract_between(r"<div[^>]+class=\"text-content\"[^>]*>([\s\S]*?)</div>", html_text)
    text = clean_text(body or html_text)
    return {
        "canonicalTitle": subject or title or canonical_id,
        "subject": subject,
        "date": date,
        "canonicalId": canonical_id,
        "fullText": text,
        "extractionMethod": "wikileaks-plusd-tagged-text",
    }


def extract_generic(html_text: str) -> dict:
    title = ""
    m = re.search(r"<title>(.*?)</title>", html_text, re.I | re.S)
    if m:
        title = clean_text(m.group(1))
    main = extract_between(r"<main[^>]*>([\s\S]*?)</main>", html_text)
    article = extract_between(r"<article[^>]*>([\s\S]*?)</article>", html_text)
    body = main or article or html_text
    text = clean_text(body)
    return {
        "canonicalTitle": title,
        "fullText": text,
        "extractionMethod": "generic-main-or-body",
    }


def assess_completeness(text: str) -> str:
    n = len(text)
    if n >= 4000:
        return "high"
    if n >= 1500:
        return "medium"
    if n >= 500:
        return "low"
    return "insufficient"


def build_bundle(data: dict) -> dict:
    url = data.get("url", "")
    provider = detect_provider(url)
    fetch_error = ""
    try:
        html_text = fetch_url(url)
    except Exception as e:
        html_text = ""
        fetch_error = str(e)

    if provider == "frus":
        extracted = extract_frus(html_text)
    elif provider == "wikileaks-plusd":
        extracted = extract_wikileaks_plusd(html_text)
    else:
        extracted = extract_generic(html_text)

    full_text = extracted.get("fullText", "")
    completeness = assess_completeness(full_text)
    snippet = full_text[:1200]

    return {
        "title": data.get("title") or extracted.get("canonicalTitle") or "Untitled source",
        "url": url,
        "date": data.get("date") or extracted.get("date") or "",
        "authorOrInstitution": data.get("authorOrInstitution", ""),
        "contentSnippet": data.get("contentSnippet") or snippet,
        "notes": data.get("notes") or "",
        "courseRelevance": data.get("courseRelevance") or "",
        "provider": provider,
        "fetchStatus": "error" if fetch_error else "ok",
        "fetchError": fetch_error or None,
        "extractionMethod": extracted.get("extractionMethod", ""),
        "canonicalId": extracted.get("canonicalId", ""),
        "subject": extracted.get("subject", ""),
        "fullText": full_text,
        "fullTextCharCount": len(full_text),
        "retrievalQuality": completeness,
        "hasSufficientText": completeness in {"medium", "high"},
    }


def render_markdown(bundle: dict) -> str:
    lines = [
        f"# Source bundle: {bundle.get('title', 'Untitled source')}",
        "",
        f"- Provider: {bundle.get('provider', '')}",
        f"- Fetch status: {bundle.get('fetchStatus', '')}",
        f"- Extraction method: {bundle.get('extractionMethod', '')}",
        f"- Retrieval quality: {bundle.get('retrievalQuality', '')}",
        f"- Full text chars: {bundle.get('fullTextCharCount', 0)}",
        f"- Has sufficient text: {'yes' if bundle.get('hasSufficientText') else 'no'}",
        "",
        "## Snippet",
        "",
        bundle.get('contentSnippet', ''),
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Fetch and structure a fuller Glassroom source bundle from a URL")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    args = ap.parse_args()

    data = load_json(args.input)
    bundle = build_bundle(data)
    md = render_markdown(bundle)

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.out_md:
        Path(args.out_md).write_text(md, encoding="utf-8")

    print(json.dumps(bundle, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
