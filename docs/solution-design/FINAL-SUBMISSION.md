# Noir — Final Submission

## 1. Project Overview

**Noir Technologies** presents **Noir**, an AI-Powered DevOps & Incident Intelligence Platform designed to accelerate software incident investigation while keeping consequential remediation decisions under human control.

Noir uses a multi-agent architecture in Microsoft Foundry to separate incident coordination, code/deployment investigation, observability analysis, and resolution recommendation.

The V1 implementation uses synthetic incident evidence so the complete investigation workflow can be demonstrated safely without exposing production systems or secrets.

## 2. Business Problem

Software incidents often require engineers to correlate information across multiple sources: incident records, source-code changes, deployments, configuration, logs, metrics, traces, alerts, and historical incidents.

A conventional investigation can be slow because engineers must manually gather and correlate this evidence before determining the likely cause and next action.

Noir addresses this problem by assigning distinct investigation responsibilities to specialised agents and then synthesising their findings into an evidence-based recommendation.

## 3. Intended Users

Primary users include:

- Software engineers
- DevOps and platform engineers
- Site Reliability Engineers
- Incident commanders
- Engineering leads
- Technical operations teams

## 4. Why a Multi-Agent Solution?

A single general-purpose agent could attempt the entire investigation, but that approach creates weaker separation of responsibilities and makes it harder to evaluate whether conclusions are supported by the correct evidence.

Noir separates the work into specialised roles:

1. **Incident Coordinator Agent** — coordinates the investigation.
2. **Code Intelligence Agent** — investigates code, configuration, commits, pull requests, and deployment changes.
3. **Observability & Incident Investigation Agent** — investigates logs, metrics, traces, alerts, telemetry, and historical signals.
4. **Resolution & Recommendation Agent** — correlates evidence and determines the safest next action.

This architecture provides clearer responsibility boundaries, more structured evidence exchange, better traceability, and targeted evaluation of individual capabilities.

## 5. Agent Architecture

```text
Incident
   |
   v
Incident Coordinator
   |
   +--> Code Intelligence Agent
   |
   +--> Observability & Incident Investigation Agent
   |
   +--> Resolution & Recommendation Agent
```

The intended investigation pattern is:

```text
Investigate -> Correlate -> Decide -> Verify
```

The Coordinator is responsible for routing and consolidating investigation information. It does not independently perform deep code or observability analysis, and it does not execute production remediation.

## 6. Agent Responsibilities

### Incident Coordinator Agent

The Coordinator is the workflow entry point. It:

- receives incident context
- identifies affected service, severity, symptoms, timing, and recent changes
- determines required investigations
- delegates specialist work
- collects findings
- identifies evidence gaps or conflicts
- routes consolidated evidence toward resolution
- preserves uncertainty when evidence is insufficient
- ensures consequential remediation requires human approval

### Code Intelligence Agent

The Code Intelligence Agent answers:

> What changed that could explain the incident?

It investigates:

- source code
- configuration
- commits
- pull requests
- changed files
- dependencies
- deployment versions
- repository documentation

For V1, it uses the repository evidence file:

`data/repositories/noir-operations/release-v2.8.4.json`

### Observability & Incident Investigation Agent

The Observability Agent answers:

> What is the system telling us?

It investigates:

- logs
- metrics
- traces
- alerts
- telemetry
- deployment timing
- service health
- historical correlations

V1 uses synthetic observability evidence stored under:

`data/logs/`

### Resolution & Recommendation Agent

The Resolution Agent answers:

> What does the evidence indicate, and what should happen next?

It:

- correlates specialist findings
- assesses likely root cause
- distinguishes evidence from inference
- assigns confidence
- considers alternative explanations
- recommends a safe next action
- identifies human approval requirements
- defines verification steps
- escalates when evidence is insufficient

It does not execute production remediation.

## 7. Tools and Data Sources

V1 includes read-only investigation tooling and synthetic evidence.

### Repository Evidence

Located under:

`data/repositories/noir-operations/`

Used to represent:

