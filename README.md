# FastAPI AI Service Patterns

Production-style FastAPI patterns for LLM-backed services, including structured outputs, streaming, retries, evaluation hooks, guardrails, and observability.

The project is built around a practical production question:

> How should an AI-backed backend service be structured so it is testable, observable, validated, and resilient to model/provider failures?

This repository focuses on the service layer around AI features. It is not another chatbot demo. It shows the backend engineering patterns that make AI functionality easier to operate, test, and evolve.

---

## What This Demonstrates

- FastAPI service design for LLM-backed features
- Pydantic request and response models
- Structured-output validation with schema-specific models
- Provider abstraction with deterministic mock provider
- Optional OpenAI and Anthropic provider adapters
- Streaming response endpoint pattern
- Retry and fallback handling behind a service boundary
- Request ID middleware for trace-style debugging
- Guardrail checks for prompt-injection and unsafe instructions
- Tool/function-calling style endpoint with tool validation
- Evaluation hook for output quality checks
- Secret redaction utilities
- Pytest coverage for API, guardrails, structured output, evaluation, tools, and redaction
- GitHub Actions CI using `uv`

---

## Repository Structure

```text
fastapi-ai-service-patterns/
├── app/
│   ├── main.py                         # FastAPI application factory
│   ├── config.py                       # Environment-driven settings
│   ├── logging.py                      # Structured log helper with redaction
│   ├── middleware.py                   # Request ID middleware
│   ├── models.py                       # Pydantic request/response models
│   ├── providers/
│   │   ├── base.py                     # Provider interface
│   │   ├── factory.py                  # Provider selection
│   │   ├── mock.py                     # Deterministic local provider
│   │   ├── openai_provider.py          # Optional OpenAI adapter
│   │   └── anthropic_provider.py       # Optional Anthropic adapter
│   ├── routes/
│   │   ├── health.py                   # Health endpoint
│   │   ├── structured.py               # Structured-output endpoint
│   │   ├── stream.py                   # Streaming endpoint
│   │   ├── guardrails.py               # Guardrail check endpoint
│   │   ├── evaluations.py              # Evaluation hook endpoint
│   │   └── tools.py                    # Tool/function-calling style endpoint
│   ├── services/
│   │   ├── ai_service.py               # AI orchestration service
│   │   ├── guardrails.py               # Prompt-injection and risk checks
│   │   ├── structured_output.py        # JSON and schema validation
│   │   ├── retry.py                    # Retry wrapper
│   │   ├── evaluation.py               # Output quality checks
│   │   └── tool_registry.py            # Mock tool registry
│   └── utils/
│       ├── ids.py                      # Request ID helper
│       └── redaction.py                # Sensitive-key redaction
├── tests/
├── docs/
├── examples/
├── .github/workflows/ci.yml
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
└── LICENSE
```

---

## Local Setup

### Prerequisites

Install:

- Python 3.12+
- uv

Verify installation:

```bash
python3 --version
uv --version
```

---

## Install Dependencies

From the repository root:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Expected result:

```text
14 passed
```

---

## Run the API Locally

```bash
uv run uvicorn app.main:app --reload
```

The service starts at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"service":"fastapi-ai-service-patterns","status":"ok","version":"0.1.0"}
```

---

## Structured Output Endpoint

This endpoint simulates an LLM-backed API that must return schema-valid structured output.

```bash
curl -X POST http://127.0.0.1:8000/v1/structured-output \
  -H "Content-Type: application/json" \
  -d @examples/structured_support_ticket.json
```

Expected behavior:

```text
- prompt passes guardrails
- mock provider returns deterministic JSON
- response is validated against the support_ticket schema
- evaluation hook verifies the output is schema-valid
- request_id is returned and also attached as x-request-id header
```

Supported schema names:

```text
support_ticket
action_plan
```

---

## Streaming Endpoint

This endpoint demonstrates a FastAPI streaming response pattern while keeping the provider behind a service boundary.

```bash
curl -X POST http://127.0.0.1:8000/v1/stream \
  -H "Content-Type: application/json" \
  -d @examples/stream_request.json
