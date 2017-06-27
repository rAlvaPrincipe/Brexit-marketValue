import pygtk
pygtk.require('2.0')
import gtk
# -*- coding: utf-8 -*-
from calculator import Calculator

class Interface:
    vocabulary = []
    vocabulary_request = ""

    def calcola(self, widget, data=None):
        calculator = Calculator()
        # use default sentiment_type = variation
        calculator.start(self.vocabulary_request, "variation", 0.001, 0, 0.6)

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

        # Another callback

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def callback(self, widget, data=None):
        if (widget.get_active() == True):
            self.vocabulary_request = data
        if (widget.get_active() == False):
            self.vocabulary_rdequest = ""

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        vbox = gtk.VBox(True, 2)
        self.window.add(vbox)

        button = gtk.CheckButton("afinn96")
        button.connect("toggled", self.callback, "afinn96")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("afinn111")
        button.connect("toggled", self.callback, "afinn111")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("bing")
        button.connect("toggled", self.callback, "bing")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("nrc")
        button.connect("toggled", self.callback, "nrc")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.Button("Calcola")
        button.connect("clicked", self.calcola, None)
        button.connect_object("clicked", gtk.Widget.destroy, self.window)
        vbox.pack_start(button, True, True, 2)
        button.show()

        vbox.show()
        self.window.show()

    # All PyGTK applications must have a gtk.main(). Control ends here
    # and waits for an event to occur (like a key press or mouse event).
    # If the program is run directly or passed as an argument to the python
    # interpreter then create a HelloWorld instance and show it
    def main(self):
        gtk.main()
