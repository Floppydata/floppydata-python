"""Error handling: typed errors per HTTP status, the error body, and recovery
from settings_in_use.

    FLOPPYDATA_API_KEY=... uv run python examples/error_handling.py [settings_id]
"""

import os
import sys

from floppydata import (
    BadGatewayError,
    BadRequestError,
    BrowserSession,
    ConflictError,
    FloppyData,
    PaymentRequiredError,
)
from floppydata.core import ApiError

fd = FloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))


# Each documented status raises its own ApiError subclass with the parsed body.
def fetch_html(url: str) -> str | None:
    try:
        return fd.web_data.fetch_web_data(url=url, difficulty="auto").html
    except PaymentRequiredError:
        print("Out of Web Data requests; top up and retry.")
    except BadRequestError as error:
        # details.target points at the offending field.
        print(f"Invalid {error.body.error.details.target}: {error.body.error.message}")
    except BadGatewayError as error:
        # service_error: a service behind the API failed; safe to retry.
        details = error.body.error.details
        print(f"Service HTTP {details.service_status}, request {details.request_id}")
    except ApiError as error:
        # Any other status, or a non-JSON body (then `body` is the text).
        print(f"HTTP {error.status_code}: {error.body}")
    return None


# settings_in_use names the session holding the settings, so stop it and retry.
def start_with_settings(settings_id: str) -> BrowserSession:
    try:
        return fd.cloud_browser.create_browser_session(settings={"id": settings_id})
    except ConflictError as error:
        active = error.body.error.details.active_session_id
        if error.body.error.code != "settings_in_use" or not active:
            raise
        print(f"Settings busy in {active}; stopping it and retrying")
        fd.cloud_browser.stop_browser_session(active)
        return fd.cloud_browser.create_browser_session(settings={"id": settings_id})


html = fetch_html("https://example.com")
print(f"Fetched {len(html)} bytes" if html else "Fetch failed")

if len(sys.argv) > 1:
    session = start_with_settings(sys.argv[1])
    print(f"Started {session.id}")
    fd.cloud_browser.stop_browser_session(session.id)