```

---

## Guardrail Check Endpoint

```bash
curl -X POST http://127.0.0.1:8000/v1/guardrails/check \
  -H "Content-Type: application/json" \
  -d @examples/guardrail_blocked.json
```

This endpoint checks for prompt-injection style text and high-risk operational instructions.

Example blocked patterns include:

```text
ignore previous instructions
reveal the system prompt
developer message
exfiltrate
jailbreak
delete all
drop database
send secrets
```

---

## Tool/Function-Calling Pattern

This endpoint demonstrates a controlled tool/function-calling pattern without blindly executing arbitrary actions.

List tools:

```bash
curl http://127.0.0.1:8000/v1/tools
```

Run a tool:

```bash
curl -X POST http://127.0.0.1:8000/v1/tools/run \
  -H "Content-Type: application/json" \
  -d @examples/tool_search_docs.json
```

Default mock tools:

| Tool | Risk | Purpose |
|---|---|---|
| `search_docs` | low | Search internal documentation snippets |
| `create_ticket` | medium | Create a mock support ticket |

---

## Evaluation Hook Endpoint

```bash
curl -X POST http://127.0.0.1:8000/v1/evaluations/run \
  -H "Content-Type: application/json" \
  -d @examples/evaluation_request.json
```

The evaluation hook checks required terms, forbidden terms, and pass/fail score. In a larger system, this pattern could connect to a full EvalOps pipeline.

---

## Provider Configuration

The mock provider is the default and is recommended for local demos and CI.

```env
AI_SERVICE_PROVIDER=mock
AI_SERVICE_FALLBACK_PROVIDER=mock
AI_SERVICE_MODEL=mock-deterministic-v1
```

Optional provider adapters are included for extension work.

Install optional LLM dependencies:

```bash
uv sync --dev --extra llm
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Add API keys only to `.env`:

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

Do not commit `.env`.

---

## Production Engineering Patterns

This project intentionally focuses on backend AI service concerns:

- API contracts before model calls
- Validated responses before returning data to clients
- Provider abstraction instead of direct SDK usage in route handlers
- Deterministic mock provider for tests and CI
- Retry and fallback logic behind the service boundary
- Request IDs for trace-style debugging
- Guardrails before model/tool execution
- Evaluation hooks for regression and quality checks
- Redaction utilities for logs and diagnostics

The main idea: LLM-backed features should be treated as production backend services, not isolated prompt experiments.

---

## Security Notes

This project is designed for local development and portfolio review.

- Do not commit real API keys, tokens, secrets, customer data, or private prompts.
- Keep real credentials only in `.env`.
- `.env` and `.env.*` are ignored by Git.
- `.env.example` is safe to commit because it contains placeholders only.
- The mock provider is recommended for public demos and CI because it does not send data to external LLM APIs.
- Optional OpenAI and Anthropic adapters should be used only with non-sensitive test cases unless proper data-handling controls are in place.
- Guardrails in this repo are intentionally lightweight examples, not a complete safety system.

Recommended production hardening would include:

- Authentication and authorization
- Tenant isolation
- Rate limiting and budget enforcement
- Centralized secret management
- Stronger prompt-injection detection
- Structured audit logging
- OpenTelemetry tracing
- Provider-level cost controls
- Evaluation dataset versioning
- Deployment-specific security review

---

## Development Commands

Run tests:

```bash
uv run pytest
```

Run the API:

```bash
uv run uvicorn app.main:app --reload
```

Run with optional provider dependencies:

```bash
uv sync --dev --extra llm
```

---

## GitHub Actions CI

The repository includes a CI workflow at:

```text
.github/workflows/ci.yml
```

The workflow:

1. Checks out the repository
2. Installs `uv`
3. Installs Python 3.12
4. Installs dependencies with `uv sync --dev`
5. Runs tests with `uv run pytest`

---

## Roadmap

- Add OpenTelemetry tracing for request and provider calls
- Add configurable provider routing rules
- Add provider latency and fallback metrics
- Add stronger structured-output repair loop
- Add JSON Schema export endpoint
- Add integration with an EvalOps report workflow
- Add Dockerfile for local containerized runs
- Add Kubernetes deployment notes

---

## License

This project is licensed under the MIT License. See LICENSE.
