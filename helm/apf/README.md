# Helm Chart

This provides our NPF Helm Chart

## Deployment

Create your deployment values file overriding [base values](values.yaml):

```bash
cat values-prod.yaml

baseUrl: https://nemperfeina.cat
baseEmail: it@geekscat.org

app:
  image: geekscat/nem-per-feina
  tag: latest
  workers: 4
  threads: 2
  debug: "False"
  log_level: INFO
  secretKey: this-is-not-an-strong-password
  replicaCount: 1

postgresql:
  postgresqlPassword: this-is-not-an-strong-password

celery:
  stdouts_level: INFO
  replicaCount: 1

ingress:
  hosts:
    - host: nemperfeina.cat
      paths:
        - path: /
          servicePort: 8000

...
```

```bash
# Create namespace
kubectl create ns $SOME_NAME

# Install Chart with our custom overrides
helm -n $SOME_NAME install $SOME_NAME helm/apf -f values-prod.yaml
```

## Troubleshooting

Ingress API changed before 1.18+, so remember to define your IngressClass (and opt mark it as defautl) with something like:

```yaml
apiVersion: networking.k8s.io/v1beta1
kind: IngressClass
metadata:
  name: traefik
  annotations:
    ingressclass.kubernetes.io/is-default-class: 'true'
spec:
  controller: traefik.io/ingress-controller
```

If you don't want to define it as `default-class`, pass `ingressClassName: traefik` to your `Ingress.spec`
