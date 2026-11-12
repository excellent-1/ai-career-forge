import unittest
from pydantic import ValidationError
from career_forge.analyzer import analyze_rules, validate_evidence
from career_forge.models import JobAnalysis, Requirement


class AnalyzerTests(unittest.TestCase):
    def test_priority_and_evidence(self):
        text = 'Required: Python and FastAPI.\nPreferred: Docker.'
        result = analyze_rules(text)
        self.assertEqual([(r.skill,r.priority) for r in result.analysis.requirements],
                         [('Python','required'),('FastAPI','required'),('Docker','preferred')])
        self.assertTrue(all(r.evidence in text for r in result.analysis.requirements))

    def test_word_boundary(self):
        skills = [r.skill for r in analyze_rules('JavaScript required.').analysis.requirements]
        self.assertEqual(skills,['JavaScript'])

    def test_csharp(self):
        self.assertEqual(analyze_rules('C# required.').analysis.requirements[0].skill,'C#')

    def test_missing_input(self):
        for text in ['', '   ', 'x'*20001]:
            with self.assertRaises(ValueError):
                analyze_rules(text)

    def test_unknown_is_not_invented(self):
        self.assertEqual(analyze_rules('Communicate clearly.').analysis.requirements,[])

    def test_optional_not_required(self):
        self.assertEqual(analyze_rules('Docker is not required.').analysis.requirements[0].priority,'preferred')

    def test_schema_rejects_invalid_priority_and_extra_fields(self):
        for values in [dict(skill='Python',priority='mandatory',evidence='Python'),
                       dict(skill='Python',priority='required',evidence='Python',salary=200000)]:
            with self.assertRaises(ValidationError):
                Requirement(**values)

    def test_rejects_fabricated_evidence(self):
        analysis = JobAnalysis(requirements=[Requirement(skill='Python',priority='required',evidence='Python required')],unknowns=[])
        with self.assertRaises(ValueError):
            validate_evidence(analysis,'Docker preferred')

    def test_genuine_quote_does_not_prove_semantics(self):
        analysis = JobAnalysis(requirements=[Requirement(skill='Kubernetes',priority='required',evidence='Docker preferred')],unknowns=[])
        self.assertTrue(validate_evidence(analysis,'Docker preferred'))

    def test_conflicting_mentions_are_preserved(self):
        result = analyze_rules('Python required.\nPython preferred.')
        self.assertEqual(len(result.analysis.requirements),2)

    def test_source_hash_is_stable_after_trimming(self):
        self.assertEqual(analyze_rules(' Python ').source_sha256,analyze_rules('Python').source_sha256)

    def test_documented_mixed_priority_limitation(self):
        result = analyze_rules('Python required, Docker preferred.')
        self.assertEqual(result.analysis.requirements[0].priority,'preferred')


if __name__ == '__main__':
    unittest.main()
