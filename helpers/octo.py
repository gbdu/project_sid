'''An object to represent messages passed between components'''

import pickle
import copy
class Octo:
	type_hints = None
	color = None
	source = None
	myid = None
	friends = None
	layers = None
	neurons_per_layer = None
	x = None
	
	def __init__(self, d=None):
		'''d is the octo dict to init from'''
		if d is not None:
			self.myid= d['myid']
			self.source= d['source']
			self.type_hints = d['type_hints']
			self.color= d['color']
			self.friends= d['friends']
			self.layers= d['layers']
			self.neurons_per_layer= d['neurons_per_layer']
			self.x = d['x']
		else:
			#print e
			self.myid = "-1"
			self.source= "default"
			self.type_hints = "default"
			self.color=(20,20,90)
			self.friends= "default"
			self.layers="default"
			self.neurons_per_layer="default"
			self.x = "default"

	def get_pickled(self):
		'''returns a pickled dump of the object'''
		return str(pickle.dumps(self))

	def get_a_copy(self):
		c = copy.copy(self)

		return c

	@staticmethod
	def fill_from_pickled(p):
		return pickle.loads(p)
		