# /usr/bin/python3

__author__ = 'gargantua'


import threading

class Ned:
    myname = None
    mythreads = []
    shutdown_event = threading.Event()

    def __init__(self):
        pass

    def live(self, name, number):
        self.myname = name
#        self.build_components()

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


ned = Ned()
ned.live("ned", 45)


while True:
    try:
        # this thread hangs on user input, therefore we cannot print
        # an accurate representation of ned here... Use a thread instead...

        t_panel = threading.Thread(target=ned.print_panel)
        # the last interesting region.py...
        t_panel.daemon = True
        t_panel.start() # start printing output
        i = raw_input("anything to say to ned? ")

        if i == "die":
            raise EOFError()
        else:
            # we have 9 organs
            pass
    except EOFError:
        print "bye"  # todo: last 'abstract' state message from Sid here
        # - last_image_dreamt
        # - last_text_said
        # - last_snippet_string_said
        break

# we've broken out of the user error, kill
# [done by python as soon as main thread exists (input from sid)] : kill all the processes here

ned.died()