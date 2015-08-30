

class Octo:
	type_hints = None
	color = None
	source = None
	myid = None
	friends = None
	layers = None
	neurons_per_layer = None
	x = None

	def __init__(d):
		'''d is the octo dict to init from'''
		
		self.type_hints = d['type_hints']
        self.color= d['color']
        self.source= d['source']
        self.myid= d['myid']
        self.friends= d['friends']
        self.layers= d['layers']
        self.neurons_per_layer= d['neurons_per_layer']
        self.x = d['x']

		pass
