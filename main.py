from tkinter import *
import functools
import db_manager
import components
import constants
import boundingbox
import input


class ButtonWrapper(Button):

    def __init__(self, name, func, height, parent_container, func_param=None):
        Button.__init__(self)
        self.container = Frame(parent_container, padx=5, pady=5,
                               width=constants.BUTTON_PANEL_WIDTH)
        self.button_object = Button(self.container, text=name, height=height)
        self.button_object.configure(command=lambda: func(func_param))
        self.button_object.pack(fill=X, expand=YES)
        self.container.pack(side=TOP, fill=X)


class ButtonsPanel:

    def __init__(self):
        self.main_frame = Frame(bd=3, relief=GROOVE)
        right_margin = Frame(width=5)
        right_margin.pack(side=RIGHT)
        width_controller = Frame(self.main_frame, width=constants.BUTTON_PANEL_WIDTH)
        width_controller.pack()
        self.main_frame.pack(side=LEFT, fill=Y)

    def get_frame(self):
        return self.main_frame


class MessageBox(Label):
    def __init__(self):
        Label.__init__(self)


class DynamicCanvas(Canvas):

    def canvas_manager(self):
        self.canvas_frame.bind("<Configure>", self.on_resize)
        self.canvas.pack(fill=BOTH, expand=YES)

    def on_resize(self, event):
        parent_width = self.parent.root.winfo_width()
        self.canvas_frame.config(width=parent_width-constants.BUTTON_PANEL_WIDTH)
        self.redraw()

    def redraw(self, *args):
        components.draw_isoplane(self.canvas)
        boundingbox.draw_boundingbox(self.canvas, self.canvas.winfo_width(),
                                     self.canvas.winfo_height())
        # also redraw all components using the draw_controller

    def __init__(self, parent=None):
        Canvas.__init__(self)
        self.parent = parent
        self.canvas_frame = Frame()
        self.canvas = Canvas(self.canvas_frame, background='black')
        self.canvas_manager()


class CommandStatus(Label):
    def __init__(self):
        Label.__init__(self)
        self.label_container = Frame()
        self.separator = Frame(self.label_container, height=10)
        self.separator.pack()
        self.label = Label(self.label_container, font='System, 11',
                           bg=constants.CMD_STATUS_COLOR,
                           anchor="w")
        self.label.pack(fill=BOTH, expand=YES)
        self.label_container.pack(side=BOTTOM, fill=X)


class CommandInput(Entry):
    def __init__(self, canvas):
        Entry.__init__(self)
        self.parent = None
        self.canvas = canvas
        self.entry_container = Frame()
        self.separator = Frame(self.entry_container, height=4)
        self.separator.pack()
        self.entry = Entry(self.entry_container, font='System, 11', bg='silver')
        self.entry.pack(fill=BOTH, expand=YES)
        self.entry.focus()
        self.entry_container.pack(side=BOTTOM, fill=X)
        self.event_binder()

    def set_parent(self, parent):
        self.parent = parent
        self.event_binder()

    def event_binder(self):
        self.entry.bind("<Return>", functools.partial(input.input_manager,
                                                      args=[self.entry,
                                                            self.parent,
                                                            self.canvas]))
        self.entry.bind("<KP_Enter>", functools.partial(input.input_manager,
                                                        args=[self.entry,
                                                              self.parent,
                                                              self.canvas]))


class MainWindow:

    def core_margins(self):
        top_margin = Frame(height=self.margin_size)
        top_margin.pack(side=TOP)
        bottom_margin = Frame(height=self.margin_size)
        bottom_margin.pack(side=BOTTOM)
        right_margin = Frame(width=self.margin_size)
        right_margin.pack(side=RIGHT)
        left_margin = Frame(width=self.margin_size)
        left_margin.pack(side=LEFT)

    def __init__(self):
        self.margin_size = 10
        self.root = Tk()
        self.root.geometry(str(constants.DEFAULT_SCREEN_WIDTH) + "x"
                           + str(constants.DEFAULT_SCREEN_HEIGHT))
        # self.root.resizable(0, 0)
        self.root.title("Piping Isometrics Generator (alpha)")
        self.core_margins()
        self.canvas = DynamicCanvas(self)
        self.entry = CommandInput(self.canvas)
        self.label = CommandStatus()
        self.canvas.canvas_frame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.entry.set_parent(self)
        components.initialize_isoplane(self.canvas.canvas)
        boundingbox.initialize_boundingbox(self.canvas.canvas)
        self.panel = ButtonsPanel()
        self.test_button1 = ButtonWrapper("Redraw",
                                          self.canvas.redraw, 1,
                                          self.panel.get_frame())
        self.test_button1 = ButtonWrapper("Toggle Isoplane",
                                          components.toggle_plane, 1,
                                          self.panel.get_frame(),
                                          self.canvas.canvas)
        self.test_button1 = ButtonWrapper("Toggle Bounding Box",
                                          boundingbox.toggle_boundingbox, 1,
                                          self.panel.get_frame(),
                                          self.canvas.canvas)


def main():
    db_manager.initialize_db()
    app = MainWindow()
    app.root.mainloop()


if __name__ == '__main__':
    main()