- releases
- commits
- configuration changes
- pull requests
- changed files

### Observability Evidence

Located under:

`data/logs/`

Used to represent:

- application logs
- metrics
- traces
- alerts
- historical correlations

### Knowledge Sources

Located under:

`data/knowledge/`

V1 includes:

- historical incident evidence
- database troubleshooting guidance

### Incident Data

Located under:

`data/incidents/`

Contains structured incident records for the demonstration scenarios.

## 8. Supporting Tool API

A FastAPI-based read-only tool service is included under:

`tools/api/`

Available endpoints provide access to:

- incident details
- repository release evidence
- observability evidence
- historical incidents
- database troubleshooting guidance
- service health

The tool service is designed for investigation rather than production mutation.

## 9. Hero Scenario — INC-1042

**INC-1042 — Customer Orders API HTTP 500 Errors Following Deployment**

The incident affects the Customer Orders API following production deployment `v2.8.4`.

The evidence shows:

- database connection pool maximum connections changed from 50 to 10
- connection timeout changed from 5000 ms to 1000 ms
- the change was introduced in the deployment
- HTTP 500 rate increased from 0.2% to 18.7%
- database connection errors increased from 1 to 46 per minute
- p95 latency increased from 180 ms to 920 ms
- logs show database connection pool exhaustion
- traces show connection acquisition timeouts
- alerts identify HTTP 500 and connection-pool exhaustion
- historical incident `INC-0978` has high similarity

The Resolution Agent correlated these signals and identified the database connection-pool configuration introduced in `v2.8.4` as the most likely root cause.

The recommended action is to restore the approved configuration or roll back the relevant change, subject to human approval.

Verification includes confirming that database connection errors, HTTP 500 rates, latency, and failed database spans return toward baseline.

## 10. Failure / Escalation Scenario — INC-1051

**INC-1051 — Intermittent Customer Portal Failure With Insufficient Evidence**

This scenario intentionally provides insufficient evidence.

Available information includes:

- intermittent portal errors
- insufficient telemetry sample size
- no consistent failing endpoint
- no reliable stack trace
- no traces
- no alerts
- no historical correlation
- no confirmed deployment correlation

The expected behaviour is **not** to invent a root cause.

The Resolution Agent correctly preserves uncertainty and identifies that further investigation or human escalation is required.

The required statement for an insufficient-evidence case is:

> Evidence is insufficient for a reliable root-cause determination.

This scenario demonstrates a critical safety property of the solution: uncertainty is preserved instead of being replaced with an unsupported technical claim.

## 11. Human Approval and Escalation

Noir separates investigation from consequential action.

For incidents where a remediation such as rollback or configuration restoration is recommended:

- the agent provides the recommendation
- the evidence and confidence are presented
- human approval is required before production remediation
- verification steps are defined after the approved action

When evidence is insufficient:

- the agent does not fabricate a root cause
- evidence gaps are identified
- additional investigation or human escalation is recommended

## 12. Evaluation

A dedicated Foundry evaluation was created:

**Noir V1 Resolution Agent Evaluation**

Configuration:

- Target: `resolution-recommendation`
- Scope: Individual turns
- Frequency: One time
- Dataset: `noir-v1-incident-evaluation-v2`
- Judge model: `gpt-4.1-mini`

Evaluated criteria:

- Task Completion
- Task Adherence
- Relevance
- Groundedness

### V1 Evaluation Result

The completed evaluation achieved:

| Evaluator | Result |
|---|---:|
| Overall | **100% — 12/12** |
| Task Completion | **100% — 3/3** |
| Task Adherence | **100% — 3/3** |
| Relevance | **100% — 3/3** |
| Groundedness | **100% — 3/3** |

The dataset contains three scenarios:

- successful investigation
- insufficient evidence
- no evidence

The evaluation therefore tests both successful reasoning and refusal to make unsupported root-cause claims.

## 13. Observability and Tracing

Microsoft Foundry tracing was used to inspect agent execution.

A successful Code Intelligence investigation produced a trace containing:

