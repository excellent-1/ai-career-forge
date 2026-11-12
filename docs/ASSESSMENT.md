# Chapter 1 assessment

## Guided practice

Complete the 12 practice challenges. The reader provides immediate feedback and includes its answers in open source. This is learning support, not a secure examination.

## Executable lab

1. Run tests and the synthetic evaluator.
2. Add a new registry alias with a test that demonstrates a false-positive boundary.
3. Build a manually labeled posting not derived from the existing evaluation cases.
4. Capture a mixed-priority error.
5. Propose and implement one parser improvement, documenting any regression.
6. Export a report and explain every field.

## Independent variation

Have another person write a posting with a negated skill, a heading, an unfamiliar tool, and a sentence containing two priorities. Label it before running extraction. Record assistance used. Review unexpected outputs rather than adjusting labels to match the program.

## Completion rubric

- Functional: handles valid and invalid input predictably.
- Evidence: no fabricated quotations accepted by the source check.
- Validation: schema rejects unsupported values and extra fields.
- Reasoning: learner distinguishes structure, grounding, and semantic correctness.
- Reproducibility: another developer can run tests and the demo.
- Communication: learner explains a real failure and its correction.

Passing the small included dataset is not a claim of general extraction accuracy. Quote validity alone is not a claim of semantic correctness. Live AI checks are mocked in automated tests; test against the real service separately if enabling it.
