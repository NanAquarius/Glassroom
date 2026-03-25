#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

BIAS_MAP = {
    "confirmation bias": {
        "fit": "The claim may be filtering evidence through a preferred narrative instead of testing competing explanations.",
        "mitigation": "Run a contradiction-first reading and explicitly list evidence against the preferred interpretation."
    },
    "anchoring": {
        "fit": "The judgment may be overly tied to an early assumption or first framing cue.",
        "mitigation": "Restate the case without the original anchor and compare alternative framings."
    },
    "mirror imaging": {
        "fit": "The analyst may be projecting their own assumptions or decision logic onto another actor.",
        "mitigation": "Rebuild the judgment from the actor's institutional incentives rather than your own intuition."
    },
    "availability heuristic": {
        "fit": "Salient or recent information may be overweighted relative to more diagnostic evidence.",
        "mitigation": "Force inclusion of less vivid but more probative evidence before final judgment."
    },
    "overconfidence": {
        "fit": "The level of certainty appears stronger than the available evidence can support.",
        "mitigation": "Downgrade confidence and separate what is known, inferred, and assumed."
    },
    "groupthink": {
        "fit": "The interpretation may be converging too quickly around consensus rather than disagreement testing.",
        "mitigation": "Run a devil's-advocacy pass and require at least one serious alternative reading."
    },
    "wishful thinking": {
        "fit": "The preferred outcome may be treated as more likely simply because it is desirable.",
        "mitigation": "Use a premortem and specify what would make the optimistic reading fail."
    },
    "premature closure": {
        "fit": "The analysis may be closing too early before key uncertainties are checked.",
        "mitigation": "List unresolved questions and identify which ones could still change the judgment."
    }
}


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def build_analysis(data: dict) -> dict:
    items = []
    excerpt = data.get('sourceExcerpt', '')
    for bias in data.get('candidateBiases', []):
        key = bias.strip().lower()
        meta = BIAS_MAP.get(key, {
            'fit': 'This candidate bias needs manual justification from the text.',
            'mitigation': 'Explain the bias-evidence link and choose the lightest corrective method.'
        })
        items.append({
            'bias': bias,
            'evidence': excerpt,
            'whyItFits': meta['fit'],
            'mitigation': meta['mitigation']
        })
    return {
        'caseTitle': data.get('caseTitle', ''),
        'coreClaim': data.get('coreClaim', ''),
        'items': items,
        'notes': data.get('notes', [])
    }


def render_markdown(result: dict) -> str:
    lines = [f"# Bias analysis: {result.get('caseTitle') or 'Untitled case'}", ""]
    if result.get('coreClaim'):
        lines += ["## Core claim", "", result['coreClaim'], ""]
    for item in result.get('items', []):
        lines += [
            f"## {item['bias']}",
            "",
            "### Evidence",
            "",
            item['evidence'] or 'No direct excerpt provided.',
            "",
            "### Why it fits",
            "",
            item['whyItFits'],
            "",
            "### Mitigation",
            "",
            item['mitigation'],
            "",
        ]
    if result.get('notes'):
        lines += ["## Notes", ""] + [f"- {x}" for x in result['notes']] + [""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description='Build a Glassroom cognitive-bias analysis pack')
    ap.add_argument('--input', required=True)
    ap.add_argument('--out-json')
    ap.add_argument('--out-md')
    args = ap.parse_args()

    data = load_json(args.input)
    result = build_analysis(data)
    md = render_markdown(result)

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
    if args.out_md:
        Path(args.out_md).write_text(md, encoding='utf-8')

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
