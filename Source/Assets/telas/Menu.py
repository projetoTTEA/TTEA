import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


builder = Gtk.Builder()
builder.add_from_file("TTEA.glade")
builder.connect_signals(Handler())

window = builder.get_object("wd_Menu")
window.show_all()

window.connect("destroy", Gtk.main_quit)
Gtk.main()