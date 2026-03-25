#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: str | None):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def uniq(items):
    seen = set()
    out = []
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def ensure_case(base: dict | None) -> dict:
    base = dict(base or {})
    base.setdefault('caseId', '')
    base.setdefault('title', '')
    base.setdefault('context', '')
    base.setdefault('geopoliticalContext', '')
    base.setdefault('keyActors', [])
    base.setdefault('policyQuestion', '')
    base.setdefault('assumptions', [])
    base.setdefault('sourceCards', [])
    base.setdefault('evidence', {'supporting': [], 'contradicting': [], 'ignored': []})
    base.setdefault('biases', [])
    base.setdefault('osintPitfalls', [])
    base.setdefault('mitigations', [])
    base.setdefault('structuredAnalysis', {})
    base.setdefault('discussionPrompts', [])
    base.setdefault('expertAnalysis', '')
    base.setdefault('recommendedDeliverables', [])
    base.setdefault('caseSummary', '')
    return base


def infer_summary(case: dict) -> str:
    title = case.get('title') or 'This case'
    pitfalls = [x for x in case.get('osintPitfalls', []) if x]
    biases = [x.get('bias', '') for x in case.get('biases', []) if isinstance(x, dict)]
    if pitfalls:
        return f"{title} centers on how {', '.join(pitfalls[:2])} distort judgment and why stronger mitigation is needed."
    if biases:
        return f"{title} highlights how {', '.join(biases[:2])} shape interpretation under uncertainty."
    return f"{title} has been assembled into a reusable Glassroom case object for further analysis."


def infer_discussion_prompts(case: dict):
    prompts = list(case.get('discussionPrompts', []))
    if not prompts and case.get('policyQuestion'):
        prompts.append(case['policyQuestion'])
    if case.get('osintPitfalls'):
        prompts.append('Which mitigation would most effectively reduce the identified OSINT pitfalls?')
    if case.get('biases'):
        prompts.append('Which bias most shaped the judgment, and what evidence should have challenged it?')
    return uniq(prompts)


def infer_deliverables(case: dict):
    deliverables = list(case.get('recommendedDeliverables', []))
    if not deliverables:
        deliverables.extend(['analytic-memo', 'interactive-case-page'])
    if case.get('structuredAnalysis', {}).get('method'):
        deliverables.append('structured-analysis-sheet')
    return uniq(deliverables)


def merge_case(base_case, source_card, bias_analysis, mitigation_pack, structured_analysis):
    case = ensure_case(base_case)

    if source_card:
        case['sourceCards'] = uniq(case.get('sourceCards', []) + [source_card])
        if not case.get('title'):
            case['title'] = source_card.get('title', '')

    if bias_analysis:
        case['biases'] = uniq(case.get('biases', []) + bias_analysis.get('items', []))
        if not case.get('title'):
            case['title'] = bias_analysis.get('caseTitle', '')

    if mitigation_pack:
        case['mitigations'] = uniq(case.get('mitigations', []) + mitigation_pack.get('items', []))
        case['osintPitfalls'] = uniq(
            case.get('osintPitfalls', []) + [x.get('pitfall', '') for x in mitigation_pack.get('items', []) if isinstance(x, dict)]
        )
        if not case.get('title'):
            case['title'] = mitigation_pack.get('caseTitle', '')

    if structured_analysis:
        case['structuredAnalysis'] = structured_analysis
        if not case.get('policyQuestion'):
            case['policyQuestion'] = structured_analysis.get('policyQuestion', '')
        if not case.get('title'):
            case['title'] = structured_analysis.get('caseTitle', '')

    case['discussionPrompts'] = infer_discussion_prompts(case)
    case['recommendedDeliverables'] = infer_deliverables(case)
    if not case.get('caseSummary'):
        case['caseSummary'] = infer_summary(case)

    return case


def render_markdown(case: dict) -> str:
    lines = [f"# Assembled case: {case.get('title') or 'Untitled case'}", ""]
    lines += [case.get('caseSummary') or '', ""]
    lines += [
        f"- Policy question: {case.get('policyQuestion', '') or 'not set'}",
        f"- Source cards: {len(case.get('sourceCards', []))}",
        f"- Bias items: {len(case.get('biases', []))}",
        f"- Mitigation items: {len(case.get('mitigations', []))}",
        f"- Structured method: {case.get('structuredAnalysis', {}).get('method', '') or 'not set'}",
        "",
    ]
    if case.get('discussionPrompts'):
        lines += ["## Discussion prompts", ""] + [f"- {x}" for x in case['discussionPrompts']] + [""]
    if case.get('recommendedDeliverables'):
        lines += ["## Recommended deliverables", ""] + [f"- {x}" for x in case['recommendedDeliverables']] + [""]
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description='Assemble a Glassroom case object from intermediate outputs')
    ap.add_argument('--base-case')
    ap.add_argument('--source-card')
    ap.add_argument('--bias-analysis')
    ap.add_argument('--mitigation-pack')
    ap.add_argument('--structured-analysis')
    ap.add_argument('--out-json', required=True)
    ap.add_argument('--out-md')
    args = ap.parse_args()

    case = merge_case(
        load_json(args.base_case),
        load_json(args.source_card),
        load_json(args.bias_analysis),
        load_json(args.mitigation_pack),
        load_json(args.structured_analysis),
    )

    Path(args.out_json).write_text(json.dumps(case, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.out_md:
        Path(args.out_md).write_text(render_markdown(case), encoding='utf-8')

    print(json.dumps(case, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
