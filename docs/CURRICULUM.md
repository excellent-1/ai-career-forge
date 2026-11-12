# AI Career Forge — curriculum roadmap

**Status:** Chapter 1 is implemented as a working draft. Chapters 2–30 are planned. Each chapter produces a deployable demonstration with a portfolio package. Public demos can use recorded/simulated model responses; live inference and heavy infrastructure may require separate resources.

| Chapter | Project | Main technologies and skills |
| --- | --- | --- |
| 1 | Job Requirements Analyzer — implemented | Python, Streamlit, Pydantic, optional structured outputs, evidence checks |
| 2 | Prompt Experiment Studio | Prompt versions, datasets, rubrics, latency, cost |
| 3 | Typed AI API Gateway | FastAPI, async I/O, provider adapters, timeouts |
| 4 | Full-Stack AI Interview Coach | TypeScript, React/Next.js or Angular, cancellation, APIs |
| 5 | Document Intake Inspector | Extraction, OCR boundaries, metadata, provenance |
| 6 | Search Strategy Lab | Keyword/vector/hybrid search, embeddings, metrics |
| 7 | Source-Cited Knowledge Assistant | LangChain, RAG, citations, abstention |
| 8 | Context Engineering Observatory | Context selection, budgets, compression, inspection |
| 9 | Memory Lifecycle Manager | Task state, expiration, correction, user isolation |
| 10 | PostgreSQL/pgvector Explorer | SQL, models, indexes, query analysis |
| 11 | Business Workflow Tool Server | MCP, typed tools, permissions, validation |
| 12 | LangGraph Workflow Agent | State, graphs, transitions, stop conditions |
| 13 | Review and Approval Platform | Checkpoints, previews, pause/resume, cancellation |
| 14 | Failure Recovery Simulator | Backoff, retry budgets, idempotency, compensation |
| 15 | Multi-Agent Investigation Studio | Handoffs, concurrency, coordination, baseline comparison |
| 16 | Enterprise Integration Agent | REST/events, Java/Spring, C#/Semantic Kernel alternatives |
| 17 | Agent Evaluation Platform | Datasets, graders, repeated runs, regressions |
| 18 | AI Security Arena | Injection defenses, untrusted data, tool boundaries |
| 19 | Trace and Incident Explorer | Structured logs, traces, correlation, replay |
| 20 | Model Routing Optimizer | Quality gates, caching, cost, latency, fallback |
| 21 | AI Release Dashboard | Docker, GitHub Actions, releases, rollback |
| 22 | Cloud Reliability Simulator | AWS/Azure architecture, Linux, Kubernetes, Terraform |
| 23 | Agentic Data Quality Platform | SQL, pandas, profiling, lineage, reviewed corrections |
| 24 | BOM Investigation Agent | Hierarchies, revisions, recursion, XML/JSON, reconciliation |
| 25 | Infrastructure Incident Assistant | Logs, network/service configuration, diagnostic tools |
| 26 | DFW Job Intelligence | Supported ingestion, deduplication, date verification, geography |
| 27 | Skills-to-Jobs Evidence Matcher | Requirement classification, evidence strength, gaps |
| 28 | Interactive Training Platform | Lesson schemas, exercises, progress, portfolio publishing |
| 29 | Adaptive Learning and Interview Defense | Prerequisites, remediation, unseen tasks, grading calibration |
| 30 | AI Career Forge DFW Capstone | Integrated training, evidence, job freshness, matching, evaluations |

## Common chapter structure

Mission → explanation → multiple choice → fill-in-the-blank → fill-in-code → fix-the-code → guided lab → unseen assessment → portfolio release → interview defense.

## Demonstration deployment

Python dashboards target Streamlit Community Cloud; lightweight APIs target Render Free; browser interfaces target static hosting. Database-backed chapters include a reproducible local Docker environment and a captured-result public demonstration when a live free database is unavailable. Cloud/Kubernetes chapters publish simulators and local execution evidence; paid cloud deployment is optional. Arbitrary submitted code must run in an isolated environment, not the public application process.

Every release includes source, instructions, meaningful validation, architecture decisions, a failure investigation, and an honest limitations statement. Training completion does not establish professional experience or guarantee employment.
