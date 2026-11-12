import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / 'app.py'


class AppTests(unittest.TestCase):
    def test_reader_and_rules_analyzer(self):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        self.assertFalse(app.exception)
        app.sidebar.radio[0].set_value('Analyzer').run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state['analysis_run']['mode'],'rules')
        self.assertTrue(app.session_state['analysis_run']['analysis']['requirements'])

    def test_practice_and_failure_lab_render(self):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        for view in ['Practice','Failure lab','Portfolio checklist']:
            app.sidebar.radio[0].set_value(view).run()
            self.assertFalse(app.exception)
