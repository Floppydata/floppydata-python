"""Account rollups: balances and usage across products in one call each.

FLOPPYDATA_API_KEY=... uv run python examples/account.py
"""

import os
from datetime import date

from floppydata import FloppyData

fd = FloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))

# All products. A proxy product the account does not have comes back as None.
balances = fd.account.get_account_balances()
rotating = balances.proxy.rotating if balances.proxy else None
static = balances.proxy.static if balances.proxy else None
web_data_left = balances.web_data.requests.remaining if balances.web_data else 0
print("Balances:")
print(f"  Web Data:       {web_data_left} requests left")
print(f"  Rotating proxy: {f'{rotating.total.traffic.available_gb} GB' if rotating else 'none'}")
print(f"  Static proxy:   {f'{static.active_ip_count} active IPs' if static else 'none'}")

# One product only.
web_data_only = fd.account.get_account_balances(product="web-data")
print(f"Web Data only: {web_data_only.web_data}")

# Usage across Web Data and rotating proxies for a date range.
usage = fd.account.get_account_usage(from_=date(2026, 9, 1), to=date(2026, 9, 30))
print(f"Usage {usage.filters.from_}..{usage.filters.to}:")
web_range = usage.web_data.requests.requested_range if usage.web_data else None
print(f"  Web Data requests: {web_range.total if web_range else 0}")
rotating_usage = usage.proxy.rotating if usage.proxy else None
rotating_range = rotating_usage.traffic.requested_range if rotating_usage else None
print(f"  Rotating proxy:    {rotating_range.total_gb if rotating_range else 0} GB")

# Rotating proxy usage filtered by proxy type.
mobile = fd.account.get_account_usage(product="proxy-rotating", proxy_type="mobile")
mobile_rotating = mobile.proxy.rotating if mobile.proxy else None
mobile_gb = mobile_rotating.traffic.last30days.total_gb if mobile_rotating else 0
print(f"  Mobile, last 30 days: {mobile_gb} GB")
