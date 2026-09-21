import pexpect
import sys

child = pexpect.spawn('aws ssm start-session --target i-0239174242be6308c')
child.expect(r'sh-.*\$', timeout=30)
print("Connected!")
child.sendline('sudo su -')
child.expect(r'root@.*#', timeout=10)
child.sendline('amazon-linux-extras install epel -y')
child.expect(r'root@.*#', timeout=60)
child.sendline('yum install stress -y')
child.expect(r'root@.*#', timeout=60)
child.sendline('stress --cpu 1 --timeout 600 &')
child.expect(r'root@.*#', timeout=10)
child.sendline('exit')
print("Stress test started!")
