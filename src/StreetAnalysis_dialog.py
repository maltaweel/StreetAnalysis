# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StreetAnalysisDialog
                                 A QGIS plugin
 Analysis for Streets
                             -------------------
        begin                : 2018-11-11
        copyright            : (C) 2018 by Mark Altaweel
        email                : maltaweel@ucl.ac.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

'''
The  imports
'''
import os

from PyQt4 import QtGui, uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'StreetAnalysis_dialog_base.ui'))


class StreetAnalysisDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Constructor
        QtGui.QDialog-- the GUI dialog used to build the gui part of the plugin.
        FORM_CLASS-- the base user interface form that shapes how the plugin gui looks like to the user.
        """
        super(StreetAnalysisDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        layout=QtGui.QVBoxLayout(self)

        children=self.findChildren(QtGui.QRadioButton)

	self.choices=[]

	for child in children:
		if child.isChecked() is True:
			self.choices.append(child)

#	self.r1 = QtGui.QRadioButton("Street Network Analysis")
#	self.r2=QtGui.QRadioButton("Graph Analysis")
#	layout.addWidget(self.r1)
#	layout.addWidget(self.r2)
	self.setupUi(self)
	
