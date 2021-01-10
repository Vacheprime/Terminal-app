
class Function:
	
	@staticmethod
	def cd(args, currentlocation):
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
	
