# Via helm chart :
    helm install elasticsearch elastic/elasticsearch
    helm install elasticsearch elastic/elasticsearch -f values.yaml
    helm install kibana elastic/kibana



## Link : https://medium.com/rahasak/deploy-elasticsearch-and-kibana-cluster-on-kubernetes-with-elasticsearch-operator-79f205170f40
    - Install elk crd(CustomResourceDefinition).
    - Namespace named elastic-system to hold all operator resources.
    - ServiceAccount, ClusterRole and ClusterRoleBinding to allow the operator to manage resources throughout the cluster
    - StatefulSet, ConfigMap, Secret and Service in elastic-system namespace to run the operator application.

1. Install CRD:
    - kubectl create -f https://download.elastic.co/downloads/eck/2.3.0/crds.yaml
    - kubectl get crd
2. install the operator with its RBAC rules. this will create namespace called elastic-system and install elastic operator on it
    - kubectl apply -f https://download.elastic.co/downloads/eck/2.3.0/operator.yaml
    - kubectl get all -n elastic-system

3. Deploy Elasticsearch Cluster
    - kubectl apply -f /Users/D073341/work/LaMa/gitrepo/argodep/elk/es-dploymentva.yaml
    - kubectl apply -f /Users/D073341/work/LaMa/gitrepo/argodep/elk/kibana.yaml



## HAC Filebeat setup
    - log-701  is logstash :
        OiW2001!
    - 
