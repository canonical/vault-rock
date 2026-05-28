# Vault rock

A distroless rock image for Vault.

## Architecture support

amd64, arm64, and s390x architectures are supported.

The s390x image is built without the embedded web UI because NodeSource does not
provide Node.js 20 packages for s390x, which is required to compile the UI
assets.

## Usage

```console
docker pull ghcr.io/canonical/vault:latest
docker run -it ghcr.io/canonical/vault:latest
```
