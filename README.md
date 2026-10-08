# Floppydata Python SDK

Typed client for the [Floppydata](https://floppydata.com) Client API v2: Web Data
(search and page fetching), rotating and static proxies, Cloud Browser sessions,
and account balances and usage.

```bash
pip install floppydata
```

Requires Python 3.10 or newer. Sync and async clients, Pydantic response models,
and full type hints (checked with mypy and Pyright).

## Quick start

Create a Client API key at https://app.floppydata.com/api-keys.

```python
from floppydata import FloppyData

fd = FloppyData(api_key="...")  # or set FLOPPYDATA_API_KEY

balances = fd.account.get_account_balances()
print(balances.web_data.requests.remaining)

page = fd.web_data.fetch_web_data(url="https://example.com", difficulty="auto")
print(len(page.html))
```

Keep the key on the server: anyone holding it can spend your balance.

Methods are grouped by product: `fd.web_data`, `fd.rotating_proxy`,
`fd.static_proxy`, `fd.proxy`, `fd.account` and `fd.cloud_browser`. Every
method and its parameters are listed in [reference.md](reference.md).
Parameters are keyword arguments in snake_case; nested objects are plain dicts:

```python
session = fd.cloud_browser.create_browser_session(
    proxy={"type": "residential", "location": {"country_code": "US"}},
    persist={"ttl_seconds": 3600},
)
```

## Async

```python
import asyncio
from floppydata import AsyncFloppyData

async def main() -> None:
    fd = AsyncFloppyData()
    proxies = await fd.static_proxy.list_static_proxies()
    print(len(proxies.items))

asyncio.run(main())
```

## Errors

Non-2xx responses raise a subclass of `floppydata.core.ApiError`, one per
documented status, with the parsed error body:

```python
from floppydata import PaymentRequiredError, BadGatewayError
from floppydata.core import ApiError

try:
    fd.web_data.fetch_web_data(url="https://example.com")
except PaymentRequiredError as error:
    print(error.body.error.code)  # "insufficient_balance"
except BadGatewayError as error:
    print(error.body.error.details.service_status)
except ApiError as error:
    print(error.status_code, error.body)  # body is text if it was not JSON
```

| Status | Exception |
| --- | --- |
| 400 | `BadRequestError` |
| 401 | `UnauthorizedError` |
| 402 | `PaymentRequiredError` |
| 403 | `ForbiddenError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 500 | `InternalServerError` |
| 502 | `BadGatewayError` |

`error.body.error.code` is one of the documented `ApiErrorCode` values.

## Retries and timeouts

Requests are **not** retried by default: the API has no idempotency keys, so a
retried `create_browser_session` or `create_rotating_proxy_subuser` could create
a duplicate. Opt in when that is acceptable:

```python
fd = FloppyData(max_retries=2, timeout=30)
fd.account.get_account_balances(request_options={"max_retries": 3})
```

## Cloud Browser

`create_browser_session` returns a `connect_url` for Playwright or Puppeteer:

```python
from playwright.sync_api import sync_playwright

session = fd.cloud_browser.create_browser_session(persist={"ttl_seconds": 3600})
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(session.connect_url)
    ...
fd.cloud_browser.stop_browser_session(session.id)
```

Pass `settings={"id": ...}` from an earlier persistent session to restore its
fingerprint, proxy IP, cookies and storage. To browse through one of your
static IPs, pass `proxy={"type": "static", "ip": ...}` with an `ip` from
`fd.static_proxy.list_static_proxies()`.

## Configuration

```python
FloppyData(
    api_key="...",                          # default: FLOPPYDATA_API_KEY
    base_url="https://api.floppydata.net",  # default
    timeout=60,                             # seconds, default 60
    max_retries=0,                          # default 0
    httpx_client=httpx.Client(...),         # e.g. for a proxy or custom transport
)
```

## Examples

[`examples/`](examples) has runnable end-to-end flows for each product:

| File | Flow |
| --- | --- |
| `web_data.py` | Check balance, search, fetch top results, report usage |
| `rotating_proxy.py` | Create a subuser, pick a location, build and verify a connection, read usage and request history |
| `static_proxy.py` | List static IPs and health-check each one concurrently (async client) |
| `account.py` | Balances and usage across products |
| `cloud_browser.py` | Persistent session with Playwright, live view, reuse saved state, clean up |
| `error_handling.py` | Typed errors, `settings_in_use` recovery |

```bash
uv sync
FLOPPYDATA_API_KEY=... uv run python examples/account.py
```

`web_data.py`, `rotating_proxy.py`, `cloud_browser.py` and `error_handling.py`
spend Web Data requests, proxy traffic or browser time.

## Versioning

The SDK follows semantic versioning, independently of the API version. While it
is `0.x`, minor versions may contain breaking changes. See [CHANGELOG.md](CHANGELOG.md).

## Development

The package under `src/floppydata` is generated from the API's OpenAPI spec with
[Fern](https://github.com/fern-api/fern)'s open-source Python generator. Do not
edit it: change `fern/` (generator config and overrides) or the API itself.

```bash
curl -fsSL https://api.floppydata.net/v2/openapi.json -o openapi/v2.json
scripts/generate.sh   # needs Node.js and Docker
uv run ruff check . && uv run mypy && uv run pytest
```

`scripts/generate.sh` also disables the generator's default retries and adds the
`py.typed` marker. With rootless Podman on an SELinux system, run it with
`DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock` and a `CONTAINERS_CONF`
file containing `[containers]` / `label = false`.

CI fails when `src/floppydata` does not match the committed spec. On `main`, it
also runs every example against a test environment set by the
`FLOPPYDATA_STAGING_BASE_URL` and `FLOPPYDATA_STAGING_API_KEY` repository secrets;
without both, that job is skipped.

Releases use [release-please](https://github.com/googleapis/release-please): commit
with [Conventional Commits](https://www.conventionalcommits.org), merge the release
PR it opens, and the release workflow publishes to PyPI through trusted publishing.

## License

MIT
