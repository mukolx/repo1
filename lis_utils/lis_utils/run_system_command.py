import subprocess
import os

def run_sys_command(comman2run):
    procs = subprocess.Popen(comman2run,stdout=subprocess.PIPE,\
                             stderr=subprocess.PIPE,shell=True)
    output, errors = procs.communicate()
    if procs.returncode != 0:
        sys.stderr.write(errors)
        sys.exit(1)
    else:
        sys.stdout.write(output)
    return output
