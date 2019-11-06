from gi.repository import Gtk


class StackWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Switcher")
        self.set_border_width(10)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        # Stack - container that shows one item at a time
        main_area = Gtk.Stack()
        main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        main_area.set_transition_duration(500)

        # Check box
        euclid_label = Gtk.Label() # change to object caller function
        euclid_label.set_markup("Deskripsi Euclidean")
        main_area.add_titled(euclid_label, "euclidean", "euclidean")

        # Label
        cos_label = Gtk.Label() # change to object caller function
        cos_label.set_markup("Deskripsi Cosine")
        main_area.add_titled(cos_label, "cosine", "cosine")

        # StackSwitcher - controller for the stack (row of buttons you can click to change items)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(main_area)
        box.pack_start(stack_switcher, True, True, 0)
        box.pack_start(main_area, True, True, 0)


win = StackWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
