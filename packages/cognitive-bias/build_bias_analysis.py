#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SOURCE_BASIS = [
    {
        "title": "CIA — Psychology of Intelligence Analysis",
        "url": "https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/",
    },
    {
        "title": "CIA — Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis",
        "url": "https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf",
    },
    {
        "title": "ODNI — Analytic Objectivity / ICD 203 Analytic Standards",
        "url": "https://www.dni.gov/index.php/how-we-work/objectivity",
    },
]

BIAS_MAP = {
    "confirmation bias": {
        "fit": "The claim may be filtering evidence through a preferred narrative instead of seriously testing competing explanations.",
        "mitigation": "Run a contradiction-first reading and force a visible comparison with at least one serious alternative explanation.",
        "recommendedTechnique": "Analysis of alternatives",
        "mitigationSteps": [
            "List the current preferred explanation in one sentence.",
            "List evidence that weakens or contradicts it before adding more supporting evidence.",
            "Write at least one competing explanation that could also fit the facts.",
            "State what additional evidence would discriminate between the two explanations.",
        ],
    },
    "anchoring": {
        "fit": "The judgment may be overly tied to an early assumption, first framing cue, or first number encountered.",
        "mitigation": "Strip away the original anchor, restate the problem from scratch, and compare multiple framings before deciding.",
        "recommendedTechnique": "Alternative framing check",
        "mitigationSteps": [
            "Rewrite the core question without the original anchor term, number, or first hypothesis.",
            "Generate two alternative framings of the same problem.",
            "Check whether your judgment changes under the new framings.",
            "Explain why the original anchor should still matter, if it does.",
        ],
    },
    "mirror imaging": {
        "fit": "The analyst may be projecting their own assumptions, preferences, or decision logic onto another actor.",
        "mitigation": "Rebuild the judgment from the actor's institutional incentives, constraints, doctrine, and risk tolerance rather than your own intuition.",
        "recommendedTechnique": "Actor-model reconstruction",
        "mitigationSteps": [
            "List the actor's incentives, constraints, and likely priorities.",
            "Identify where your own assumptions may differ from the actor's context.",
            "Re-state the judgment as that actor might see it.",
            "Check whether the original conclusion still holds under the actor-centered model.",
        ],
    },
    "availability heuristic": {
        "fit": "Salient, recent, vivid, or easily recalled information may be overweighted relative to more diagnostic evidence.",
        "mitigation": "Force inclusion of less vivid but more probative evidence and make source quality explicit before final judgment.",
        "recommendedTechnique": "Evidence-weighting pass",
        "mitigationSteps": [
            "Separate vivid evidence from high-diagnostic-value evidence.",
            "Describe the credibility and limitations of each important source.",
            "Add at least one non-salient source that could materially change the judgment.",
            "Re-evaluate the conclusion after weighting diagnostic value rather than memorability.",
        ],
    },
    "overconfidence": {
        "fit": "The level of certainty appears stronger than the available evidence can support.",
        "mitigation": "Downgrade confidence, distinguish what is known from what is inferred, and make uncertainty explicit.",
        "recommendedTechnique": "Confidence calibration",
        "mitigationSteps": [
            "Separate facts, assumptions, and judgments into distinct buckets.",
            "State what could still prove the judgment wrong.",
            "Use an explicit confidence level rather than rhetorical certainty.",
            "Revise the conclusion so the confidence matches the evidence base.",
        ],
    },
    "groupthink": {
        "fit": "The interpretation may be converging too quickly around consensus rather than being tested through disagreement.",
        "mitigation": "Run a devil's-advocacy or red-team pass and require at least one serious alternative reading before final synthesis.",
        "recommendedTechnique": "Red team / devil's advocacy",
        "mitigationSteps": [
            "Assign one person or one paragraph to argue against the emerging consensus.",
            "Make at least one alternative interpretation visible in the output.",
            "Document which evidence favors the minority view.",
            "Explain why the consensus still wins, if it does.",
        ],
    },
    "wishful thinking": {
        "fit": "The preferred outcome may be treated as more likely simply because it is desirable.",
        "mitigation": "Use a premortem and specify what would make the optimistic reading fail.",
        "recommendedTechnique": "Premortem",
        "mitigationSteps": [
            "Assume the preferred outcome turns out to be wrong.",
            "List the most plausible reasons it failed.",
            "Identify which of those failure conditions are already partly visible.",
            "Revise the judgment so desirability is not mistaken for probability.",
        ],
    },
    "premature closure": {
        "fit": "The analysis may be closing too early before key uncertainties, assumptions, or missing evidence are checked.",
        "mitigation": "List unresolved questions, define what could still change the judgment, and delay closure until the decision threshold is explicit.",
        "recommendedTechnique": "Key uncertainties check",
        "mitigationSteps": [
            "List the unresolved questions that still matter to the judgment.",
            "State which ones could meaningfully change the conclusion.",
            "Define what evidence threshold would justify closure.",
            "Flag the judgment as provisional if that threshold has not been met.",
        ],
    },
    "framing effect": {
        "fit": "The way the problem is presented may be steering the judgment before the evidence is fully assessed.",
        "mitigation": "Reframe the question in multiple ways and compare whether the same evidence still supports the same conclusion.",
        "recommendedTechnique": "Reframing pass",
        "mitigationSteps": [
            "Rewrite the problem using at least two alternative question frames.",
            "Test whether the same evidence looks equally persuasive under each frame.",
            "Identify which words in the original frame carried hidden assumptions.",
            "Preserve the frame that best matches the actual decision problem.",
        ],
    },
    "satisficing": {
        "fit": "The analysis may be stopping at the first explanation that seems good enough rather than examining whether a better one exists.",
        "mitigation": "Force one more serious hypothesis and define a visible stop rule for when the search is sufficient.",
        "recommendedTechnique": "Hypothesis expansion",
        "mitigationSteps": [
            "Write the first acceptable explanation currently driving the judgment.",
            "Generate at least one additional plausible explanation that could compete with it.",
            "Compare the two using the same evidence set.",
            "State why the search can stop now rather than later.",
        ],
    },
    "recency bias": {
        "fit": "Recent developments may be receiving more weight than longer-term patterns, baselines, or historical context.",
        "mitigation": "Reinsert trend, baseline, and historical comparison before interpreting the latest signal.",
        "recommendedTechnique": "Baseline and trend check",
        "mitigationSteps": [
            "Describe the longer-term baseline before discussing the newest event.",
            "Compare the recent development against historical patterns.",
            "Ask whether the latest event is exceptional, cyclical, or merely more visible.",
            "Revise the judgment if the baseline weakens the recency-driven interpretation.",
        ],
    },
    "fundamental attribution error": {
        "fit": "Behavior may be explained too quickly in terms of intent or character instead of situational, bureaucratic, or structural constraints.",
        "mitigation": "Test situational and organizational explanations before settling on motive-heavy interpretations.",
        "recommendedTechnique": "Disposition vs situation check",
        "mitigationSteps": [
            "List the situational constraints that could explain the observed behavior.",
            "List the organizational or bureaucratic pressures shaping the actor's choices.",
            "Compare those explanations against intent-based interpretations.",
            "Keep motive claims narrow unless the evidence clearly supports them.",
        ],
    },
}

