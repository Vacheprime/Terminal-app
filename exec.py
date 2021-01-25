import subprocess
from update_tools import update_tools


def run(args, cmd):	
	subprocess.run(args[1:])
	

# update_tools("exec")
