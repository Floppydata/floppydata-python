"""Rotating proxy, end to end.

balance -> create a subuser -> pick a location -> build a connection
-> verify it with the proxy checker -> usage and request history
-> delete the subuser.

    FLOPPYDATA_API_KEY=... uv run python examples/rotating_proxy.py
"""

import os
import time
from collections import Counter
from datetime import datetime, timedelta, timezone

from floppydata import FloppyData

fd = FloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))

PROXY_TYPE = "residential"
COUNTRY = "US"

# 1. Traffic balance: expiring + non-expiring = total.
balance = fd.rotating_proxy.get_rotating_proxy_balance()
print(
    f"Rotating traffic: {balance.total.traffic.available_gb} GB "
    f"({balance.expiring.traffic.available_gb} GB expiring at {balance.expiring.expires_at})"
)

# 2. Existing subusers (a default one is created if the account has none).
subusers = fd.rotating_proxy.list_rotating_proxy_subusers()
print(f"Existing subusers: {', '.join(str(s.id) for s in subusers.items)}")

# 3. A dedicated subuser keeps this workload's traffic separate in usage reports.
subuser = fd.rotating_proxy.create_rotating_proxy_subuser(
    name=f"sdk-example-{int(time.time())}"
).subuser
print(f"Created subuser {subuser.id} ({subuser.username})")

try:
    # 4. Pick a location. Cities and states are country-level lists.
    locations = fd.rotating_proxy.list_rotating_proxy_locations(type=PROXY_TYPE)
    country = next((loc for loc in locations.items if loc.country_code == COUNTRY), None)
    if country is None:
        raise SystemExit(f"{COUNTRY} is not available for {PROXY_TYPE} proxies")
    city = country.cities[0]
    print(f"{country.name}: {len(country.cities)} cities; using {city}")

    # 5. Build a sticky (15 min) SOCKS5 connection for the new subuser.
    connection = fd.rotating_proxy.build_rotating_proxy_connection(
        subuser_id=subuser.id,
        type=PROXY_TYPE,
        country=COUNTRY,
        city=city,
        rotation=15,
        session="sdk_example_1",
        protocol="socks5",
    ).connection
    print(f"Connection: {connection.protocol}://{connection.host}:{connection.port}")

    # 6. Verify the exit IP. The checker takes a connection string or separate fields.
    check = fd.proxy.check_proxy(request={"connection_string": connection.connection_string})
    print(f"Exit IP {check.ip} in {check.location.city}, {check.location.country}")

    again = fd.proxy.check_proxy(
        request={
            "host": connection.host,
            "port": connection.port,
            "username": connection.username,
            "password": connection.password,
            "protocol": connection.protocol,
        }
    )
    print(f"Same sticky session, same IP: {again.ip == check.ip}")

    # 7. Usage for this subuser only.
    usage = fd.rotating_proxy.get_rotating_proxy_usage(subuser_id=subuser.id)
    print(f"Subuser traffic last 7 days: {usage.traffic.last7days.total_gb} GB")

    # 8. Per-request history for the last 24h, paginated. Keep from/to fixed across pages.
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)
    limit = 500
    bytes_by_host: Counter[str] = Counter()
    offset = 0
    while True:
        page = fd.rotating_proxy.list_rotating_proxy_requests(
            from_=start, to=end, limit=limit, offset=offset
        )
        for event in page.events:
            bytes_by_host[event.host] += event.traffic_in + event.traffic_out
        if len(page.events) < limit:
            break
        offset += limit
    print("Top hosts by traffic in the last 24h:")
    for host, total in bytes_by_host.most_common(5):
        print(f"  {host}: {total} B")
finally:
    # 9. Clean up. The last remaining subuser cannot be deleted.
    fd.rotating_proxy.delete_rotating_proxy_subuser(subuser.id)
    print(f"Deleted subuser {subuser.id}")
