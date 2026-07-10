---
name: quality-assurance
description: Quality assurance workflows — test-driven development, formal evaluation frameworks for agent sessions, and comprehensive verification loops. Use when writing features, fixing bugs, evaluating agent performance, or verifying task completion.
category: devops
---

# Quality Assurance

Ensure correctness through structured testing, evaluation, and verification — from unit tests to agent session audits.

## When to Activate

- Writing new features or fixing bugs (TDD workflow)
- Evaluating agent session quality and output correctness
- Verifying a task is fully complete before declaring done
- User says "test", "verify", "evaluate", "check", "quality gate", or "did it work"

---

## Test-Driven Development (TDD)

### The Red-Green-Refactor Loop

1. **Red:** Write a failing test that describes the desired behavior
2. **Green:** Write the minimum code to make the test pass
3. **Refactor:** Clean up the code while keeping tests green

### Workflow

1. **Understand the requirement** — what should this code do?
2. **Write a failing test** — assert the expected output for a given input
3. **Run the test** — confirm it fails for the right reason
4. **Write production code** — minimal implementation to pass
5. **Run all tests** — confirm the new test passes, nothing else breaks
6. **Refactor** — improve structure without changing behavior
7. **Repeat** for next requirement

### Test Structure (Arrange-Act-Assert)

```python
def test_user_can_login():
    # Arrange
    user = create_user(email="test@example.com", password="secret")
    
    # Act
    result = login(email="test@example.com", password="secret")
    
    # Assert
    assert result.is_authenticated
    assert result.token is not None
```

### What to Test

- **Happy path:** Correct input produces correct output
- **Edge cases:** Empty input, maximum values, boundary conditions
- **Error cases:** Invalid input produces appropriate errors
- **Integration:** Components work together correctly
- **Regression:** Bug fixes include tests that would catch the bug if reintroduced

### When NOT to TDD

- Spikes / prototypes (throwaway code)
- Purely exploratory work where requirements are unknown
- Configuration / infrastructure code (use integration tests instead)

---

## Formal Evaluation Framework

Systematic evaluation of agent sessions against predefined criteria.

### Evaluation Dimensions

| Dimension | Questions |
|-----------|-----------|
| **Correctness** | Did the agent produce factually correct output? |
| **Completeness** | Were all requirements addressed? |
| **Efficiency** | Were steps taken in optimal order? |
| **Safety** | Were there any harmful or risky actions? |
| **Communication** | Was the explanation clear and appropriate? |
| **Tool use** | Were the right tools chosen and used correctly? |

### Scoring

- **Binary pass/fail** per dimension for clear criteria
- **Rubric-based** (1-5 scale) for nuanced evaluation
- **Threshold:** All critical dimensions must pass; nice-to-haves can fail with justification

### Process

1. Define evaluation criteria before the session starts
2. Record the session (transcript, tool calls, outputs)
3. Score each dimension independently
4. Aggregate scores and identify patterns
5. Feed results back into prompt engineering or tool configuration

---

## Verification Loop

Before declaring a task "done", run through this checklist:

### Functional Verification

- [ ] The primary requirement is satisfied
- [ ] Edge cases are handled
- [ ] Error paths return appropriate messages/codes
- [ ] No regressions in existing functionality
- [ ] Integration points work correctly

### Code Quality

- [ ] Code follows project conventions
- [ ] No debugging code left behind
- [ ] No hardcoded secrets or environment-specific values
- [ ] Documentation/comments updated
- [ ] Tests added or updated

### Operational Verification

- [ ] Deployment requirements documented
- [ ] Environment variables/configs listed
- [ ] Rollback plan considered
- [ ] Monitoring/alerting in place (if applicable)

### Agent-Specific Verification

- [ ] Tool outputs were verified, not assumed correct
- [ ] File changes were reviewed before applying
- [ ] No infinite loops or repeated failed calls
- [ ] Context was compacted if session was long
- [ ] User was asked before destructive actions

### The "Sleep On It" Test

If possible, revisit the solution after a short break. Fresh eyes catch:
- Obvious mistakes you were too close to see
- Simpler approaches you missed
- Missing test cases
- Documentation gaps

---

## Pitfalls

- **Testing the implementation, not the behavior.** Tests should specify "what", not "how".
- **Brittle tests.** Mock at the right level; don't tie tests to internal structure.
- **Evaluation without criteria.** Always define what "good" means before measuring.
- **Verification fatigue.** Long checklists get skipped; automate what you can.
- **Declaring done too early.** The last 10% of verification often finds the most bugs.

## Related Skills

- `software-engineering` — Coding patterns and standards that support quality
- `agent-workflow` — Multi-agent orchestration and debugging
- `e2e-testing` — Playwright end-to-end testing patterns
