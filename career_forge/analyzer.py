"""Small, inspectable baseline; this is deliberately NOT an LLM."""
import hashlib
import re
from .models import AnalysisRun, JobAnalysis, Requirement

MAX_INPUT = 20_000
SKILLS = {
    "Python": r"\bpython\b", "TypeScript": r"\btypescript\b",
    "JavaScript": r"\bjavascript\b", "Java": r"\bjava\b",
    "C#": r"(?<!\w)c\#(?!\w)", "SQL": r"\bsql\b",
    "FastAPI": r"\bfastapi\b", "Pydantic": r"\bpydantic\b",
    "LangChain": r"\blangchain\b", "LangGraph": r"\blanggraph\b",
    "MCP": r"\bmcp\b|\bmodel context protocol\b",
    "RAG": r"\brag\b|\bretrieval[- ]augmented generation\b",
    "PostgreSQL": r"\bpostgres(?:ql)?\b", "pgvector": r"\bpgvector\b",
    "Docker": r"\bdocker\b", "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "AWS": r"\baws\b|\bamazon web services\b",
    "Azure": r"\bazure\b", "React": r"\breact\b",
    "Angular": r"\bangular\b", "Next.js": r"\bnext\.js\b",
    "Git": r"\bgit\b", "GitHub Actions": r"\bgithub actions\b",
    "Spring Boot": r"\bspring boot\b", "Terraform": r"\bterraform\b",
    "PyTorch": r"\bpytorch\b", "Databricks": r"\bdatabricks\b",
    "PySpark": r"\bpyspark\b",
}


def validate_input(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Paste a job description before analyzing.")
    if len(text) > MAX_INPUT:
        raise ValueError(f"Use at most {MAX_INPUT:,} characters.")
    return text


def priority_for(text: str) -> str:
    # Ambiguous requirements remain unspecified; no guessed certainty.
    if re.search(r"\b(?:not required|optional|nice to have|preferred|bonus)\b", text, re.I):
        return "preferred"
    if re.search(r"\b(?:required|must|mandatory|minimum)\b", text, re.I):
        return "required"
    return "unspecified"


def analyze_rules(text: str) -> AnalysisRun:
    text = validate_input(text)
    requirements = []
    # Preserve exact source substrings, including punctuation and casing.
    for span in re.split(r"\n|(?<=[.!?])\s+", text):
        evidence = span.strip()
        for skill, pattern in SKILLS.items():
            if re.search(pattern, evidence, re.I):
                item = Requirement(skill=skill, priority=priority_for(evidence), evidence=evidence)
                if item not in requirements:
                    requirements.append(item)
    return AnalysisRun(
        mode="rules", source_sha256=hashlib.sha256(text.encode()).hexdigest(),
        analysis=JobAnalysis(requirements=requirements, unknowns=[
            "Salary, location, years of experience, and unstated requirements are not inferred.",
            "Priority headings, negation, mixed clauses, and unfamiliar skills need human review.",
        ]),
        warnings=["Rules-based baseline: keyword mentions are not proof of a hiring requirement."],
    )


def validate_evidence(analysis: JobAnalysis, source: str) -> list[str]:
    """Reject unsupported quotes; exact quotation is necessary, not semantic proof."""
    for requirement in analysis.requirements:
        if requirement.evidence not in source:
            raise ValueError(f"Evidence was not found verbatim for {requirement.skill}.")
    return ["Quotes verified against input; skill interpretation and priority still need review."]
