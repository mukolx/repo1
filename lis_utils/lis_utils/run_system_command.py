import subprocess

def run_sys_command(comman2run):
    system_process = subprocess.Popen(comman2run,stdout=subprocess.PIPE,\
                             stderr=subprocess.PIPE,shell=True)
    output, errors = system_process.communicate()
    if system_process.returncode != 0:
        sys.stderr.write(errors)
        sys.exit(1)
    else:
        sys.stdout.write(output)
    return output
