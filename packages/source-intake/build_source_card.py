#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

PRIMARY_TYPES = {"official-statement", "diplomatic-cable", "intelligence-document"}

INSTITUTION_HINTS = {
    "state.gov": "U.S. Department of State",
    "archives.gov": "U.S. National Archives",
    "cia.gov": "CIA",
    "justice.gov": "U.S. Department of Justice",
    "europa.eu": "European Union",
    "un.org": "United Nations",
    "wikileaks.org": "WikiLeaks",
    "whitehouse.gov": "White House",
}


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def infer_title(data: dict) -> str:
    if data.get("title"):
        return data["title"].strip()
    for key in ("canonicalTitle", "subject"):
        if data.get(key):
            return str(data[key]).strip()
    for key in ("path", "filePath", "url"):
        if data.get(key):
            return Path(str(data[key])).name
    return "Untitled source"


def infer_institution(url: str | None, text: str) -> str:
    if url:
        netloc = urlparse(url).netloc.lower()
        for hint, inst in INSTITUTION_HINTS.items():
            if hint in netloc:
                return inst
    patterns = [
        (r"department of state|state department", "U.S. Department of State"),
        (r"central intelligence agency|\bcia\b", "CIA"),
        (r"department of justice|\bdoj\b", "U.S. Department of Justice"),
        (r"united nations|\bun\b", "United Nations"),
        (r"european union|\beu\b", "European Union"),
    ]
    low = text.lower()
    for pat, inst in patterns:
        if re.search(pat, low):
            return inst
    return ""


def classify_source_type(title: str, url: str | None, path: str | None, text: str) -> str:
    joined = " ".join(filter(None, [title, url or "", path or "", text])).lower()
    if any(x in joined for x in ["cable", "embassy", "wikileaks", "plusd"]):
        return "diplomatic-cable"
    if any(x in joined for x in ["reading room", "declassified", "intelligence estimate", "cia"]):
        return "intelligence-document"
    if any(x in joined for x in ["press release", "statement", "ministry", ".gov", "white house", "department of", "official", "foreign relations of the united states"]):
        return "official-statement"
    if any(x in joined for x in ["journal", "doi", "abstract", "university press", "cq press"]):
        return "academic-paper"
    if any(x in joined for x in ["reuters", "bbc", "times", "news", "article"]):
        return "news-article"
    if any(x in joined for x in ["note", "lecture", "class note", "syllabus"]):
        return "course-note"
    return "other"


def infer_audience(source_type: str, institution: str) -> str:
    if source_type in {"official-statement", "diplomatic-cable", "intelligence-document"}:
        return institution or "policy / institutional audience"
    if source_type == "academic-paper":
        return "academic audience"
    if source_type == "news-article":
        return "public audience"
    if source_type == "course-note":
        return "classroom audience"
    return "general audience"


def infer_reliability(source_type: str, url: str | None, retrieval_quality: str, has_sufficient_text: bool) -> str:
    base = ""
    if source_type in {"official-statement", "diplomatic-cable", "intelligence-document"}:
        base = "High provenance value as a primary or near-primary source, but still requires interpretation and context checking."
    elif source_type == "academic-paper":
        base = "Useful for framing and scholarly interpretation; not automatically a substitute for primary evidence."
    elif source_type == "news-article":
        base = "Useful for context and chronology, but should be checked against stronger upstream or official sources when possible."
    elif source_type == "course-note":
        base = "Useful for class framing, but should not be treated as raw evidence unless explicitly sourced."
    elif url and "wikileaks.org" in url.lower():
        base = "Potentially valuable document source; verify provenance and separate the document from later interpretation."
    else:
        base = "Needs closer provenance and reliability review."

    suffix = f" Retrieval quality: {retrieval_quality}."
    if not has_sufficient_text:
        suffix += " Full text capture is still too thin; do not treat this as a complete source capture yet."
    return base + suffix


def infer_next_step(source_type: str, has_sufficient_text: bool) -> str:
    if not has_sufficient_text:
        return "source-upstream-search"
    if source_type in {"official-statement", "diplomatic-cable", "intelligence-document"}:
        return "bias-analysis"
    if source_type == "news-article":
        return "source-upstream-search"
    if source_type == "academic-paper":
        return "structured-analysis"
    if source_type == "course-note":
        return "course-writing"
    return "bias-analysis"


def build_card(data: dict) -> dict:
    title = infer_title(data)
    url = data.get("url")
    path = data.get("path") or data.get("filePath")
    full_text = data.get("fullText", "")
    text = " ".join(filter(None, [full_text, data.get("contentSnippet", ""), data.get("notes", "")]))
    source_type = classify_source_type(title, url, path, text)
    institution = data.get("authorOrInstitution") or infer_institution(url, " ".join(filter(None, [title, text])))
    retrieval_quality = data.get("retrievalQuality")
    if not retrieval_quality:
        text_len = len(full_text)
        if text_len >= 4000:
            retrieval_quality = "high"
        elif text_len >= 1500:
            retrieval_quality = "medium"
        elif text_len >= 500:
            retrieval_quality = "low"
        else:
            retrieval_quality = "insufficient"
    has_sufficient_text = bool(data.get("hasSufficientText", retrieval_quality in {"medium", "high"}))
    return {
        "title": title,
        "sourceType": source_type,
        "date": data.get("date", ""),
        "authorOrInstitution": institution,
        "audience": infer_audience(source_type, institution),
        "isPrimarySource": source_type in PRIMARY_TYPES,
        "reliabilityNote": infer_reliability(source_type, url, retrieval_quality, has_sufficient_text),
        "courseRelevance": data.get("courseRelevance") or "Relevant as a source to classify before deeper bias, structure, or writing work.",
        "recommendedNextStep": infer_next_step(source_type, has_sufficient_text),
        "upstreamUrl": url or "",
        "fullTextCharCount": data.get("fullTextCharCount", len(full_text)),
        "retrievalQuality": retrieval_quality,
        "hasSufficientText": has_sufficient_text,
        "contentSnippet": data.get("contentSnippet", ""),
    }


def render_markdown(card: dict) -> str:
    lines = [
        f"# Source card: {card['title']}",
        "",
        f"- Source type: {card['sourceType']}",
        f"- Date: {card['date'] or 'unknown'}",
        f"- Author / institution: {card['authorOrInstitution'] or 'unknown'}",
        f"- Audience: {card['audience']}",
        f"- Primary source: {'yes' if card['isPrimarySource'] else 'no'}",
        f"- Retrieval quality: {card.get('retrievalQuality', '')}",
        f"- Full text chars: {card.get('fullTextCharCount', 0)}",
        f"- Has sufficient text: {'yes' if card.get('hasSufficientText') else 'no'}",
        "",
        "## Reliability note",
        "",
        card['reliabilityNote'],
        "",
        "## Course relevance",
        "",
        card['courseRelevance'],
        "",
        "## Recommended next step",
        "",
        card['recommendedNextStep'],
        "",
    ]
    if card.get("contentSnippet"):
        lines += ["## Snippet", "", card["contentSnippet"], ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Build a Glassroom source card from a source descriptor JSON")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    args = ap.parse_args()

    data = load_json(args.input)
    card = build_card(data)
    md = render_markdown(card)

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.out_md:
        Path(args.out_md).write_text(md, encoding="utf-8")

    print(json.dumps(card, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
