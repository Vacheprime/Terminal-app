import subprocess, pickle, time, socket
from _thread import *

# global variables
cmd = ""
state = ">"


def letterprint(text):
	for i in range(0, len(text)):
		if i < len(text) - 1:
			print(text[i], end="", flush= True)
			time.sleep(0.01)
		else:
			print(text[i], end="\n")
			time.sleep(0.01)


# some info
hostname = socket.gethostname()
letterprint("terminal.py v1.5.0")
letterprint("Welcome, " + str(hostname) + "!")

# gets import list for commands (Imports.txt)
try:
	import_file = open('Imports.txt', 'rb')
	imports_list = pickle.load(import_file)
	import_file.close()
	letterprint("Imports: " + str(imports_list))
except:
	letterprint("error reading imports")


# stores the imports in the imports_dict dictionnary.
imports_dict = {}
for x in imports_list:
	try:
		imports_dict[x] = __import__(x)
		letterprint("Imported: " + str(x))
	except ImportError as e:
		letterprint("error importing: " + str(x) + "\n" + str(e))


# Warning if no tool in path.
if len(imports_dict) == 0:
	letterprint("No tool in path. Only preset functions are available.")

# change path (imports_dict).
def chtool(args):
	executed = False
	# removes tool(s) and updates Imports.txt
	if args[1] == "rm":
		executed = True
		for x in args[2:]:
			imports_list.remove(x)
			letterprint("removed " + str(x) + " from tools")
		import_file = open("Imports.txt", "wb")
		pickle.dump(imports_list, import_file)
		import_file.close()

	# adds tool(s) and updates Imports.txt
	elif args[1] == "add" and not args[2] in imports_list:
		executed = True
		if len(args[2:]) > 1:
			letterprint("Can only add one tool at a time.")
		imports_list.append(args[2])
		letterprint("added " + str(args[2]) + " to tools")
		import_file = open("Imports.txt", "wb")
		pickle.dump(imports_list, import_file)
		import_file.close()

	# updates path
	if executed == True:
		imports_dict = {}
		for x in imports_list:
			try:
				imports_dict[x] = __import__(x)
				letterprint("Imported: " + str(x))
			except ImportError as e:
				letterprint("error importing: " + str(x) + "\n" + str(e))
		return imports_dict
	return imports_dict



while True:

	# testing
	lenght_dict = len(imports_dict)
	lenght_list = len(imports_list)
	if len(imports_dict) != len(imports_list):
		state = "?"
	if len(imports_dict) == 0:
		state = "!"
	if lenght_dict != 0 and lenght_dict == lenght_list:
		state = ">"

	#  input and arguments
	cmd = str(input(state + "> "))
	args = cmd.split()

	# clear command (preset)

	if cmd == "clear":
		subprocess.run("clear")

	elif cmd == "path":
		print(imports_dict)
		letterprint(str(imports_list))
	# rmtool command (preset)

	elif len(args) > 0 and args[0] == "chtool":
		try:
			imports_dict = chtool(args)
		except:
			letterprint("error executing")

	# analysing command

	elif len(args) > 0 and args[0] in imports_dict:
		try:
			imports_dict[args[0]].run(args, cmd)
		except:
			letterprint("error executing")

	# unknown command

	elif len(args) > 0 and cmd != "exit":
		letterprint("error: unknown command: " + str(cmd))

	elif len(args) > 0 and cmd == "exit":
		if len(imports_dict) > 0:
			letterprint("Goodbye, " + str(hostname) + "!")
			break
		else:
			break
