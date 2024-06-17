1. Setup a paswwordless ssh
2. Install container on Masternode and each worker Node.
    yum install yum-utils -y
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo -y
    
3. Install and configure Kubernetes on Master Node and each Worker Node.
    yum install -y yum-utils containerd.io && rm -I /etc/containerd/config.toml
    yum repolist
    systemctl enable containerd
    systemctl start containerd
    systemctl status containerd
4. Create a kubernetes.repo file. and add below contain.
        [kubernetes]
        name=Kubernetes
        baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
        enabled=1
        gpgcheck=1
        gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
5. Install kubelet kubectl kubeadm via command 
    "yum install -y kubelet kubectl kubeadm"
6. Delete swap entry from fstab
    sed -i '/swap/d' /etc/fstab
    swapoff -a
    setenforce 0
    sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config


9. Create /etc/sysctl.d/k8s.conf with beow content
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
10. modprobe br_netfilter
11. Run command "echo 'br_netfilter' | sudo tee /etc/modules-load.d/br_netfilter.conf"
12. Run command "sudo tee /etc/sysctl.d/k8s.conf <<EOF
    net.bridge.bridge-nf-call-iptables = 1
    net.bridge.bridge-nf-call-ip6tables = 1
        EOF"

11. sysctl --system
12. Open firewall ports
          firewall-cmd --permanent --add-port=6443/tcp
          firewall-cmd --permanent --add-port=2379-2380/tcp
          firewall-cmd --permanent --add-port=10250/tcp
          firewall-cmd --permanent --add-port=10251/tcp
          firewall-cmd --permanent --add-port=10252/tcp
          firewall-cmd --permanent --add-port=10255/tcp
          firewall-cmd --reload
          firewall-cmd --permanent --add-port=10251/tcp
          firewall-cmd --permanent --add-port=10255/tcp
          firewall-cmd --reload
13. Deploy Kubernetes Cluster
14. run command "systemctl enable kubelet.service"
15. run command "kubeadm init --pod-network-cidr=192.168.0.0/16"
16. Once kubernetes is running. add networking fannel
    curl -O https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
    kubectl apply -f kube-flannel.yml
    kubectl get pods -n kube-system