'''

Take a component_id,(parent,child) list and read the data

Rect octo for each component_id

Put it in (cid,octo_snap) form and store it

'''


LIMIT = 64

class limited_list(list):
	def append(self, item):
		list.append(self, item)
		if len(self) > LIMIT: self[:1]=[]

class OctoSnapper:
	_cid_octo_snaps = limited_list() # List of the form (cid, octo/chunk)

	def __init__(self):
		pass

	def okto(self, cid):
		for i in self._cid_octo_snaps :
			if i[0] == cid:
				return i[1]

	def live_loop(self, breakflag, cid_pipes):
		while True:
			if breakflag.value == -1:
				sleep(1)

			if breakflag.value == 0:
				return ;

			if breakflag.value == 1: # means work is being done, so snap
				for mess in cid_pipes:
					cid = mess[0]
					ppipe = mess[1][0]
					cpipe = mess[1][1]

					chunk = ppipe.recv()
					print "chunk recieved..."

					_cid_octo_snaps.append((cid, chunk))
		pass
