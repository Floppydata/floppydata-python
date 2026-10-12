# Contributing

The package under `src/floppydata` is generated from the API's OpenAPI spec with
[Fern](https://github.com/fern-api/fern)'s open-source Python generator. Do not
edit it: change `fern/` (generator config and overrides) or the API itself.

```bash
node scripts/sync-spec.mjs   # download the production spec into openapi/v2.json
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

## Keeping up with the API

The `Sync API spec` workflow (`.github/workflows/sync-spec.yml`) regenerates the
SDK from the production spec and opens a `feat:` or `feat!:` PR on branch
`sync/api-spec` when it changed (breaking changes are detected with oasdiff). The
client-api production deploy triggers it through `repository_dispatch`
(`api-spec-updated`, with the deployed spec's SHA-256 so the workflow waits for
production to serve it); it also runs daily and can be started by hand. Merge the
PR, then merge the release PR that release-please opens.
