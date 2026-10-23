# Platinum Bot — Current State Snapshot

**Generated:** 2026-10-23T12:07:31+05:30
**Server:** platinum-bot
**Repository:** https://github.com/amansingh111111111-byte/platinum-aman.git
**Branch:** main
**Latest commit:** 98b4859 Merge branch 'main' of https://github.com/amansingh111111111-byte/platinum-aman

## 1. Project Structure
```text
./.gitignore
./client_agent/client.py
./client_agent/client.py.backup_20261023_105021
./client_agent/client.py.bak_20261023_025606
./client_agent/client.py.before_live_gate_20261023_105821
./client_agent/client.py.pre_live_safety_20261023_105957
./client_agent/dhan_token.py
./client_agent/equity_protection.py
./dhan.env
./docs/PLATINUM_BOT_STATE.md
./equity.env
./equity.env.backup_20261023_103504
./equity.env.backup_20261023_104615
./equity.env.backup_20261023_110022
./fno_agent.env.backup_20261023_103504
./fno_agent/DEPLOY.md
./fno_agent/README.md
./fno_agent/__init__.py
./fno_agent/brokers/__init__.py
./fno_agent/brokers/base.py
./fno_agent/brokers/dhan.py
./fno_agent/brokers/kite.py
./fno_agent/deploy/fno-agent.service
./fno_agent/deploy/setup.sh
./fno_agent/executor.py
./fno_agent/fno_journal.db-shm
./fno_agent/fno_journal.db-wal
./fno_agent/holidays.json
./fno_agent/instruments.py
./fno_agent/journal.py
./fno_agent/kite_login.py
./fno_agent/main.py
./fno_agent/main.py.before_env_fix
./fno_agent/market.py
./fno_agent/notifier.py
./fno_agent/requirements.txt
./fno_agent/settings.py
./fno_agent/sizer.py
./login_test.py
./platinum-aman
./position_sizing.py
./services/__init__.py
./services/discord_service.py
./services/email_service.py
./services/fno_parser.py
./services/gemini_service.py
./services/google_sheets_service.py
./services/notion_service.py
./services/regex_service.py
./services/scrip_service.py
./services/telegram_log_service.py
./setup_wizard.py
./signal_queue.py
./tests/test_position_sizing.py
```

## 2. Python Source Files
client_agent/client.py
client_agent/equity_protection.py
fno_agent/__init__.py
fno_agent/brokers/__init__.py
fno_agent/brokers/base.py
fno_agent/brokers/dhan.py
fno_agent/brokers/kite.py
fno_agent/executor.py
fno_agent/instruments.py
fno_agent/journal.py
fno_agent/kite_login.py
fno_agent/main.py
fno_agent/market.py
fno_agent/notifier.py
fno_agent/settings.py
fno_agent/sizer.py
login_test.py
position_sizing.py
services/__init__.py
services/discord_service.py
services/email_service.py
services/fno_parser.py
services/gemini_service.py
services/google_sheets_service.py
services/notion_service.py
services/regex_service.py
services/scrip_service.py
services/telegram_log_service.py
setup_wizard.py
signal_queue.py
tests/test_position_sizing.py

## 3. Dependency Files

### fno_agent/requirements.txt
requests
pandas
pydantic>=2
python-dotenv
pyotp
kiteconnect

## 4. Environment Variable Names (values excluded)

### .env
BROKER=<REDACTED>
DARVAS_SIGNAL_DB=<REDACTED>
FNO_CAPITAL_PER_TRADE=<REDACTED>
FNO_MAX_LOTS=<REDACTED>
FNO_MAX_CONCURRENT_SIGNALS=<REDACTED>
FNO_MAX_SIGNAL_AGE_SEC=<REDACTED>
FNO_SL_TARGET_ENABLED=<REDACTED>
FNO_SL_PCT=<REDACTED>
FNO_TARGET_PCT=<REDACTED>
FNO_ENFORCE_MARKET_HOURS=<REDACTED>
ALLOWED_CHANNELS=<REDACTED>
DHAN_TOKEN_FILE=<REDACTED>

