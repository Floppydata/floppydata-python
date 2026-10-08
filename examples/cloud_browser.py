"""Cloud Browser lifecycle.

create a persistent session with a custom fingerprint, proxy and cookies
-> drive it with Playwright -> live view -> stop
-> start a second session reusing the saved state -> stop
-> page through session history -> delete history and saved settings.

    pip install playwright
    FLOPPYDATA_API_KEY=... uv run python examples/cloud_browser.py
"""

import os

from playwright.sync_api import sync_playwright

from floppydata import FloppyData

fd = FloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))
TASK_ID = "sdk-example-python"


def visit(connect_url: str, url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(connect_url)
        try:
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(url)
            return page.title()
        finally:
            # With keep_alive this only releases the relay; the session keeps running.
            browser.close()


# 1. First session: custom settings, kept for 1 hour after it ends.
first = fd.cloud_browser.create_browser_session(
    browser={
        "viewport": {"width": 1440, "height": 900},
        "fingerprint": {
            "strategy": "custom",
            "os": "windows",
            "locale": "en-US",
            "timezone": "auto",  # follows the proxy location
            "geolocation": {"mode": "auto"},
            "hardware": {"cpu_cores": 8, "memory_gb": 8},
            "masking": {"canvas": "noise", "webgl": {"mode": "auto"}, "webrtc": "proxy"},
        },
    },
    proxy={
        "type": "residential",
        "location": {"country_code": "US", "city": "New York"},
        "rotation": {"mode": "sticky"},
    },
    storage={
        "cookies": {
            "items": [
                {
                    "name": "consent",
                    "value": "yes",
                    "domain": ".example.com",
                    "path": "/",
                    "secure": True,
                }
            ]
        }
    },
    runtime={"timeout_seconds": 1800, "keep_alive": True},
    persist={"ttl_seconds": 3600},
    start_url="https://example.com",
    metadata={"taskId": TASK_ID},
)
settings_id = first.settings.id
print(f"Session {first.id} {first.status}, settings {settings_id} ({first.settings.persistence})")

try:
    # 2. Drive it with Playwright over CDP.
    if not first.connect_url:
        raise SystemExit("Session has no connect_url")
    print(f"Page title: {visit(first.connect_url, 'https://example.com')}")

    # 3. keep_alive, so we can reconnect with a freshly signed connect_url.
    current = fd.cloud_browser.get_browser_session(first.id)
    if current.connect_url:
        print(f"Reconnected, title: {visit(current.connect_url, 'https://example.org')}")

    # 4. Live view URL to watch the browser (close any CDP relay first).
    live_view = fd.cloud_browser.create_browser_session_live_view(first.id)
    print(f"Live view: {live_view.live_view_url}")
finally:
    # 5. Stop (idempotent). Saved state is kept until ended_at + ttl_seconds.
    stopped = fd.cloud_browser.stop_browser_session(first.id)
    print(f"Stopped; state kept until {stopped.settings.retention_expires_at}")

try:
    # 6. Second session reusing the saved fingerprint, proxy IP, cookies and storage.
    #    browser/proxy/persist cannot be sent together with settings.
    second = fd.cloud_browser.create_browser_session(
        settings={"id": settings_id},
        runtime={"timeout_seconds": 600, "keep_alive": False},
        metadata={"taskId": TASK_ID},
    )
    try:
        if second.connect_url:
            print(f"Title with restored state: {visit(second.connect_url, 'https://example.com')}")
    finally:
        fd.cloud_browser.stop_browser_session(second.id)

    # 7. Page through stopped sessions with the opaque cursor; delete this example's history.
    cursor: str | None = None
    while True:
        page = fd.cloud_browser.list_browser_sessions(status="stopped", limit=20, cursor=cursor)
        for session in page.items:
            if (session.metadata or {}).get("taskId") == TASK_ID:
                fd.cloud_browser.delete_browser_session(session.id)
                print(f"Deleted history for {session.id}")
        cursor = page.next_cursor
        if not cursor:
            break
finally:
    # 8. Permanently delete the saved browser state, even if a step above failed.
    fd.cloud_browser.delete_browser_settings(settings_id)
    print(f"Deleted settings {settings_id}")
