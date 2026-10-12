# Contributing

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
