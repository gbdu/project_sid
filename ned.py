import sid

# logging.basicConfig(filename='logs/ned',level=logging.DEBUG)

'''
    a simple implementation of sid with user input
'''

class Ned(sid.Sid):
    ''' provides visual representation of a sid
        also takes user input
    '''
    
    def get_panel(self):
        panel = "Hello, my name is " + self.getname() + "."
        # panel += "   I have %d components running concurrently" % len ( self.mythreads )
        # panel += str(threading.active_count())
        return panel

    def catch_line(self):
        i = raw_input("anything to say to ned? ")
        if i == "die": raise EOFError
        return i

    def get_components(self):
        return self.components;

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
    ned.live()


