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


import threading

import component


class sid:
    myname = None
    mythreads = []
    shutdown_event = threading.Event()

    def __init__(self):
        pass

    def build_components(self):

        # build 21 audio components
        for i in range(21):
            new_component = component.component(i)
            t = threading.Thread(target=new_component, args=(i,))

            t.daemon = True
            t.start()
            self.mythreads.append(t)
        # build 21 video components
        for i in range(21):
            new_component = component.component(i)
            t = threading.Thread(target=new_component, args=(i,))

            t.daemon = True
            t.start()
            self.mythreads.append(t)
        # build 21 language components
            for i in range(21):
            new_component = component.component(i)
            t = threading.Thread(target=new_component, args=(i,))

            t.daemon = True
            t.start()
            self.mythreads.append(t)

        # build the x component... (TODO: interesting)

        x = component.component(64) # the last component
            t = threading.Thread(target=new_component, args=(i,))

            t.daemon = True
            t.start()
            self.mythreads.append(t)


    def live(self, name, number):
        self.myname = name
        self.build_components(number)

    def last_words(self):
        pass

    def died(self):
        pass

    def name(self):
        return self.myname;


ned = sid()
ned.live("ned", 45)

while True:
    try:
        i = raw_input("the sid (" + ned.name() + " with " + str(len(ned.mythreads)) + " is listening>")
        if i == "die":
            raise EOFError()
        else:
            # we have 9 organs
            pass
    except EOFError:
        print "bye"  # todo: last 'abstract' state message from Sid here
        break

# we've broken out of the user error, kill
# todo: kill all the processes here

ned.died()