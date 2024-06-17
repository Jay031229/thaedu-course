# Prerequisites:

- setup a password less ssh 

Step 1: Install Containerd on Master Node and each Worker Node.
yum install yum-utils -y
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo -y
yum install -y yum-utils containerd.io && rm -I /etc/containerd/config.toml
yum repolist

systemctl enable containerd
systemctl start containerd
systemctl status containerd


step 2 - Install and configure Kubernetes on Master Node and each Worker Node.
    - Create file 
        vi /etc/yum.repos.d/kubernetes.repo
       [kubernetes]
        name=Kubernetes
        baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
        enabled=1
        gpgcheck=1
        gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
       


    - Where:
            baseurl — URL from where the package manager pulls the Kubernetes packages.
            enabled — Indicate that repository is enabled and can be used for package installations and updates.


            gpgcheck — Indicate that the package manager will verify the GPG signatures of the packages.
            repo_gpgcheck — Ensures that the repository is trusted and gpgkey should be checked.


            gpgkey — URLs where the GPG keys are located.

            Once pasted, press Ctrl+O, then Enter to save it. Then press Ctrl+X to exit.


            After adding the Kubernetes package to the CentOs directory we can now install Kubernetes services.

            For that, we need to execute the following command.

    - yum install -y kubelet kubectl kubeadm
    

    -   sed -i '/swap/d' /etc/fstab
    -   swapoff -a
    - setenforce 0
    - sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

    - Create /etc/sysctl.d/k8s.conf
    - modprobe br_netfilter
    - sysctl --system
        echo '1' |   tee /proc/sys/net/ipv4/ip_forward
        echo 'net.ipv4.ip_forward = 1' |   tee -a /etc/sysctl.conf
        sysctl -p

          firewall-cmd --permanent --add-port=6443/tcp
          firewall-cmd --permanent --add-port=2379-2380/tcp
          firewall-cmd --permanent --add-port=10250/tcp
          firewall-cmd --permanent --add-port=10251/tcp
          firewall-cmd --permanent --add-port=10252/tcp
          firewall-cmd --permanent --add-port=10255/tcp
          firewall-cmd --reload


        On worker nodes : 
            sudo firewall-cmd --permanent --add-port=10251/tcp
            sudo firewall-cmd --permanent --add-port=10255/tcp
            sudo firewall-cmd --reload

        
Step 3: Deploy Kubernetes Cluster.

    - systemctl enable kubelet.service
    - kubeadm init --pod-network-cidr=192.168.0.0/16

    Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    Alternatively, if you are the root user, you can run:

    export KUBECONFIG=/etc/kubernetes/admin.conf



Step 4 - add networking fannel : 
    # Ensure Kubernetes is running
        kubectl get nodes

        # Download the Flannel YAML file
        curl -O https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

        # Apply the Flannel network configuration
        kubectl apply -f kube-flannel.yml

        # Verify the network deployment
        kubectl get pods -n kube-system





Step - 5 Adding worker nodes
    Then you can join any number of worker nodes by running the following on each as root:

        
        
        sudo modprobe br_netfilter
        echo 'br_netfilter' | sudo tee /etc/modules-load.d/br_netfilter.conf
    sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

        sudo sysctl --system

        lsmod | grep br_netfilter

        sysctl net.bridge.bridge-nf-call-iptables
        sysctl net.bridge.bridge-nf-call-ip6tables

        lsmod | grep br_netfilter

        







        
        
        
        Join Worker Node to the Cluster
        kubeadm token create --print-join-command
        
        kubeadm join 192.168.2.159:6443 --token 25aevw.oh3kqn7qgm478vbq \
                --discovery-token-ca-cert-hash sha256:20157fa7def4b65f61d3a69faa9d4bc44659c9516afd1886effd46b703fe753a 


