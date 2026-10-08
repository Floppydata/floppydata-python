"""Behaviour of the generated client that this repo relies on or configures."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable

import httpx
import pytest

from floppydata import AsyncFloppyData, BadGatewayError, FloppyData, PaymentRequiredError
from floppydata.core import ApiError

Handler = Callable[[httpx.Request], httpx.Response]

API_ERROR = {
    "error": {
        "code": "insufficient_balance",
        "message": "Insufficient Web Data balance.",
        "details": {"requestId": "abc-CDG"},
    }
}


def make_client(handler: Handler, requests: list[httpx.Request], **kwargs: object) -> FloppyData:
    def record(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return handler(request)

    client = httpx.Client(transport=httpx.MockTransport(record))
    return FloppyData(httpx_client=client, **kwargs)  # type: ignore[arg-type]


def test_reads_api_key_from_env_and_targets_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FLOPPYDATA_API_KEY", "env-key")
    requests: list[httpx.Request] = []
    fd = make_client(
        lambda _: httpx.Response(200, json={"requests": {"total": 10, "used": 1, "remaining": 9}}),
        requests,
    )

    balance = fd.web_data.get_web_data_balance()

    assert balance.requests.remaining == 9
    assert str(requests[0].url) == "https://api.floppydata.net/v2/web-data/balance"
    assert requests[0].headers["X-Api-Key"] == "env-key"


def test_refuses_to_start_without_an_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FLOPPYDATA_API_KEY", raising=False)
    with pytest.raises(ApiError, match="FLOPPYDATA_API_KEY"):
        FloppyData()


def test_sends_snake_case_kwargs_and_dicts_as_camel_case_json() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        if request.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(
            200,
            json={
                "html": "<html></html>",
                "sourceUrl": "https://example.com",
                "fetchedAt": "2026-10-08T00:00:00Z",
            },
        )

    requests: list[httpx.Request] = []
    fd = make_client(respond, requests, api_key="k", base_url="https://api.example.test")

    fd.web_data.fetch_web_data(url="https://example.com", country_code="US", difficulty="auto")
    fd.rotating_proxy.delete_rotating_proxy_subuser(7)

    assert json.loads(requests[0].content) == {
        "url": "https://example.com",
        "countryCode": "US",
        "difficulty": "auto",
    }
    assert requests[1].method == "DELETE"
    assert str(requests[1].url) == "https://api.example.test/v2/proxy/rotating/subusers/7"


BROWSER_SESSION = {
    "id": "58e531ee-16ca-49d0-8722-b425d154cc10",
    "status": "running",
    "connectUrl": "wss://api.example.test/connect",
    "settings": {
        "id": "f742823c-7ba6-4488-a72d-6e9c5447eacb",
        "persistence": "persistent",
        "ttlSeconds": 600,
        "retentionExpiresAt": None,
    },
    "runtime": {"timeoutSeconds": 120, "keepAlive": True},
    "createdAt": "2026-10-08T12:00:00Z",
    "startedAt": "2026-10-08T12:00:01Z",
    "expiresAt": "2026-10-08T12:02:00Z",
    "endedAt": None,
}


def test_nested_dict_arguments_are_converted_too() -> None:
    requests: list[httpx.Request] = []
    fd = make_client(lambda _: httpx.Response(201, json=BROWSER_SESSION), requests, api_key="k")

    session = fd.cloud_browser.create_browser_session(
        proxy={"type": "static", "ip": "203.0.113.7"},
        persist={"ttl_seconds": 600},
        runtime={"timeout_seconds": 120, "keep_alive": True},
    )

    assert session.settings.ttl_seconds == 600
    assert session.runtime.keep_alive is True
    assert json.loads(requests[0].content) == {
        "proxy": {"type": "static", "ip": "203.0.113.7"},
        "persist": {"ttlSeconds": 600},
        "runtime": {"timeoutSeconds": 120, "keepAlive": True},
    }


def test_raises_typed_errors_with_the_parsed_body() -> None:
    fd = make_client(lambda _: httpx.Response(402, json=API_ERROR), [], api_key="k")

    with pytest.raises(PaymentRequiredError) as raised:
        fd.web_data.fetch_web_data(url="https://example.com")

    assert raised.value.status_code == 402
    assert raised.value.body.error.code == "insufficient_balance"
    assert raised.value.body.error.details.request_id == "abc-CDG"
    assert isinstance(raised.value, ApiError)


def test_does_not_retry_by_default() -> None:
    """generate.sh sets max_retries to 0: retried creates could duplicate billed resources."""
    error = {
        "error": {
            "code": "service_error",
            "message": "Browser could not be started.",
            "details": {},
        }
    }
    requests: list[httpx.Request] = []
    fd = make_client(lambda _: httpx.Response(502, json=error), requests, api_key="k")

    with pytest.raises(BadGatewayError) as raised:
        fd.cloud_browser.create_browser_session()

    assert raised.value.body.error.code == "service_error"
    assert len(requests) == 1


def test_non_json_errors_raise_the_base_api_error_with_text() -> None:
    fd = make_client(
        lambda _: httpx.Response(502, text="<html>Bad gateway</html>"), [], api_key="k"
    )

    with pytest.raises(ApiError) as raised:
        fd.account.get_account_balances()

    assert raised.value.status_code == 502
    assert raised.value.body == "<html>Bad gateway</html>"


def test_retries_when_opted_in() -> None:
    requests: list[httpx.Request] = []
    responses = iter(
        [httpx.Response(502), httpx.Response(200, json={"items": [], "pendingCount": 0})]
    )
    fd = make_client(lambda _: next(responses), requests, api_key="k", max_retries=1)

    result = fd.static_proxy.list_static_proxies()

    assert result.items == []
    assert len(requests) == 2


def test_async_client() -> None:
    requests: list[httpx.Request] = []

    def record(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"items": [], "pendingCount": 0})

    async def run() -> None:
        async with httpx.AsyncClient(transport=httpx.MockTransport(record)) as http:
            fd = AsyncFloppyData(api_key="k", httpx_client=http)
            result = await fd.static_proxy.list_static_proxies()
            assert result.pending_count == 0

    asyncio.run(run())
    assert requests[0].headers["X-Api-Key"] == "k"
