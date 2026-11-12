import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / 'app.py'


class AppTests(unittest.TestCase):
    def test_reader_and_rules_analyzer(self):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        self.assertFalse(app.exception)
        app.sidebar.radio[0].set_value('Analyzer').run()
        next(b for b in app.button if b.label == 'Analyze posting').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state['analysis_run']['mode'],'rules')
        self.assertTrue(app.session_state['analysis_run']['analysis']['requirements'])

    def test_completed_project_launch_runs_example_and_accepts_new_input(self):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        next(b for b in app.button if b.label == 'Run completed Chapter 1 project').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.sidebar.radio[0].value, 'Completed project')
        report = app.session_state['completed_report']
        self.assertEqual(report['mode'], 'rules')
        self.assertEqual(len(report['analysis']['requirements']), 9)
        app.text_area[0].set_value('Required: Python.').run()
        next(b for b in app.button if b.label == 'Analyze posting').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.session_state['completed_report']['analysis']['requirements']), 1)

    def test_practice_and_failure_lab_render(self):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        for view in ['Practice','Failure lab','Portfolio checklist']:
            app.sidebar.radio[0].set_value(view).run()
            self.assertFalse(app.exception)
