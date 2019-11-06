from gi.repository import Gtk


class UserInput(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Top Match")
        self.set_border_width(10)
        self.set_size_request(10, 10)

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Max Number
        # Careful to string input (?)
        self.top_match = Gtk.Entry()
        self.top_match.set_text("Maximum Number of Match ")
        vbox.pack_start(self.top_match, True, True, 0)
    
        def sign_in(self, widget):
            print(self.top_match.get_text())

window = UserInput()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
