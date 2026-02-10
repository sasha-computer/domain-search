## Codebase Patterns
- Project uses `uv` for Python package management; run with `uv run python main.py`
- Package structure: `domain_search/` for source, `tests/` for tests
- TLD cache stored at `~/.cache/domain-search/tlds.txt` with 1-day expiry
- Tests use `unittest.mock.patch` to mock external calls (httpx, filesystem)
- Async tests use `@pytest.mark.asyncio` with `AsyncMock` for async resolver mocking
- DNS checker uses `dns.asyncresolver.Resolver` with `asyncio.Semaphore` for concurrency control
- Run tests with `uv run pytest tests/ -v`

---

## 2026-02-10 - US-001
- Implemented TLD list fetching from IANA (https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
- Local file caching in `~/.cache/domain-search/tlds.txt` with 1-day max age
- Parses correctly: skips comments, lowercases, handles IDN/punycode TLDs
- Reports 1,437 TLDs found
- Files changed: `domain_search/__init__.py`, `domain_search/tld_list.py`, `main.py`, `tests/test_tld_list.py`, `pyproject.toml`
- **Learnings for future iterations:**
  - `uv init` creates a `main.py` with a hello-world stub - overwrite it
  - IANA TLD list has ~1,437 entries (comment line at top starting with `#`)
  - `httpx` is used for HTTP (async-capable for later stories)
  - `pytest-asyncio` added as dev dep for future async tests (US-002)
---

## 2026-02-10 - US-002
- Implemented async DNS availability checker in `domain_search/dns_checker.py`
- Checks NS and SOA records to classify domains as registered/available/unknown
- Uses `asyncio.Semaphore` for configurable concurrency (default 50)
- Handles timeouts gracefully (marks as "unknown")
- Files changed: `domain_search/dns_checker.py`, `tests/test_dns_checker.py`, `pyproject.toml`, `progress.md`, `prd.json`
- **Learnings for future iterations:**
  - When patching async functions in the same module, mock at the `dns.asyncresolver.Resolver` class level rather than patching `check_domain` directly (closure captures the function reference)
  - `dns.resolver.LifetimeTimeout` is a separate exception from `dns.exception.Timeout` — catch both for robust timeout handling
  - `dnspython` async resolver: use `resolver.resolve(domain, rdtype)` with await
  - `DomainStatus` enum and `DomainResult` dataclass provide clean typed results for downstream consumers (US-003, US-005, US-006)
---
