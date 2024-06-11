
 
acvml2610.wdf.sap.corp             12 CPU, 128 GB RAM
acvml2611.wdf.sap.corp             8 CPU, 48 GB RAM
acvml2612.wdf.sap.corp             8 CPU, 48 GB RAM
acvml2613.wdf.sap.corp             8 CPU, 48 GB RAM
acvml2614.wdf.sap.corp             8 CPU, 48 GB RAM
acvml2615.wdf.sap.corp             12 CPU, 64GB RAM, 1 TB NFS Export (/dev/sdb1 mounted on /mnt/sdb)

Credentials:
 
root/welcome!


1. To access LAB environment.
    - Connect via VPN MAC
    - Enable ssh tunneling on linux machine -
        ssh -L 10022:10.66.170.30:22 D073341@192.168.2.100
    - From Linux machine -
        netstat -an | grep 10022
            tcp        0      0 127.0.0.1:10022         0.0.0.0:*               LISTEN
        ssh root@localhost -p 10022

2. Next task is to create a user for Lab Excercise.
    - T0011
    - T0012
    - T0013
    - T0014
    - T0015
    - T0016