# Deployment guide

## A. Free interactive book: GitHub Pages

1. Push the complete repository to GitHub.
2. Open repository Settings → Pages.
3. Under Build and deployment, choose GitHub Actions as the source.
4. Open Actions → Publish interactive chapter → Run workflow; select main.
5. Wait for a successful deployment and open the URL shown in the deployment output. It typically resembles `https://YOUR_GITHUB_USERNAME.github.io/ai-career-forge/`; this is an example, not an already deployed URL.
6. Check lesson navigation, practice feedback, analyzer export, and narrow-screen layout.

The workflow publishes `web/`. Paths are relative for project-site compatibility. This edition is entirely browser-side and has no credentials, backend, job crawling, or live AI. Subsequent changes under web/ can be published by re-running the workflow.

## B. Free Python project: Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/ and connect your GitHub repository.
2. Choose Create app and select the repository, main branch, and `app.py` entrypoint.
3. Choose a supported Python version; Python 3.12 was used for draft verification.
4. Leave secrets empty for the free rules baseline.
5. Deploy and test the Analyzer and Failure lab workspaces.

The runtime installs root `requirements.txt`. Free hosting is resource-limited and may sleep. This draft is a portfolio demonstration, not a production service. Server session data can reset; export reports/checklists to retain them. The browser reader separately uses localStorage.

## Optional private live AI mode

Do not enable provider-funded inference on an unrestricted public demo. This draft has no account-level authorization, distributed rate limit, or billing controls. Use private access, a controlled session, and provider spending controls before enabling it.

In Streamlit's server secrets (or local `.streamlit/secrets.toml`), configure:

```toml
ENABLE_LIVE_AI = "true"
OPENAI_API_KEY = "YOUR_SERVER_SIDE_KEY"
OPENAI_MODEL = "YOUR_STRUCTURED_OUTPUT_CAPABLE_MODEL"
```

Select a model available in your account that supports the SDK's structured parse operation. Model availability and pricing can change. The UI requires an explicit consent checkbox before a live request. The posting is then transmitted to the model provider. Do not submit confidential material without appropriate authorization.

The adapter uses the OpenAI Python SDK, a 30-second timeout, no automatic retries, schema validation, refusal handling, and exact quote verification. It does not silently fall back to a baseline after a provider error. A model response can still be semantically wrong even after validation.

Never commit `.streamlit/secrets.toml`, `.env`, or credentials. `.env.example` is documentation; no automatic dotenv loading is implemented.

## Official references

- Streamlit deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Streamlit dependencies: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- OpenAI structured outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- GitHub Pages workflow publishing: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

Free hosting does not imply free inference. No deployment is performed by extracting this repository.
