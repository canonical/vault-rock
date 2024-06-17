# Contributing

## Build and deploy

```bash
rockcraft pack -v
vault_version=$(yq '.version' rockcraft.yaml)
sudo rockcraft.skopeo --insecure-policy copy oci-archive:vault_${vault_version}_amd64.rock docker-daemon:vault:${vault_version}
docker run vault:${vault_version}
```