### fno_agent/.env
BROKER=<REDACTED>
DARVAS_SIGNAL_DB=<REDACTED>
FNO_CAPITAL_PER_TRADE=<REDACTED>
FNO_MAX_LOTS=<REDACTED>
FNO_MAX_CONCURRENT_SIGNALS=<REDACTED>
FNO_MAX_SIGNAL_AGE_SEC=<REDACTED>
FNO_SL_TARGET_ENABLED=<REDACTED>
FNO_SL_PCT=<REDACTED>
FNO_TARGET_PCT=<REDACTED>
FNO_ENFORCE_MARKET_HOURS=<REDACTED>
ALLOWED_CHANNELS=<REDACTED>
DHAN_TOKEN_FILE=<REDACTED>
TESTING_MODE=<REDACTED>

### equity.env
BROKER=<REDACTED>
DARVAS_SIGNAL_DB=<REDACTED>
DHAN_TOKEN_FILE=<REDACTED>
EQUITY_PENDING_FILE=<REDACTED>
TESTING_MODE=<REDACTED>
TRADE_AMOUNT_INR=<REDACTED>
DEFAULT_QUANTITY=<REDACTED>
EQUITY_MAX_SIGNAL_AGE_SEC=<REDACTED>
SIGNAL_QUEUE_POLL_SECONDS=<REDACTED>
EQUITY_SL_TARGET_ENABLED=<REDACTED>
EQUITY_SL_PCT=<REDACTED>
EQUITY_TARGET_PCT=<REDACTED>
EQUITY_SL_LIMIT_BUFFER_PCT=<REDACTED>
DHAN_CLIENT_ID=<REDACTED>
DHAN_PIN=<REDACTED>
DHAN_TOTP_SECRET=<REDACTED>

### fno_agent/.env.example
BROKER=<REDACTED>
DRY_RUN=<REDACTED>
DARVAS_SIGNAL_DB=<REDACTED>
SIGNAL_QUEUE_POLL_SECONDS=<REDACTED>
FNO_MAX_CONCURRENT_SIGNALS=<REDACTED>
FNO_MAX_SIGNAL_AGE_SEC=<REDACTED>
ALLOWED_CHANNELS=<REDACTED>
FNO_CAPITAL_PER_TRADE=<REDACTED>
FNO_MAX_LOTS=<REDACTED>
FNO_CHASE_PCT=<REDACTED>
FNO_ENTRY_TIMEOUT_SEC=<REDACTED>
FNO_MIN_DAYS_TO_EXPIRY=<REDACTED>
FNO_SL_LIMIT_BUFFER_PCT=<REDACTED>
FNO_SL_TARGET_ENABLED=<REDACTED>
FNO_SL_PCT=<REDACTED>
FNO_TARGET_PCT=<REDACTED>
FNO_ENFORCE_MARKET_HOURS=<REDACTED>
DHAN_CLIENT_ID=<REDACTED>
DHAN_ACCESS_TOKEN=<REDACTED>
DHAN_PIN=<REDACTED>
DHAN_TOTP_SECRET=<REDACTED>
KITE_API_KEY=<REDACTED>
KITE_API_SECRET=<REDACTED>
KITE_ACCESS_TOKEN=<REDACTED>
TELEGRAM_LOG_BOT_TOKEN=<REDACTED>
TELEGRAM_TEST_LOG_CHAT_ID=<REDACTED>
TELEGRAM_LIVE_LOG_CHAT_ID=<REDACTED>
FNO_TG_BOT_TOKEN=<REDACTED>
FNO_TG_CHAT_ID=<REDACTED>

## 5. Platinum-Related Systemd Services
● darvas-telegram-listener.service loaded activating auto-restart Darvas Telegram Signal Listener (SQLite queue)
 fno-agent.service loaded active running FnO signal execution agent
 trading-client-restart.service loaded inactive dead Daily pre-market restart of the equity trading client
 trading-client.service loaded active running Equity trading signal execution client

## 6. Git Status
## main...origin/main
?? docs/

## 7. Important Safety Notes
- This report records the state observed at generation time.
- Environment-variable values and credentials must not be committed.
- Runtime databases and raw logs require separate review.
- Service presence does not establish that the trading system is safe.
