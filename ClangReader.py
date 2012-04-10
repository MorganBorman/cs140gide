'''Holds the functionality for ready the output of the clang static 
analyzer and returning the lines and ranges of the highlighting'''

def read(filename):
	with open(filename) as filehandle:
		for line in filehandle.readlines():
			pass
