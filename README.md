# krombox

This is an attempt to automate the installs of new software on my chromebox, via Ansible.  
I'm driving everything from my Win10 box:  
http://www.jeffgeerling.com/blog/2016/using-ansible-through-windows-10s-subsystem-linux

## Install ansible
Install (Host):
```bash
$ sudo apt-get install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible
$ sudo mv /etc/ansible/hosts /etc/ansible/hosts.orig
```
## Configure ssh
Before you start ansible, you need to configure ssh on both the Host and the Guest platforms.

On Host, generate key
```
$ ssh-keygen
```

On Guest, install ssh:
```
$ sudo apt-get install openssh-server
$ sudo /etc/init.d/ssh restart
```
From Host (Win10), export key to Guest
```
$ ssh-copy-id mattiss@192.168.86.24
```
## Deploy ansible playbook
On Host:
```
cd /mnt/c/Dev/krombox/
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
ansible-playbook -i "localhost," -c local playbook.yml --tags "docker" --extra-vars "ansible_become_pass=********"
ansible-playbook -i "mintyfresh-vm," playbook.yml --tags "test" --extra-vars "ansible_become_pass=********" 
```

## Update all packages:
```
$ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
```