#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Listado de puertos de jack en GTK+ 3
"""

###########################################
### Primero conectamos a Dbus ###
###########################################
import dbus
bus = dbus.SessionBus()

jack_control = bus.get_object("org.jackaudio.service", "/org/jackaudio/Controller")

port_list = jack_control.GetAllPorts()

############################################
### Ahora la Gui ###
############################################

from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self):
       Gtk.Window.__init__(self, title="Listado de Puertos Jack")
       self.set_default_size(200, 200)
       model = self.__create_model(port_list)
       sw = Gtk.ScrolledWindow()
       treeView = Gtk.TreeView(model)
       cellRenderer = Gtk.CellRendererText()
       column = Gtk.TreeViewColumn("Puertos", cellRenderer, text=0)
       treeView.append_column(column)
       sw.add(treeView)
       self.add(sw)

    def __create_model(self, item_list):
        model = Gtk.ListStore(str)
        for item in item_list:
            model.append([item])
        return model


    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
