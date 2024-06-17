sudo virt-install \
--name ubuntu \
--memory 2048 \
--vcpus 2 \
--disk path=/home/admin/qcow2_img/bionic-server-cloudimg-amd64.img,format=qcow2 \
--os-type linux \
--os-variant generic \
--network bridge=br0 \
--graphics vnc \
--import
