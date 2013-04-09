#!/usr/bin/env python

import datetime
import glib
from time import sleep
from gi.repository import Gtk

def yieldsleep(func):
    def start(*args, **kwds):
        iterable = func(*args, **kwds)
        def step(*args, **kwds):
            try:
                time = next(iterable)
                glib.timeout_add_seconds(time, step)
            except StopIteration:
                pass
        glib.idle_add(step)
    return start

class PyPomo:
    def __init__(self):
        self.PyPomoWindow = Gtk.Window()
        self.PyPomoWindow.set_title("Timeboxing")
        self.PyPomoWindow.set_default_size(500, 200)
        self.PyPomoWindow.set_position(Gtk.WindowPosition.CENTER)
        self.PyPomoWindow.connect("destroy", self.close_window)
        self.vbox = Gtk.VBox(False, 5)
        self.title = Gtk.Label()
        self.title.set_markup('<big>00:00:00</big>')
        self.title.set_line_wrap(True)
        self.vbox.add(self.title)
        self.btn_start = Gtk.Button("Start")
        self.btn_start.connect_after("clicked", self.click_start)
        self.btn_stop = Gtk.Button("Stop")
        self.btn_stop.connect_after("clicked", self.click_stop)
        self.vbox.pack_start(self.btn_start, False, False, 0)
        self.vbox.pack_start(self.btn_stop, False, False, 0)
        self.PyPomoWindow.add(self.vbox)
        self.PyPomoWindow.show_all()

    @yieldsleep
    def click_start(self, widget):
        n_time = 0
        self.stop = False
        while n_time < 1500 and self.stop == False:
            # now = datetime.datetime.now()
            yield 1
            self.set_label(n_time)
            print "Start the Clock, Seconds: %d" % n_time
            n_time += 1

    def click_stop(self, widget):
        self.stop = True

    def set_label(self, second):
        minute = second / 60
        self.title.set_markup('<big>%d:%d</big>' % (minute, second))

    def close_window(self, widget):
        Gtk.main_quit()

    def main():
        Gtk.main()

if __name__ == '__main__':
    app = PyPomo()
    Gtk.main()