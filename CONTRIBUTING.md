# Contributing

## Build and deploy

```bash
rockcraft pack -v
sudo skopeo --insecure-policy copy oci-archive:vault_<version>_amd64.rock docker-daemon:vault:<version>
docker run vault:<version>
```