- agent invocation
- model call
- GitHub evidence retrieval
- resulting agent output

Trace evidence is retained as a V1 demonstration artifact.

Tracing supports the project's requirement for visibility into agent execution, tool usage, and investigation behaviour.

## 14. Security and Responsible AI

V1 follows these principles:

- read-only investigation where possible
- least-privilege access
- human approval for consequential remediation
- no production secrets in the repository
- synthetic incident and observability data
- evidence-grounded reasoning
- explicit uncertainty
- escalation when evidence is insufficient
- no autonomous production remediation

## 15. V1 Limitations

The V1 implementation intentionally focuses on a demonstrable, safe evaluation workflow.

Current limitations include:

- synthetic evidence rather than live production telemetry
- synthetic repository evidence for the demonstration
- limited external system integration
- A2A specialist connectivity is demonstrated for the working handoff path, while the complete autonomous multi-agent orchestration is not treated as production-complete in V1
- production remediation is intentionally not automated

These limitations do not change the core V1 demonstration: specialised agents can investigate distinct evidence domains, produce structured findings, and support evidence-based resolution decisions.

## 16. Future Improvements

Potential V2 improvements include:

- live GitHub and observability integrations
- reliable end-to-end A2A orchestration
- live incident-management integration
- richer knowledge retrieval
- automated post-remediation verification
- broader evaluation datasets
- recurring quality monitoring
- production-grade authentication and deployment
- deeper historical incident correlation

These improvements are deliberately outside the V1 submission scope.

## 17. Technology Stack

- Microsoft Foundry
- Microsoft Foundry Agent Service
- MAI-Thinking-1
- gpt-4.1-mini for evaluation judging
- FastAPI
- Python
- GitHub
- JSON / JSONL
- Microsoft Foundry tracing and evaluation

## 18. Repository Structure

```text
ai-powered-devops-incident-intelligence/
├── .github/
├── agents/
│   ├── coordinator/
│   ├── code-intelligence/
│   ├── observability/
│   └── resolution/
├── tools/
│   ├── repository/
│   ├── observability/
│   ├── knowledge/
│   ├── incidents/
│   └── api/
├── data/
│   ├── incidents/
│   ├── logs/
│   ├── repositories/
│   └── knowledge/
├── evaluation/
│   ├── datasets/
│   ├── scenarios/
│   └── results/
├── architecture/
│   ├── diagrams/
│   └── decisions/
├── demo/
│   ├── scenarios/
│   └── screenshots/
└── docs/
    ├── solution-design/
    ├── architecture/
    ├── agents/
    ├── workflows/
    ├── evaluation/
    ├── observability/
    ├── security/
    └── demo/
```

## 19. V1 Success Criteria

The V1 solution is considered complete when it can demonstrate:

1. A realistic software incident investigation scenario.
2. Multiple specialised agents with distinct responsibilities.
3. Separation of code and observability investigation.
4. Evidence-based resolution recommendations.
5. Human approval for consequential remediation.
6. Correct handling of insufficient evidence.
7. Working investigation tooling and synthetic evidence.
8. Microsoft Foundry tracing.
9. A completed evaluation with measurable results.
10. A recorded demonstration and supporting documentation.

## 20. Submission Summary

Noir demonstrates how a multi-agent architecture can improve software incident investigation by separating evidence gathering and analysis responsibilities while maintaining human oversight over consequential decisions.

The V1 implementation demonstrates the hero incident `INC-1042`, where multiple evidence sources converge on a likely database connection-pool configuration issue, and the failure scenario `INC-1051`, where insufficient evidence correctly leads to uncertainty and escalation.

The completed Foundry evaluation achieved **100% across Task Completion, Task Adherence, Relevance, and Groundedness**, providing measurable evidence that the Resolution Agent behaved as intended across the three V1 evaluation cases.

**Project:** Noir  
**Organisation:** Noir Technologies  
**Solution:** AI-Powered DevOps & Incident Intelligence Platform  
**Repository:** `ai-powered-devops-incident-intelligence`
