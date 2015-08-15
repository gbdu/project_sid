# /usr/bin/python3

__author__ = 'gargantua'

import threading
import component


class Sid:
	'''create 64 components, then hang and print a message every 1 sec
        as the components run
        '''

	myname = None

	mycomponents = []
	mythreads = []

	shutdown_event = threading.Event()

	def create_component(self, mid, component_hints):
		new = component.component(component_hints)
		tx = threading.Thread(target=new.run)
		new.set_thread(mid)
		tx.daemon = True
		self.mycomponents.append(new)
		self.mythreads.append(tx)
		return tx

	@property
	def get_components(self):
		return self.mycomponents

	def __init__(self):
		# create default number of 63 types of components
		for i in range(21):
			thread_id = self.create_component(i + 1, "langu")
		for i in range(21, 42):
			thread_id = self.create_component(i + 1, "audio")
		for i in range(42, 63):
			thread_id = self.create_component(i + 1, "video")

	def _run_all_components(self):

		for i in self.mycomponents:
			i.run()

	def setname(self, myn):
		myname = myn

	def live(self, g_name):
		self._run_all_components()

		while True:
			import time
			time.sleep(1)

	def count_human_components(self):
		return 3;

	def get_media_numbers(self):
		return 0;  # todo: add code to watch media to ned

	def last_words(self):
		pass

	def died(self):
		pass

	def print_panel(self):
		sid_panel = ""
		return sid_panel

	def name(self):
		return self.myname;
