'''

Take a component_id,(parent,child) list and read the data

Rect octo for each component_id

Put it in (cid,octo_snap) form and store it

'''

class OctoSnapper:
	octo_frame = [ ] # cid , chunk
	plist = [] # a list of (cid, (plock, clock))

	def __init__(self, pipelist):
		self.plist = pipelist

	def okto(self, cid):
		'''
		find the latest octo snapshot of 'cid'
		'''
		for i in self.octo_frame :
			if i[0] == cid:
				return i[1]

	def get_snapshot(self):
		'''
		returns the whole frame
		'''
		return octo_frame

	def live_loop(self, breakflag):
		while True:
			if breakflag.value == -1:
				sleep(1)

			if breakflag.value == 0:
				return ;

			if breakflag.value == 1: # means work is being done, so snap
				for mess in self.plist:
					cid = mess[0]
					ppipe = mess[1][0]
					cpipe = mess[1][1]

					chunk = ppipe.recv()
					print "chunk recieved..."

					self.octo_frame.append((cid, chunk))
		pass
