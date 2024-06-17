https://ranchergovernment.com/blog/article-simple-rke2-longhorn-and-rancher-install


 # Rocky instructions
 # stop the software firewall
 systemctl stop firewalld
 systemctl disable firewalld

 # get updates, install nfs, and apply
 yum install -y nfs-utils cryptsetup iscsi-initiator-utils

 # enable iscsi for Longhorn
 systemctl start iscsid.service
 systemctl enable iscsid.service

 # update all the things
 yum update -y

 # clean up
 yum clean all



# RKE2 Server Install
     
 curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=server sh -
 OR file path : /Users/D073341/work/sre-cops/thaedu-course/k8/rke-io.sh

 # start and enable for restarts -
 systemctl enable rke2-server.service
 systemctl start rke2-server.service
 
 # simlink all the things - kubectl
 ln -s $(find /var/lib/rancher/rke2/data/ -name kubectl) /usr/local/bin/kubectl
 
 # add kubectl conf
 export KUBECONFIG=/etc/rancher/rke2/rke2.yaml

 # check node status
 kubectl  get node


<-------------------------------------------------------------------------------------->
# RKE2 Agent Install
 
 # we add INSTALL_RKE2_TYPE=agent
 curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=agent sh -

 # create config file
 mkdir -p /etc/rancher/rke2/

 # change the ip to reflect your rancher1 ip
 echo "server: https://$RANCHER1_IP:9345" > /etc/rancher/rke2/config.yaml

 # change the Token to the one from rancher1 /var/lib/rancher/rke2/server/node-token
 echo "token: $TOKEN" >> /etc/rancher/rke2/config.yaml

 # enable and start
 systemctl enable rke2-agent.service
 systemctl start rke2-agent.service

<=============================================================>
 # Rancher Installation
 # add helm
 curl -#L https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

 # add needed helm charts
 helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
 helm repo add jetstack https://charts.jetstack.io


 # still on  rancher1
 # add the cert-manager CRD
 kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.6.1/cert-manager.crds.yaml

 # helm install jetstack
 helm upgrade -i cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace

 # helm install rancher
 helm upgrade -i rancher rancher-latest/rancher --create-namespace --namespace cattle-system --set hostname=rancher.dockr.life --set bootstrapPassword=bootStrapAllTheThings --set replicas=1


 # Longhorn
 # get charts
 helm repo add longhorn https://charts.longhorn.io

 # update
 helm repo update

 # install
 helm upgrade -i longhorn longhorn/longhorn --namespace longhorn-system --create-namespace




