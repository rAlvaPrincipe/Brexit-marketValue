import transEmissCalc as matrix
import sentiment_list_by_day as sm
import pygtk
pygtk.require('2.0')
import gtk

class Interface:
    vocabulary=[]
    def calcola(self, widget, data=None):


        days = ['2016/12/05', '2016/12/06', '2016/12/07', '2016/12/08', '2016/12/09',
                '2016/12/12', '2016/12/13', '2016/12/14', '2016/12/15', '2016/12/16',
                '2016/12/19', '2016/12/20', '2016/12/21', '2016/12/22', '2016/12/23',
                '2016/12/27', '2016/12/28', '2016/12/29', '2016/12/30']

        d = sm.retrieveVocabulary(self.vocabulary)

        days_sentiment = {}
        out_file = open("Sentiment.txt", "w")
        for i in range(0, days.__len__() - 1):
            days_sentiment[i] = sm.day_sentiment(days[i], d)
            out_file.write(days[i] + "   " + str(days_sentiment[i]) + "\n")
            print(days_sentiment[i])
        out_file.close()

        tollerance = 0.001
        source = "D:\Dropbox\Universita\Modelli probabilistici per le decisioni\Progetto\Dataset\Market_values.txt"
        source_ext = "D:\Dropbox\Universita\Modelli probabilistici per le decisioni\Progetto\Dataset\Market_values_ext.txt"
        source_emission = "Sentiment.txt"
        print("INPUT DATASET:")
        # printer(extract(source))

        # print("\nDELTA  delta(day_t) = day_t - day_t-1")
        # printer(delta(extract(source_ext)))

        matrix.build_transition_m(matrix.extract(source_ext), tollerance)

        # printer(delta_emission(extract(source_emission)))

        matrix.build_emission_m(matrix.delta(matrix.extract(source), tollerance),
                                matrix.delta_emission(matrix.extract(source_emission)))

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
        if (widget.get_active()  == True):
            self.vocabulary.append(data)
        if (widget.get_active()  == False):
            self.vocabulary.remove(data)


    def __init__(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        vbox = gtk.VBox(True, 2)
        self.window.add(vbox)


        button = gtk.CheckButton("affin")
        button.connect("toggled", self.callback, "affin")
        vbox.pack_start(button, True, True, 2)
        button.show()

        button = gtk.CheckButton("bing")
        button.connect("toggled", self.callback, "bing")
        vbox.pack_start(button, True, True, 2)
        button.show()



        button = gtk.Button("Calcola")

        button.connect("clicked", self.calcola, None)
        button.connect_object("clicked", gtk.Widget.destroy, self.window)
        vbox.pack_start(button, True, True, 2)
        button.show()

        vbox.show()

        self.window.show()


    def main(self):
    # All PyGTK applications must have a gtk.main(). Control ends here

    # and waits for an event to occur (like a key press or mouse event).

        gtk.main()
    # If the program is run directly or passed as an argument to the python
    # interpreter then create a HelloWorld instance and show it

if __name__ == "__main__":
    interface = Interface()
    interface.main()
