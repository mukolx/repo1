import subprocess
import os

def run_command(commnd):
    process = subprocess.Popen(commnd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    output, errors = process.communicate()
    #checking run status
    if process.returncode != 0:
        sys.stderr.write(errors)
        sys.exit(1)
    else:
        sys.stdout.write(output)
    ### incase the subprocess command fails use 
    ### os.system(cmmnd)
    return output