from threading import Thread
from time import sleep


class Foo:
	mystuff = None

	def __init__(self, stuff):
		self.mystuff = stuff

	def show(self):
		print self.mystuff


l = [] 
f = Foo(l)

def tit(l):
	while True:
		l.append(1)
		sleep(2)




tito = Thread(target = tit, args = (l,))

tito.start()


sleep(2)

f.show()