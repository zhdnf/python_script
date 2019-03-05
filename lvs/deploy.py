import os
import sys

def install(name):
    stat = os.system("yum install %s -y > /dev/null"%name)
    if stat == 0:
        print("%s Completed"%name)
    else:
        print("%s Failed"%name)

def uninstall(name):
    stat = os.system("yum remove %s -y > /dev/null"%name)
    if stat == 0:
        print("%s Uninstall Successfully"%name)
    else:
        print("%s Failed"%name)

def execute(cmd):
    stat = os.system("%s"%cmd)
    if stat == 0:
        pass
    else:
        print("%s is failed"%cmd)

def deploy():
    path = './keepalived.conf'

    # install keepalived and ipvsadm
    install("keepalived")
    install("ipvsadm")

    # keepalived.conf
    execute("cp %s /etc/keepalived/ -f"%path)

    # restart keepalived service
    execute("service keepalived restart")

    # keepalived starting up
    execute("chkconfig keepalived on")

    # switch on ip_forward 
    # centos 6.5 
    execute("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # centos 7
    # execute("echo 'net.ipv4.ip_forward' = 1 > /usr/lib/sysctl.d/50-default.conf")

def rollback():
    # uninstall keepalived ipvsadm
    uninstall("keepalived")
    uninstall("ipvsadm")

    # switch off ip_forward
    execute("echo 0 > /proc/sys/net/ipv4/ip_forward")

if __name__  == "__main__":
    
    opt = ''

    if len(sys.argv) != 2:
        print("please input parameters: deploy or rollback")
        exit(0)

    opt = sys.argv[1]

    if opt == "deploy":
        deploy()
    elif opt == "rollback":
        rollback()
    else:
        print("please input parameters: deploy or rollback")
    
    