ALIASES = {
    "confirmation": "confirmation bias",
    "confirmation bias": "confirmation bias",
    "anchoring": "anchoring",
    "anchor bias": "anchoring",
    "mirror imaging": "mirror imaging",
    "mirror-imaging": "mirror imaging",
    "availability": "availability heuristic",
    "availability heuristic": "availability heuristic",
    "overconfidence": "overconfidence",
    "groupthink": "groupthink",
    "wishful thinking": "wishful thinking",
    "premature closure": "premature closure",
    "framing": "framing effect",
    "framing effect": "framing effect",
    "satisficing": "satisficing",
    "recency bias": "recency bias",
    "fundamental attribution error": "fundamental attribution error",
    "disposition bias": "fundamental attribution error",
}


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def normalize_bias_name(bias: str) -> str:
    key = bias.strip().lower()
    return ALIASES.get(key, key)


def display_bias_name(key: str, original: str) -> str:
    if original and original.strip():
        return original
    return key


def build_analysis(data: dict) -> dict:
    items = []
    excerpt = data.get('sourceExcerpt', '')
    for bias in data.get('candidateBiases', []):
        key = normalize_bias_name(bias)
        meta = BIAS_MAP.get(key, {
            'fit': 'This candidate bias needs manual justification from the text.',
            'mitigation': 'Explain the bias-evidence link, clarify uncertainty, and choose the lightest corrective tradecraft step.',
            'recommendedTechnique': 'Manual tradecraft review',
            'mitigationSteps': [
                'Identify the evidence that makes this bias plausible.',
                'Separate information, assumptions, and judgment.',
                'Add one corrective analytic step before finalizing the conclusion.',
            ],
        })
        items.append({
            'bias': display_bias_name(key, bias),
            'evidence': excerpt,
            'whyItFits': meta['fit'],
            'mitigation': meta['mitigation'],
            'recommendedTechnique': meta['recommendedTechnique'],
            'mitigationSteps': meta['mitigationSteps'],
        })
    return {
        'caseTitle': data.get('caseTitle', ''),
        'coreClaim': data.get('coreClaim', ''),
        'sourceBasis': SOURCE_BASIS,
        'items': items,
        'notes': data.get('notes', []),
    }


def render_markdown(result: dict) -> str:
    lines = [f"# Bias analysis: {result.get('caseTitle') or 'Untitled case'}", ""]
    if result.get('coreClaim'):
        lines += ["## Core claim", "", result['coreClaim'], ""]
    if result.get('sourceBasis'):
        lines += ["## Tradecraft basis", ""]
        for src in result['sourceBasis']:
            lines.append(f"- {src['title']} — {src['url']}")
        lines += [""]
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
            "### Recommended technique",
            "",
            item['recommendedTechnique'],
            "",
            "### Mitigation",
            "",
            item['mitigation'],
            "",
            "### Mitigation steps",
            "",
        ]
        lines += [f"- {step}" for step in item.get('mitigationSteps', [])]
        lines += [""]
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
