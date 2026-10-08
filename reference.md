# Reference
## Web Data
<details><summary><code>client.web_data.<a href="src/floppydata/web_data/client.py">fetch_web_data</a>(...) -> FetchWebDataResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a page and returns its rendered HTML. Explicit low, medium, or high difficulty makes one attempt; auto retries low, then medium, then high only after a failed attempt. The first successful attempt consumes one Web Data request. Failed fetches return structured v2 JSON errors with message "Failed to scrape the URL" and safe metadata only. Use this for page retrieval. Do not use it for usage reporting; use getWebDataUsage or getAccountUsage instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.web_data.fetch_web_data(
    url="https://example.com",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**url:** `str` — Target page URL to fetch through Web Data.
    
</dd>
</dl>

<dl>
<dd>

**country_code:** `typing.Optional[str]` — 2-letter country code for the request exit location.
    
</dd>
</dl>

<dl>
<dd>

**city:** `typing.Optional[str]` — City for the request exit location.
    
</dd>
</dl>

<dl>
<dd>

**difficulty:** `typing.Optional[FetchWebDataRequestDifficulty]` — Access difficulty pool. low, medium, and high make one attempt. auto retries low, then medium, then high after a failed attempt. Omit this field to make one attempt at the default difficulty.
    
</dd>
</dl>

<dl>
<dd>

**render_delay_ms:** `typing.Optional[int]` — Delay before rendered HTML is returned, in milliseconds.
    
</dd>
</dl>

<dl>
<dd>

**cache_max_age_days:** `typing.Optional[int]` — Maximum age of cached content in days, from 0 to 1.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.web_data.<a href="src/floppydata/web_data/client.py">search_web_data</a>(...) -> SearchWebDataResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Searches the public web and returns lightweight organic results in ranking order. One successful search consumes one Web Data request. Use this to discover relevant pages; use fetchWebData when you already have a URL and need its HTML. AI overviews, related questions, and location controls are not included.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.web_data.search_web_data(
    query="browser automation",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**query:** `str` — Search query. Whitespace is trimmed before searching.
    
</dd>
</dl>

<dl>
<dd>

**num_results:** `typing.Optional[int]` — Maximum number of organic results to return.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.web_data.<a href="src/floppydata/web_data/client.py">get_web_data_balance</a>() -> WebDataBalance</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the authenticated account balance for Web Data requests only. Use getAccountBalances for an account-level rollup across products.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.web_data.get_web_data_balance()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.web_data.<a href="src/floppydata/web_data/client.py">get_web_data_usage</a>(...) -> GetWebDataUsageResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns Web Data API usage for the authenticated account as UTC period rollups: yesterday, last7Days, and last30Days. If from or to is supplied, the response also includes requestedRange. Use this for Web Data-only reporting.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.web_data.get_web_data_usage()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**from:** `typing.Optional[GetWebDataUsageRequestFrom]` — Start date or datetime in RFC 3339 format.
    
</dd>
</dl>

<dl>
<dd>

**to:** `typing.Optional[GetWebDataUsageRequestTo]` — End date or datetime in RFC 3339 format.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Rotating Proxy
<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">build_rotating_proxy_connection</a>(...) -> BuildRotatingProxyConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Builds one rotating proxy connection string from targeting and session options. Use connection.connectionString as the primary copy-paste value. Set subuserId to an ID from /v2/proxy/rotating/subusers, or omit it to use the first account subuser. Use locations first to choose valid country, city, and state values; state takes precedence over city.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.build_rotating_proxy_connection(
    type="residential",
    country="US",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**type:** `BuildRotatingProxyConnectionRequestType` — Proxy type
    
</dd>
</dl>

<dl>
<dd>

**country:** `str` — 2-letter country code.
    
</dd>
</dl>

<dl>
<dd>

**subuser_id:** `typing.Optional[int]` — Subuser ID from GET /v2/proxy/rotating/subusers. When omitted, the first account subuser is used.
    
</dd>
</dl>

<dl>
<dd>

**city:** `typing.Optional[str]` — City name from GET /v2/proxy/rotating/locations. Spaces are encoded as underscores. Used only when state is not supplied.
    
</dd>
</dl>

<dl>
<dd>

**state:** `typing.Optional[str]` — State or subdivision value from GET /v2/proxy/rotating/locations. When supplied, it takes precedence over city.
    
</dd>
</dl>

<dl>
<dd>

**asn:** `typing.Optional[str]` — Target ASN as digits.
    
</dd>
</dl>

<dl>
<dd>

**rotation:** `typing.Optional[float]` — Rotation value: -1 for each request, 0 for sticky, or interval minutes.
    
</dd>
</dl>

<dl>
<dd>

**session:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**protocol:** `typing.Optional[BuildRotatingProxyConnectionRequestProtocol]` 
    
</dd>
</dl>

<dl>
<dd>

**udp:** `typing.Optional[bool]` — Route UDP traffic through the proxy. Supported only for SOCKS5 residential or mobile proxies.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">list_rotating_proxy_subusers</a>() -> ListRotatingProxySubusersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns rotating proxy subusers for the authenticated account. Use a subuser username and password when building proxy usernames manually. Pass a returned id as subuserId to /v2/proxy/rotating/connections, /v2/proxy/rotating/usage, or /v2/account/usage.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.list_rotating_proxy_subusers()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">create_rotating_proxy_subuser</a>(...) -> CreateRotatingProxySubuserResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a named rotating proxy subuser for the authenticated account and returns its proxy username and password. Use this when you need separate proxy identities for workloads, teams, or environments.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.create_rotating_proxy_subuser(
    name="crawler-prod",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Human-readable label for the new proxy subuser.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">delete_rotating_proxy_subuser</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes one proxy subuser owned by the authenticated account. Proxy strings that use the deleted username stop working. The final remaining subuser cannot be deleted.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.delete_rotating_proxy_subuser(
    subuser_id=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**subuser_id:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">list_rotating_proxy_locations</a>(...) -> ListRotatingProxyLocationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns supported rotating proxy countries with static country-level cities and state/subdivision lists. Cities are not nested under states. Use the returned city or state strings directly in buildRotatingProxyConnection; state takes precedence over city when both are supplied.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.list_rotating_proxy_locations(
    type="residential",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**type:** `ListRotatingProxyLocationsRequestType` — Proxy type to list locations for.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">get_rotating_proxy_balance</a>() -> RotatingProxyBalance</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns rotating proxy traffic balance only. For account-level balances across products, use /v2/account/balances.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.get_rotating_proxy_balance()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">get_rotating_proxy_usage</a>(...) -> GetRotatingProxyUsageResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns rotating proxy traffic usage as UTC period rollups: yesterday, last7Days, and last30Days. If from or to is supplied, the response also includes requestedRange. Use subuserId from /v2/proxy/rotating/subusers to report one subuser, or omit it to include all account subusers. proxyType can be combined with subuserId. Rollups report total traffic with txBytes and rxBytes set to null.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.get_rotating_proxy_usage(
    subuser_id=123,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**from:** `typing.Optional[GetRotatingProxyUsageRequestFrom]` — Date or datetime in RFC 3339 format
    
</dd>
</dl>

<dl>
<dd>

**to:** `typing.Optional[GetRotatingProxyUsageRequestTo]` — Date or datetime in RFC 3339 format
    
</dd>
</dl>

<dl>
<dd>

**subuser_id:** `typing.Optional[int]` — Subuser ID from GET /v2/proxy/rotating/subusers. Omit to include all account subusers.
    
</dd>
</dl>

<dl>
<dd>

**proxy_type:** `typing.Optional[GetRotatingProxyUsageRequestProxyType]` — Proxy type
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.rotating_proxy.<a href="src/floppydata/rotating_proxy/client.py">list_rotating_proxy_requests</a>(...) -> ListRotatingProxyRequestsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns per-request analytics events for the authenticated account, one row per accessed host, sorted by date descending. Use subuserId from GET /v2/proxy/rotating/subusers to filter to one subuser, or omit it to include all account subusers. from and to must both be set or both omitted; the window defaults to the last 7 days when omitted. Page with limit/offset while keeping the window fixed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.rotating_proxy.list_rotating_proxy_requests(
    subuser_id=123,
    limit=100,
    offset=0,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**subuser_id:** `typing.Optional[int]` — Subuser ID from GET /v2/proxy/rotating/subusers. Omit to include requests from all account subusers.
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[ListRotatingProxyRequestsRequestFrom]` — Window start, RFC3339. from and to must both be set or both omitted. Defaults to the last 7 days when omitted.
    
</dd>
</dl>

<dl>
<dd>

**to:** `typing.Optional[ListRotatingProxyRequestsRequestTo]` — Window end, RFC3339. Must be after from.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum events to return.
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Pagination offset.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Static Proxy
<details><summary><code>client.static_proxy.<a href="src/floppydata/static_proxy/client.py">list_static_proxies</a>() -> ListStaticProxiesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns static proxy inventory for the authenticated account with a canonical connection.connectionString copy-paste URL. Static proxies are inventory-only in v2; usage reporting is not available for this product.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.static_proxy.list_static_proxies()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Proxy
<details><summary><code>client.proxy.<a href="src/floppydata/proxy/client.py">check_proxy</a>(...) -> CheckProxyResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Checks one proxy connection and returns the detected exit IP and location. Provide either connectionString or structured proxy fields.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.proxy.check_proxy(
    request={
        "connection_string": "http://user-USERNAME-type-residential-country-US-rotation-15:PASSWORD@geo.g-w.info:10080"
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `CheckProxyRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Account
<details><summary><code>client.account.<a href="src/floppydata/account/client.py">get_account_balances</a>(...) -> GetAccountBalancesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns account-level balance summaries across available products. Use product-scoped balance endpoints when a page only needs one product.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.account.get_account_balances()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**product:** `typing.Optional[GetAccountBalancesRequestProduct]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.account.<a href="src/floppydata/account/client.py">get_account_usage</a>(...) -> GetAccountUsageResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns account-level usage across products with usage reporting as UTC period rollups. If from or to is supplied, product usage also includes requestedRange. Use subuserId from /v2/proxy/rotating/subusers to narrow rotating proxy usage; it does not apply to Web Data. Rotating proxy rollups report total traffic with txBytes and rxBytes set to null. Static proxies are inventory-only and are not included in usage responses.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.account.get_account_usage(
    subuser_id=123,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**product:** `typing.Optional[GetAccountUsageRequestProduct]` 
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[GetAccountUsageRequestFrom]` — Date or datetime in RFC 3339 format
    
</dd>
</dl>

<dl>
<dd>

**to:** `typing.Optional[GetAccountUsageRequestTo]` — Date or datetime in RFC 3339 format
    
</dd>
</dl>

<dl>
<dd>

**subuser_id:** `typing.Optional[int]` — Rotating proxy subuser ID from GET /v2/proxy/rotating/subusers. Omit to include all account subusers.
    
</dd>
</dl>

<dl>
<dd>

**proxy_type:** `typing.Optional[GetAccountUsageRequestProxyType]` — Rotating proxy type. Applies to rotating proxy usage.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Cloud Browser
<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">list_browser_sessions</a>(...) -> ListBrowserSessionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists browser session history using cursor pagination.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.list_browser_sessions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**status:** `typing.Optional[ListBrowserSessionsRequestStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**cursor:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">create_browser_session</a>(...) -> BrowserSession</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates and starts a browser. The smallest request is {} and creates burner browser state that is cleaned up after the session ends. Add persist.ttlSeconds to keep settings.id reusable for a bounded retention window.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.create_browser_session()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**settings:** `typing.Optional[CreateBrowserSessionRequestSettings]` 
    
</dd>
</dl>

<dl>
<dd>

**browser:** `typing.Optional[CreateBrowserSessionRequestBrowser]` 
    
</dd>
</dl>

<dl>
<dd>

**storage:** `typing.Optional[CreateBrowserSessionRequestStorage]` 
    
</dd>
</dl>

<dl>
<dd>

**proxy:** `typing.Optional[CreateBrowserSessionRequestProxy]` 
    
</dd>
</dl>

<dl>
<dd>

**persist:** `typing.Optional[CreateBrowserSessionRequestPersist]` 
    
</dd>
</dl>

<dl>
<dd>

**runtime:** `typing.Optional[CreateBrowserSessionRequestRuntime]` 
    
</dd>
</dl>

<dl>
<dd>

**start_url:** `typing.Optional[str]` — URL the browser opens when newly created settings launch.
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">get_browser_session</a>(...) -> BrowserSession</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns current session state and a freshly signed connection URL while the session is active.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.get_browser_session(
    session_id="sessionId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**session_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">delete_browser_session</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an ended browser session from history. Persistent browser state is not deleted; burner state is cleaned up when the session ends.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.delete_browser_session(
    session_id="sessionId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**session_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">stop_browser_session</a>(...) -> BrowserSession</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Idempotently stops the browser and synchronizes its saved browser state.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.stop_browser_session(
    session_id="sessionId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**session_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">create_browser_session_live_view</a>(...) -> CreateBrowserSessionLiveViewResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a fresh live-view URL. It is rejected while a CDP relay is connected.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.create_browser_session_live_view(
    session_id="sessionId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**session_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.cloud_browser.<a href="src/floppydata/cloud_browser/client.py">delete_browser_settings</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Permanently deletes inactive saved settings and browser state. It never silently stops an active session.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from floppydata import FloppyData
from floppydata.environment import FloppyDataEnvironment

client = FloppyData(
    api_key="<value>",
    environment=FloppyDataEnvironment.PRODUCTION,
)

client.cloud_browser.delete_browser_settings(
    settings_id="settingsId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**settings_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

