# Contributing

## Build and deploy

```bash
rockcraft pack -v
sudo skopeo --insecure-policy copy oci-archive:vault_1.14.3_amd64.rock docker-daemon:vault:1.14.3
docker run vault:1.14.3
```
