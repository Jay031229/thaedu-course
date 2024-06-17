1. To forward service : 
    kubectl port-forward svc/argocd-server -n argocd 8080:443 --address='0.0.0.0'

    kubectl port-forward svc/my-elasticsearch-es-http 9200:9200 --address='0.0.0.0' &
    kubectl port-forward svc/my-elasticsearch-kb-http 5601:5601 --address='0.0.0.0' &