#!/usr/bin/env python

import os
import datetime
import sys
from gi.repository import Gtk, GObject

class PyPomo:
    def __init__(self):
        self.build_gui()

    def build_gui(self):
        self.seconds_total = 0
        self.seconds = 0
        self.PyPomoWindow = Gtk.Window()
        self.PyPomoWindow.set_title("PyPomo")
        self.PyPomoWindow.set_default_size(600, 600)
        self.PyPomoWindow.set_position(Gtk.WindowPosition.CENTER)
        self.PyPomoWindow.set_icon_from_file(self.get_resource_path('../data/image/alarm.ico'))
        
        mb = Gtk.MenuBar()
        filemenu = Gtk.Menu()
        filem = Gtk.MenuItem("File")
        filem.set_submenu(filemenu)
        exit = Gtk.MenuItem("Exit")
        exit.connect("activate", Gtk.main_quit)
        filemenu.append(exit)
        mb.append(filem)
        helpmenu = Gtk.Menu()
        helpm = Gtk.MenuItem("Help")
        helpm.set_submenu(helpmenu)
        about = Gtk.MenuItem("About")
        about.connect("activate", self.about_window)
        helpmenu.append(about)
        mb.append(helpm)
        
        self.PyPomoWindow.connect("delete-event", self.on_window_delete)
        self.vbox = Gtk.VBox(False, 5)
        self.label_clock = Gtk.Label()
        self.label_clock.set_markup('<span size="40000">00:00:00</span>')
        self.label_clock.set_line_wrap(True)
        self.vbox.add(self.label_clock)
        self.btn_start = Gtk.Button("Start")
        self.btn_start.connect_after("clicked", self.click_start)
        self.vbox.pack_start(self.btn_start, False, False, 0)
        self.vbox.pack_start(mb, False, False, 0)
        self.PyPomoWindow.add(self.vbox)
        self.PyPomoWindow.show_all()

    def click_start(self, widget):
        """Start de Clock
        """
        GObject.timeout_add_seconds(1, self.count_label)

    def count_label(self):
        """Label of my Clock
        """
        while self.seconds_total <= 1500:
            minute = self.seconds_total / 60
            if self.seconds_total % 60 == 0:
                self.seconds = 0
            self.label_clock.set_markup('<span size="40000">00:%02d:%02d</span>' % (minute, self.seconds))
            self.seconds_total += 1
            self.seconds += 1
            return True
        # self.PyPomoWindow.set_keep_above(True)
        dial = Gtk.Dialog("Alert", self.PyPomoWindow)
        dial.resize(300,50)
        label_dial = Gtk.Label("Your time is over!")
        label_dial.show()
        # dial.set_resizable(False)
        dial.vbox.pack_start(label_dial, False, False, 0)
        answer = dial.run()
        dial.destroy()
        self.restart_clock()
        return False

    def on_window_delete(self, widget, event):
        # return widget.hide_on_delete()
        self.close_window(self)

    def close_window(self, widget):
        self.PyPomoWindow.destroy()
        Gtk.main_quit()

    def about_window(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent (True)
        about_dialog.set_icon_name ("Pypomo")
        about_dialog.set_name('Pypomo')
        about_dialog.set_version('0.1')
        about_dialog.set_copyright("(C) 2012 Misalabs")
        about_dialog.set_comments(("Clock pomodore"))
        about_dialog.set_authors(['Misalabs <arensiatik@gmail.com>'])
        about_dialog.run()
        about_dialog.destroy()


    def restart_clock(self):
        self.seconds = 0
        self.seconds_total = 0
        self.label_clock.set_markup("<span size='40000'>00:00:00</span>")

    def get_resource_path(self, rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def main():
        Gtk.main()

if __name__ == '__main__':
    app = PyPomo()
    Gtk.main()
    sys.exit(0)
