import sys

if len(sys.argv) == 1:
	print "Usage: stackmachine.py programfile"
	sys.exit(0)

class Machine():
	stack = []
	instructions = []
	data = []
	addresses = {}
	pc = 0
	maxpc = 0
	def __init__(self,filename):
		programfile = open(filename,'r')
		lines = programfile.readlines()
		for line in lines: self.instructions.append(line[:-1]) 	# otherwise these come with a newline at the end
		self.maxpc = len(self.instructions)
		programfile.close()
	def pop(self):
		a = self.stack[0]
		self.stack = self.stack[1:]
		return a
	def push(self,value):
		self.stack = [int(value)] + self.stack
	def copy(self):
		self.stack = self.stack[0] + self.stack
	def rvalue(self,var):
		self.push(self.data[self.addresses[var]])
	def lvalue(self,var):
		if var not in self.addresses:
			self.addresses[var] = len(self.data)
			self.data.append(0)
		self.push(self.addresses[var])
	def assign(self):
		R,L = self.pop(), self.pop()
		self.data[L] = R
	def goto(self,lbl):
		self.pc = self.instructions.index("label " + lbl)
	def gofalse(self,lbl):
		if self.pop() == 0: self.goto(lbl)
	def gotrue(self,lbl):
		if self.pop() != 0: self.goto(lbl)
	def add(self):
		a,b = self.pop(),self.pop()
		self.push(a+b)
	def mul(self):
		a,b = self.pop(),self.pop()
		self.push(a*b)
	def div(self):
		a,b = self.pop(),self.pop()
		self.push(a/b)
	def mod(self):
		a,b = self.pop(),self.pop()
		self.push(a%b)
	def sub(self):
		a,b = self.pop(),self.pop()
		self.push(a-b)
	func0 = {
		"copy":copy,
		"pop":pop,
		"assign":assign,
		"+":add,
		"-":sub,
		"*":mul,
		"/":div,
		"%":mod
		}
	func1 = {
		"push":push,
		"rvalue":rvalue,
		"lvalue":lvalue,
		"goto":goto,
		"gofalse":gofalse,
		"gotrue":gotrue
		}
	def run(self,debug=False):
		while self.pc < self.maxpc:
			if debug: print self.stack
			inst = self.instructions[self.pc].split()
			if inst[0] in self.func0:
				self.func0[inst[0]](self)
			elif inst[0] in self.func1:
				self.func1[inst[0]](self,inst[1])
			self.pc += 1
		print self.stack

M = Machine(sys.argv[1])
if len(sys.argv)>2:
	M.run(debug=True)
else:
	M.run(debug=False)
