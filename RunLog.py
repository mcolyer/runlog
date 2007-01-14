#!/usr/bin/env python

import os
import gtk
import xml.dom.minidom
from xml import xpath
import re

from SimpleGladeApp import SimpleGladeApp

IPOD_DIR="/media/ipod" # The place where your ipod is mounted
NIKE_PLUS_ID="" # Your Nike+ Serial number goes here you can find it under your ipod in /iPod_Control/Device/Trainer/Workouts/Empeds/
NIKE_PLUS_DATA_NEW="/iPod_Control/Device/Trainer/Workouts/Empeds/"+NIKE_PLUS_ID+"/latest/"
NIKE_PLUS_DATA_OLD="/iPod_Control/Device/Trainer/Workouts/Empeds/"+NIKE_PLUS_ID+"/synched/"

class RunLog(SimpleGladeApp):
    def new(self):
        path = IPOD_DIR+NIKE_PLUS_DATA_OLD
        store = gtk.ListStore(str, str, str, str)

	# Read in the files which have been synced
	for file in os.listdir(path):
		data = {}
    		document = xml.dom.minidom.parse(path+file)
    		data['distance'] = xpath.Evaluate("//distanceString", document)[0].firstChild.data
    		data['time'] = xpath.Evaluate("//durationString", document)[0].firstChild.data
    		data['pace'] = xpath.Evaluate("//pace", document)[0].firstChild.data
    		string = xpath.Evaluate("//time", document)[0].firstChild.data
    		year, month, day = re.match("^([0-9]{4})-([0-9]{2})-([0-9]{2})", string).groups()
    		data['date'] = "%s/%s/%s" % (month, day, year)
		store.prepend((data['date'], data['distance'], data['time'], data['pace']))

	path = IPOD_DIR+NIKE_PLUS_DATA_NEW
	# Read in the files that haven't been synced
	for file in os.listdir(path):
		data = {}
    		document = xml.dom.minidom.parse(path+file)
    		data['distance'] = xpath.Evaluate("//distanceString", document)[0].firstChild.data
    		data['time'] = xpath.Evaluate("//durationString", document)[0].firstChild.data
    		data['pace'] = xpath.Evaluate("//pace", document)[0].firstChild.data
    		string = xpath.Evaluate("//time", document)[0].firstChild.data
    		year, month, day = re.match("^([0-9]{4})-([0-9]{2})-([0-9]{2})", string).groups()
    		data['date'] = "%s/%s/%s" % (month, day, year)
		store.prepend((data['date'], data['distance'], data['time'], data['pace']))

        self.fields = ('Date', 'Distance', 'Total Time', 'Pace')
        self.runViewer.set_model(store)

        for column_index, column_name in enumerate(self.fields):
            column = gtk.TreeViewColumn(column_name, gtk.CellRendererText(), text=column_index)
            column.set_property("resizable", True)
            self.runViewer.append_column(column)

    def main(self):
        gtk.main()

    def quit(self, data):
        gtk.main_quit()

app = RunLog("RunLog.glade")
app.run()

#vim: set ts=4 sw=4 expandtab :
