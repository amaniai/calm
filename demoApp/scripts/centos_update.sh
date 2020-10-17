#!/bin/bash

sudo yum update -y
## Disable SELinux
sudo setenforce 0
sudo sed -i 's/permissive/disabled/' /etc/sysconfig/selinux
