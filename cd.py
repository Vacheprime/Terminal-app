from update_tools import update_tools
import pickle



def run(args, currentlocation):
	if "chatapp" in args and len(args) < 3:
		location = "chatapp"
		return location
	elif "hack" in args and len(args) < 3:
		location = "hack"
		return location
	elif "home" in args and len(args) < 3:
		location = "home"
		return location
	else:
		if len(args) == 2:
			print("error: " + args[1] + " is not a tool.")
		elif len(args) > 2:
			print("error: unexpected argument.")
		else:
			print("error: no tool specified.")
		return currentlocation

"""
l = ["cd"]

add = open("Imports.txt", "wb")
pickle.dump(l, add)
add.close()

"""
"""
add = open("Tools.txt", "rb")
cd = pickle.load(add)
add.close()
cd["cd"].cd(1, 5)
"""
"""
cd = Cd()
print(cd)
update_tools("cd", cd)
"""
"""
cd = Cd()
d = {"cd", cd}
tool = open("Tools.txt", "wb")
writy = pickle.dump(d, tool)
tool.close
"""
