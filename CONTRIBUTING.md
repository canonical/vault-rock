# Contributing

## Build and deploy

```bash
rockcraft pack -v
vault_version=$(yq '.version' rockcraft.yaml)
arch=$(dpkg --print-architecture)
sudo rockcraft.skopeo --insecure-policy copy oci-archive:vault_${vault_version}_${arch}.rock docker-daemon:vault:${vault_version}
docker run vault:${vault_version}
```
