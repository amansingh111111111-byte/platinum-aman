# Platinum Bot

Automated trading project with separate equity and Futures & Options (F&O)
workers, broker adapters, signal parsing, a local SQLite signal queue,
position sizing, protection logic, and supporting integrations.

## Project structure

- `client_agent/` — equity execution client and protection logic.
- `fno_agent/` — F&O worker, broker adapters, executor, sizing, market
  utilities, journal, and deployment files.
- `services/` — signal parsers and supporting integrations.
- `signal_queue.py` — SQLite signal queue.
- `position_sizing.py` — position-sizing logic.
- `setup_wizard.py` — configuration/setup helper.
- `tests/` — automated tests.
- `docs/` — project state and operational documentation.

## Architecture

Equity and F&O execution are separate workers. They depend on their
configuration, broker adapters, and signal-queue setup.

Telegram logging integrations do not necessarily implement Telegram
message ingestion. Verify the listener implementation and deployment
before assuming that messages reach the queue.

## Setup and deployment

Review these files before running deployment commands:

- `fno_agent/README.md`
- `fno_agent/DEPLOY.md`
- `fno_agent/deploy/setup.sh`
- `fno_agent/deploy/fno-agent.service`
- `fno_agent/requirements.txt`

Only run scripts after reviewing their effects on the system.

## Configuration and secrets

Use example configuration files as templates. Never commit real `.env`
files, broker credentials, access tokens, Telegram session files, private
keys, runtime databases, or raw logs.

Keep testing/dry-run mode enabled until message ingestion, parsing,
queue handling, risk controls, broker responses, and recovery procedures
have been verified.

## Testing

Use the project's Python virtual environment if available:

    .venv/bin/python -m pytest -q

or:

    venv/bin/python -m pytest -q

Record actual test results in `docs/TESTING.md`.

## Operational safety

- Verify that all intended workers use the correct absolute queue path.
- Inspect claimed or uncertain signals before attempting replay.
- A successful function call does not prove that an order was filled.
- Do not enable live trading before the end-to-end workflow is tested.
- Do not modify another trading deployment while working on Platinum Bot.

## Documentation

See `docs/PLATINUM_BOT_STATE.md` for the initial environment snapshot.
Maintain architecture, configuration, deployment, testing, and recovery
documentation as the implementation evolves.
