"""Static proxies: list owned IPs -> health-check each one concurrently (async client).

FLOPPYDATA_API_KEY=... uv run python examples/static_proxy.py
"""

import asyncio
import os

from floppydata import AsyncFloppyData
from floppydata.core import ApiError


async def main() -> None:
    fd = AsyncFloppyData(base_url=os.environ.get("FLOPPYDATA_BASE_URL"))

    inventory = await fd.static_proxy.list_static_proxies()
    print(f"{len(inventory.items)} active static IPs, {inventory.pending_count} pending")

    results = await asyncio.gather(
        *(
            fd.proxy.check_proxy(request={"connection_string": proxy.connection.connection_string})
            for proxy in inventory.items
        ),
        return_exceptions=True,
    )

    for proxy, result in zip(inventory.items, results, strict=False):
        label = f"{proxy.ip} [{proxy.proxy_type}, {proxy.country_code}]"
        if isinstance(result, ApiError):
            print(f"FAIL {label}: HTTP {result.status_code}")
        elif isinstance(result, BaseException):
            raise result
        elif result.ip != proxy.ip:
            print(f"WARN {label}: exits via {result.ip}")
        else:
            print(f"OK   {label}: {result.location.city}")


asyncio.run(main())
