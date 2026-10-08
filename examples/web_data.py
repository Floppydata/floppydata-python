"""Web Data: check balance -> search -> fetch the top results -> report usage.

FLOPPYDATA_API_KEY=... uv run python examples/web_data.py
"""

import os
import re
from datetime import date

from floppydata import FloppyData
from floppydata.core import ApiError

fd = FloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))

QUERY = "browser automation frameworks"
PAGES_TO_FETCH = 3

# 1. Make sure we can afford one search plus N page fetches.
balance = fd.web_data.get_web_data_balance()
print(f"Web Data requests remaining: {balance.requests.remaining}")
if balance.requests.remaining < 1 + PAGES_TO_FETCH:
    raise SystemExit("Not enough Web Data requests left")

# 2. Search the web (consumes 1 request).
search = fd.web_data.search_web_data(query=QUERY, num_results=10)
print(f"Search {search.request_id}: {len(search.results)} results")
for result in search.results:
    print(f"  - {result.title} ({result.url})")

# 3. Fetch rendered HTML for the top results (1 request each).
#    One failed page should not stop the others.
for result in search.results[:PAGES_TO_FETCH]:
    try:
        page = fd.web_data.fetch_web_data(
            url=result.url,
            country_code="US",
            difficulty="auto",  # retries low -> medium -> high after a failed attempt
            render_delay_ms=2000,
            cache_max_age_days=1,  # accept a cached copy up to 1 day old
        )
    except ApiError as error:
        print(f"Fetch {result.url} failed: HTTP {error.status_code}")
        continue
    match = re.search(r"<title>(.*?)</title>", page.html, re.I | re.S)
    title = match.group(1).strip() if match else None
    print(f"Fetched {page.source_url}: {len(page.html)} bytes, title {title!r}")

# 4. Usage rollups, plus an explicit date range.
usage = fd.web_data.get_web_data_usage(from_=date(2026, 9, 1), to=date(2026, 9, 30))
requests = usage.requests
print("Web Data usage (total / successful / failed):")
day, week, month = requests.yesterday, requests.last7days, requests.last30days
print(f"  yesterday:    {day.total} / {day.successful} / {day.failed}")
print(f"  last 7 days:  {week.total} / {week.successful} / {week.failed}")
print(f"  last 30 days: {month.total} / {month.successful} / {month.failed}")
if requests.requested_range:
    print(f"  {usage.filters.from_}..{usage.filters.to}: {requests.requested_range.total}")
