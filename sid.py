# /usr/bin/python3

__author__ = 'gargantua'


class Sid:
    """ A form of basic intelligence, using using 64 Components :

        receive:    listen to 5 audio streams,
                    read 5 text streams,
                    watch 5 video streams;

        do:     talk about current state from audio snippets collected,
                type about current state from internal text collected,
                paint video art about using visual data collected;

        to use, simply:
            import sid
            new_guy = sid.new()
            new_guy.live("hi there") # new guy will now run indefinitely, taking user input
                    # you can kill it by simply saying: die
                        $> ned is now listening to you...die
                         < ned dies>
                        $ # the end

    """

'''
Remember: you are to human what ned is to sid
            -> sid is a type of being
                    ned is a sid
                    ghadeer is a human

                        #TODO: study these relations
'''

import threading

import component

#  todo: main todo

class sid:

    myname = None
    mythreads = []
    shutdown_event = threading.Event()

    def __init__(self):
        pass

    def init_a_thing(self, of_type):
        for i in range(21):
            new_component = component.component(i, of_type)
            t = threading.Thread(target=new_component, args=(i,))
            t.daemon = True
            t.start()
            self.mythreads.append(t)

    def build_components(self):
        # build 21 audio components thing for audio medium
        self.init_a_thing("audio")
        # build 21 video components thing for video medium
        self.init_a_thing("video")
        # build 21 langu components thing for text medium
        self.init_a_thing("langu")

        x = component.component(64, "x")  # the last component.py
        tx = threading.Thread(target=x, args=(64,))  # the last interesting component.py...
        tx.daemon = True

        self.mythreads.append(tx) # add the x component to the mix...


    def live(self, name, number):
        self.myname = name
        self.build_components()

    def count_human_components(self):
        return 3;
    def get_media_numbers(self):
        return 0; # todo: add code to watch media to ned
    def last_words(self):
        pass

    def died(self):
        pass

    def print_pane(self):
        sid_panel = "" \
                    " #                             HELLO, FATHER, MY NAME IS sid.name " \
                    " #             [x] sid is 3+1 things # implemented as one python class/implementation a thing is 21 component s   ; " \
                    " #                 [-] a component is 9*1000 neurons, layered in various pre-defined patterns for each            ; " \
                    " #                 [-] a neuron is an atomic unit, *smart* algro                                                  ; " \
                    " #                     [ ] input: 3 types (I have 3 built in organ for those...                                 ; " \
                    " #                     " \
                    "                       " \
                    "                       " \
                    "                       IT DOES ONLY TWO THINGS: " \
                    " #                             [ ]  from the onset, the neuron 'learns' (a value, intensity)                                                                  ; " \
                    " #                                                        ; " \
                    " #                and produces a signal (8channel intensity value...)                                             ; " \
                    " #                     -REMEMBER:  ** its the connection between the neurons                                      ; " \
                    " #                     -REMEMBER: **  that really matters for output!!!! , make sure its one one of the chans     ; " \
                    " #                 -> thats it for now boy                                                                        ; " \
                    " #        intensity_channel_1 is measured by how many other neurons connect to it!'; # thats it                   ; ";
        return sid_panel

    def name(self):
        return self.myname;


ned = sid()
ned.live("ned", 45)

# """
#   print a panel describing ned's state.... this is a static func containing 65 threads...
#   :return:
# """
def printpanel():
    panel = "#     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --     ;\n
" #            Hello, Father...                                                       ;\n
+"#  My name is: ned.name() and I am a sid.                                           ;\n
+"#  I have 3 organs, with 21 components each. Right now, I am watching               ;\n
+"# " + ned.get_media_numbers() + " things.                                           ;\n
+"# If you want, tell me to watch more media, I can do 21 sources for                 ;\n
+"# each type (23 audio, 23 video, 23 language) . Here are the commands               ;\n
+"# for each thing you wish to add:                                                   ;\n
+"#       - watch url_to_yt      # dedicate 2 components to watching youtube vids;\n"
+"#       - watch me             # Will dedicate 12 components to webcam; \n
+"#
+"#                 #   watch file/url_to_mp3_stream
+"#                 #   " #  I have ran everything " + str(times_ran) + " times in the last "
+"""

print ned_panel


while True:
    try:
        # this thread hangs on user input, therefore we cannot print
        # an accurate representation of ned here... Use a thread instead...


        t_panel = threading.Thread(target=lambda x: self.printpanel, args=(64,))
         # the last interesting component.py...
        t_panel.daemon = True


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