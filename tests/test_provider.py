import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from career_forge.models import JobAnalysis, Requirement
from career_forge.providers import analyze_live


def completion(parsed=None, refusal=None):
    return NS(choices=[NS(message=NS(parsed=parsed, refusal=refusal))])


class ProviderTests(unittest.TestCase):
    def run_with(self, result, text='Python required.'):
        with patch('openai.OpenAI') as client:
            client.return_value.chat.completions.parse.return_value = result
            return analyze_live(text, api_key='test-not-a-real-key', model='test-model')

    def test_accepts_grounded_result(self):
        parsed=JobAnalysis(requirements=[Requirement(skill='Python',priority='required',evidence='Python required.')],unknowns=[])
        self.assertEqual(self.run_with(completion(parsed)).mode,'live-ai')

    def test_refusal(self):
        with self.assertRaises(ValueError):
            self.run_with(completion(refusal='declined'))

    def test_absent_parse(self):
        with self.assertRaises(ValueError):
            self.run_with(completion())

    def test_unsupported_quote(self):
        parsed=JobAnalysis(requirements=[Requirement(skill='Python',priority='required',evidence='invented')],unknowns=[])
        with self.assertRaises(ValueError):
            self.run_with(completion(parsed))

    def test_configuration_required(self):
        with self.assertRaises(ValueError):
            analyze_live('Python',api_key='',model='')
