# Create secret
Log in registry and get a secret key:
```
docker login registry.gitlab.atp-fivt.org
cat ~/.docker/config.json | base64
```

Add it to secret config (`registry_secret.yaml`):
```
.dockerconfigjson: <secret>

```
Start minikube, add addons and the secret:
```
minikube start
minikube addons enable ingress
kubectl create -f registry_secret.yaml
```

# Deploy
```
kubectl apply -f kuber/all_conf.yaml
```

# Queries examples
Get ip via:
```
minikube ip
```

For instance, minikube ip is `172.17.0.2`

`GET` -- `172.17.0.2/ping/`

output:
``` json
{
  "status": "ok"
}
```

`POST` -- `172.17.0.2/add-to-favourite/`
```json
{
	"user": "Darya",
	"item": "test url"
}
```

output:
``` json
{
  "Msg": "tried to add Darya test url",
  "Success": true
}
```

`GET` -- `172.17.0.2/get-all-favourite/`
``` json
{
    "user": "Darya"	
}
```

output:
``` json
{
  "Msg": "tried to get all favourite Darya",
  "Result": [
    "test url"
  ]
}
```

`POST` -- `172.17.0.2/remove-from-favourite/`
``` json
{
	"user": "Darya",
	"item": "test url"
}
```

output:
``` json
{
  "Msg": "tried to remove test url from Darya ",
  "Success": true
}
```