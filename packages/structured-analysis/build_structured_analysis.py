#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def build_key_assumptions(data: dict) -> dict:
    items = []
    for assumption in data.get('assumptions', []):
        items.append({
            'assumption': assumption,
            'whyItMatters': 'This assumption materially affects the judgment if it is wrong.',
            'whatWouldWeakenIt': 'Contradictory evidence, failed historical comparison, or alternative actor incentives.',
            'whatToVerifyNext': 'Look for direct primary-source evidence or stronger contradictory signals.'
        })
    return {
        'caseTitle': data.get('caseTitle', ''),
        'method': 'key-assumptions-check',
        'policyQuestion': data.get('policyQuestion', ''),
        'items': items
    }


def build_ach(data: dict) -> dict:
    hypotheses = data.get('hypotheses', [])
    supporting = data.get('evidence', {}).get('supporting', [])
    contradicting = data.get('evidence', {}).get('contradicting', [])
    rows = []
    for hyp in hypotheses:
        rows.append({
            'hypothesis': hyp,
            'supportingEvidence': supporting,
            'contradictingEvidence': contradicting,
            'diagnosticValue': 'Needs analyst review to determine which evidence best discriminates between hypotheses.',
            'provisionalAssessment': 'Tentative pending comparative evaluation.'
        })
    return {
        'caseTitle': data.get('caseTitle', ''),
        'method': 'ach',
        'policyQuestion': data.get('policyQuestion', ''),
        'rows': rows
    }


def render_markdown(result: dict) -> str:
    lines = [f"# Structured analysis: {result.get('caseTitle') or 'Untitled case'}", ""]
    lines += [f"- Method: {result.get('method', '')}", f"- Policy question: {result.get('policyQuestion', '')}", ""]
    if result.get('method') == 'key-assumptions-check':
        for item in result.get('items', []):
            lines += [
                f"## {item['assumption']}",
                "",
                f"- Why it matters: {item['whyItMatters']}",
                f"- What would weaken it: {item['whatWouldWeakenIt']}",
                f"- What to verify next: {item['whatToVerifyNext']}",
                "",
            ]
    else:
        for row in result.get('rows', []):
            lines += [
                f"## Hypothesis: {row['hypothesis']}",
                "",
                "### Supporting evidence",
                "",
            ] + [f"- {x}" for x in row.get('supportingEvidence', [])] + [
                "",
                "### Contradicting evidence",
                "",
            ] + [f"- {x}" for x in row.get('contradictingEvidence', [])] + [
                "",
                f"- Diagnostic value: {row['diagnosticValue']}",
                f"- Provisional assessment: {row['provisionalAssessment']}",
                "",
            ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description='Build a Glassroom structured-analysis pack')
    ap.add_argument('--input', required=True)
    ap.add_argument('--out-json')
    ap.add_argument('--out-md')
    args = ap.parse_args()

    data = load_json(args.input)
    method = (data.get('method') or 'key-assumptions-check').strip().lower()
    if method == 'ach':
        result = build_ach(data)
    else:
        result = build_key_assumptions(data)
    md = render_markdown(result)

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
    if args.out_md:
        Path(args.out_md).write_text(md, encoding='utf-8')

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
