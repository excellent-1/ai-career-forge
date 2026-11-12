"""Evaluate a small synthetic baseline dataset. Not a market-wide accuracy claim."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from career_forge.analyzer import analyze_rules


def evaluate():
    cases = json.loads((ROOT / 'content/evaluation.json').read_text())
    rows = []
    for case in cases:
        result = analyze_rules(case['text'])
        predicted = {(r.skill, r.priority) for r in result.analysis.requirements}
        expected = {(r['skill'], r['priority']) for r in case['expected']}
        skills_p = {s for s, _ in predicted}
        skills_e = {s for s, _ in expected}
        rows.append({'id': case['id'], 'expected':len(expected), 'predicted':len(predicted),
                     'skill_precision': len(skills_p & skills_e)/len(skills_p) if skills_p else 1.0,
                     'skill_recall': len(skills_p & skills_e)/len(skills_e) if skills_e else 1.0,
                     'exact_skill_priority_match': predicted == expected,
                     'quotes_valid': all(r.evidence in case['text'] for r in result.analysis.requirements)})
    return {'scope':'8 synthetic smoke cases; documented challenge failures are outside this benchmark',
            'cases':rows, 'exact_matches':sum(r['exact_skill_priority_match'] for r in rows), 'total':len(rows)}


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report['exact_matches'] == report['total'] else 1)
