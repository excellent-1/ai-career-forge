"""Chapter 1: interactive book and deployable portfolio application."""
import json
import os
from pathlib import Path
import streamlit as st
from career_forge.analyzer import analyze_rules
from career_forge.providers import analyze_live

ROOT = Path(__file__).parent
CONTENT = json.loads((ROOT / 'content/chapter1.json').read_text())
st.set_page_config(page_title='AI Career Forge · Chapter 1', page_icon='📖', layout='wide')
st.sidebar.title('AI Career Forge')
st.sidebar.caption('BUILD · VERIFY · DEPLOY')
view = st.sidebar.radio('Workspace', ['Read chapter', 'Completed project', 'Practice', 'Analyzer', 'Failure lab', 'Portfolio checklist'], key='workspace')
st.sidebar.info('Chapter 1 is implemented. Later chapters and automated job matching are planned.')
st.title('Build a Job Requirements Analyzer')
st.caption('Chapter 1 · Working draft · Python / Pydantic / Structured outputs')


def open_completed_project():
    st.session_state.workspace = 'Completed project'
    st.session_state.completed_input = CONTENT['sample']
    st.session_state.completed_report = analyze_rules(CONTENT['sample']).model_dump()


st.button('Run completed Chapter 1 project', key='launch_completed', on_click=open_completed_project)


def setting(name):
    value = os.environ.get(name, '')
    if value:
        return value
    try:
        return str(st.secrets.get(name, ''))
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return ''


if view == 'Read chapter':
    lesson_id = st.selectbox('Section', range(len(CONTENT['lessons'])),
                             format_func=lambda i: CONTENT['lessons'][i]['label'])
    lesson = CONTENT['lessons'][lesson_id]
    st.header(lesson['title'])
    st.markdown(lesson['body'])
    st.caption('Source files and a printable Markdown chapter are included in the repository.')
elif view == 'Practice':
    st.info('Self-assessment: these checks validate short answers, not arbitrary Python code. Run the repository tests for executable coding work.')
    for q in CONTENT['questions']:
        with st.expander(q['title']):
            st.write(q['prompt'])
            if q.get('starter'):
                st.code(q['starter'], language='python')
            if q.get('options'):
                answer = st.radio('Your answer', q['options'], index=None, key=q['id'])
            else:
                answer = st.text_input('Your answer', key=q['id'])
            if st.button('Check answer', key='check-'+q['id']):
                accepted = [q['answer'], *q.get('aliases', [])]
                correct = (answer or '').strip().casefold() in [a.casefold() for a in accepted]
                if correct:
                    st.success(q['explanation'])
                else:
                    st.warning('Try again. '+q['explanation'])
elif view in ['Analyzer', 'Completed project']:
    completed = view == 'Completed project'
    report_key = 'completed_report' if completed else 'analysis_run'
    input_key = 'completed_input' if completed else 'analyzer_input'
    if completed:
        st.subheader('Finished reference application')
        st.write('Try the completed analyzer before building your own. The fictional chapter example is analyzed automatically. Edit the input and run it again.')
        st.caption('Previewing this reference does not mark lessons, exercises, or portfolio tasks complete.')
        if report_key not in st.session_state:
            st.session_state[report_key] = analyze_rules(CONTENT['sample']).model_dump()
    st.info('Default mode is a deterministic keyword baseline, not a model. Review every classification.')
    if input_key not in st.session_state:
        st.session_state[input_key] = CONTENT['sample']
    source = st.text_area('Job description', height=220, max_chars=20_000, key=input_key)
    live_enabled = setting('ENABLE_LIVE_AI').lower() == 'true'
    modes = ['Rules baseline'] + (['Live AI (uses paid API)'] if live_enabled else [])
    mode = st.selectbox('Extraction mode', modes)
    if not live_enabled:
        st.caption('Live AI is disabled. Private deployments can enable it with server-side settings; see docs/DEPLOYMENT.md.')
    consent = mode == 'Rules baseline' or st.checkbox('Send this posting to the configured model provider; usage may cost money.')
    if st.button('Analyze posting', type='primary', disabled=not consent, key='analyze_posting'):
        # Clear previous results so a failed run cannot display stale output.
        st.session_state.pop(report_key, None)
        try:
            with st.spinner('Analyzing…'):
                run = analyze_rules(source) if mode == 'Rules baseline' else analyze_live(
                    source, api_key=setting('OPENAI_API_KEY'), model=setting('OPENAI_MODEL'))
            st.session_state[report_key] = run.model_dump()
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error('The model service did not complete the request. Check server configuration, model support, quota, or connectivity. No result was accepted.')
    if report_key in st.session_state:
        run = st.session_state[report_key]
        st.subheader('Last successful report')
        st.caption('Results represent the input at analysis time. Re-run after editing.')
        for warning in run['warnings']:
            st.warning(warning)
        st.dataframe(run['analysis']['requirements'], width='stretch')
        if completed:
            with st.expander('Inspect the JSON report'):
                st.json(run)
        for unknown in run['analysis']['unknowns']:
            st.write('• '+unknown)
        st.download_button('Download JSON report', json.dumps(run, indent=2),
                           file_name='job-analysis.json', mime='application/json')
elif view == 'Failure lab':
    st.header('Find the limits before adding complexity')
    cases = {
        'Mixed priorities': 'Python is required, but Docker is preferred.',
        'Heading scope': 'Required qualifications:\nPython\nFastAPI',
        'Negated experience': 'No Python experience is needed.',
        'Unknown skill': 'Required: COBOL.',
    }
    choice = st.selectbox('Challenge', list(cases))
    st.code(cases[choice], language='text')
    st.json(analyze_rules(cases[choice]).model_dump())
    st.text_area('What failed? What test and correction would you propose?', key='failure_notes')
    st.download_button('Export investigation notes', st.session_state.get('failure_notes',''), 'investigation.md')
else:
    st.header('Your portfolio release checklist')
    tasks = ['Run the tests and benchmark', 'Add an unseen labeled posting',
             'Explain a baseline failure', 'Export a report with source evidence',
             'Document whether live AI was actually tested', 'Publish a reproducible repository',
             'Deploy rules mode without secrets', 'Record a two-minute project walkthrough']
    done = sum(st.checkbox(task, key='portfolio-'+str(i)) for i, task in enumerate(tasks))
    st.progress(done / len(tasks), text=f'{done}/{len(tasks)} self-reported tasks complete')
    st.caption('Progress is session-local and is not a verified certification. Export your checklist for a durable record.')
    checklist = '\n'.join(f"- [{'x' if st.session_state.get('portfolio-'+str(i)) else ' '}] {task}" for i,task in enumerate(tasks))
    st.download_button('Export checklist', checklist, 'portfolio-checklist.md')
