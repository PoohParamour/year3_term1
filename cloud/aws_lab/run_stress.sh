#!/bin/bash
scp -i labsuser.pem -o StrictHostKeyChecking=no CafeKey.pem ec2-user@100.29.185.54:/home/ec2-user/CafeKey.pem
ssh -i labsuser.pem -o StrictHostKeyChecking=no ec2-user@100.29.185.54 << 'INNER'
  chmod 400 CafeKey.pem
  ssh -i CafeKey.pem -o StrictHostKeyChecking=no ec2-user@10.0.3.51 << 'DEEP'
    sudo amazon-linux-extras install epel -y
    sudo yum install stress -y
    stress --cpu 1 --timeout 600 > /dev/null 2>&1 &
DEEP
INNER
