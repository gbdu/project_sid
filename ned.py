import sid
import threading

'''
    a simple implementation of sid with user input

'''

class Ned(sid.Sid):
    ''' provides visual representation of a sid
        also takes user input
    '''

    def get_panel(self):
        panel = "Name   : %s, I have %d organs and %d components, each with %d neuron (total %d neurons)\n" \
                "I am watching %d different data streams. Tell me to watch more stuff by saying:\n" \
                "   - watch_video url_to_yt # for a youtube video\n" \
                "   - watch_me " \
                "# to watch webcam\n";
        print panel

    def catch_line(self):
        i = raw_input("anything to say to ned? ")
        if i == "die": raise EOFError
        return i

    def get_components(self):
	    return self.mycomponents;

    def catch_input(self):
        while True:
            try:
                self.catch_line()

            except EOFError:
                print "bye"  # todo: last 'abstract' state message from Sid here
                # - last_image_dreamt
                # - last_text_said
                # - last_snippet_string_said
                break


if __name__ == "__main__":
    ned = Ned()  # create a new instance of our AI
    ned.setname("ned")
    ned.live(45)


