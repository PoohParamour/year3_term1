import pty
import os
import sys
import subprocess
import time

def run_stress(instance_id):
    pid, fd = pty.fork()
    if pid == 0:
        # Child process
        os.execvp("aws", ["aws", "ssm", "start-session", "--target", instance_id, "--document-name", "AWS-StartInteractiveCommand", "--parameters", 'command="sudo amazon-linux-extras install epel -y && sudo yum install stress -y && stress --cpu 1 --timeout 300"'])
    else:
        # Parent process
        time.sleep(310)
        try:
            os.kill(pid, 9)
        except:
            pass

run_stress("i-0239174242be6308c")
run_stress("i-09460c382632d8f3b")
