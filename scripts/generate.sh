#!/usr/bin/env bash
# Regenerate src/floppydata from openapi/v2.json with Fern.
# Needs Node.js and Docker (or Podman with its Docker socket).
set -euo pipefail
cd "$(dirname "$0")/.."

export FERN_DISABLE_TELEMETRY=true
image="fernapi/fern-python-sdk:$(sed -n 's/^ *version: *//p' fern/generators.yml | head -1)"
# Podman refuses short image names without a TTY; pulling the full name first
# lets the short name Fern uses resolve locally. Harmless with Docker.
docker pull -q "docker.io/$image" >/dev/null

rm -rf .fern-out
# Pin the SDK version (sent as User-Agent) to pyproject.toml; otherwise Fern
# guesses one from the registry and output differs between machines.
sdk_version=$(sed -n 's/^version = "\(.*\)"$/\1/p' pyproject.toml | head -1)
npx -y "fern-api@$(node -p "require('./fern/fern.config.json').version")" generate --local --version "$sdk_version"

# Keep only the package code, plus Fern's API reference (its links are
# relative to the repo root).
rm -rf src/floppydata
mkdir -p src
cp .fern-out/reference.md reference.md
# .fern/metadata.json records where generation ran (commit, CI or local), so it
# differs on every machine; it is not part of the package.
rsync -a --exclude README.md --exclude reference.md --exclude CONTRIBUTING.md \
  --exclude tests --exclude .fern .fern-out/ src/floppydata/
rm -rf .fern-out
# PEP 561 marker, so customers' type checkers use the SDK's types.
touch src/floppydata/py.typed

# Let release-please bump the User-Agent version together with pyproject.toml.
wrapper=src/floppydata/core/client_wrapper.py
if [ "$(grep -c "\"User-Agent\": \"floppydata/$sdk_version\"," "$wrapper")" != 1 ]; then
  echo "generate.sh: expected one User-Agent line for $sdk_version in $wrapper; Fern output changed" >&2
  exit 1
fi
sed -i "s|\"User-Agent\": \"floppydata/$sdk_version\",|&  # x-release-please-version|" "$wrapper"

# No retries by default (Fern defaults to 2, POSTs included). The API has no
# idempotency keys, so a retried create could duplicate a billed browser
# session or a subuser. Customers opt in with FloppyData(max_retries=N).
client=src/floppydata/client.py
expected=2
for pattern in 'max_retries if max_retries is not None else 2$' 'retries for failed requests\. Defaults to 2\.'; do
  count=$(grep -c "$pattern" "$client" || true)
  if [ "$count" != "$expected" ]; then
    echo "generate.sh: expected $expected matches of '$pattern' in $client, found $count; Fern output changed" >&2
    exit 1
  fi
done
sed -i -e 's/max_retries if max_retries is not None else 2$/max_retries if max_retries is not None else 0/' \
  -e 's/retries for failed requests\. Defaults to 2\./retries for failed requests. Defaults to 0 (no retries)./' "$client"
