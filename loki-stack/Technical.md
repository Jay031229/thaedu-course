# Loki Deployment 
    - Follow link : https://grafana.com/docs/loki/latest/setup/install/helm/install-scalable/
    - Add Helm repository.
        helm repo add grafana https://grafana.github.io/helm-charts
        helm repo update
    - Install monilithic loki
      Create the configuration file values.yaml:
## Additional note : need to add below lines in additional in value.yaml otherwise loki-gatrway will be in creashloopback. https://github.com/grafana/loki/issues/6006
        global:
            clusterDomain: cluster.local
            dnsNamespace: kube-system
            dnsService: rke2-coredns-rke2-coredns
            deploymentMode: SingleBinary
    - Deploy the Loki cluster using one of these commands.
        helm install --values /Users/D073341/work/sre-cops/thaedu-course/loki-stack/1-loki/value.yaml loki -n loki grafana/loki
# After loki deployment : Port forward on 177 system
    kubectl port-forward --namespace loki svc/loki-gateway 3100:80 --address='0.0.0.0' &
    http://191.168.2.177:3100/loki/api/v1/push

    Loki address : http://loki-gateway.loki.svc.cluster.local/

<================================================================================>
## next deployment is promtail
    - Goal is to get kubernetes log files

    - Deployed prom in pron namespace
    - k apply -f /Users/D073341/work/sre-cops/thaedu-course/loki-stack/promtail/prom-deployment.yaml
