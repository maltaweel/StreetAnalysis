# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StreetAnalysis
                                 A QGIS plugin
 Analysis for Streets
                              -------------------
        begin                : 2018-11-11
        git sha              : $Format:%H$
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
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QPushButton


from PyQt5.QtGui import QIcon 

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QTranslator
from PyQt5.QtCore import qVersion
from PyQt5.QtCore import QCoreApplication


# Initialize Qt resources from file resources.py
# Import the code for the dialog

import subprocess
import os


import loadApplyModel
import networkAnalysis 
from StreetAnalysis_dialog import StreetAnalysisDialog

class StreetAnalysis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        self.locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'StreetAnalysis_{}.qm'.format(locale))

        if os.path.exists(self.locale_path):
            self.translator = QTranslator()
            self.translator.load(self.locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&StreetAnalysis')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'StreetAnalysis')
        self.toolbar.setObjectName(u'StreetAnalysis')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('StreetAnalysis', message)
 
    '''
    Method to run and launch the gui based on selected options by the user.
     '''
    def runThis(self):
        app = QApplication([])
        qid = QFileDialog()
        win = QMainWindow()
        #	win.closeEvent=
        win.setWindowFlags(0)
        win.setFixedSize(QSize(1000,1000))
        win.show()
        
        dir=self.locale_path.split("i18n")[0]
	
        fine=os.path.join(dir,'help.pdf')
        if os.name=='posix':
            subprocess.Popen([fine],shell=True) 
        else:
            os.startfile('example.pdf')
            
            

	
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = StreetAnalysisDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/StreetAnalysis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&StreetAnalysis'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""

        self.dlg.show()
        result=self.dlg.exec_()

        children=self.dlg.findChildren(QRadioButton)
        secondChildren=self.dlg.findChildren(QPushButton)

        self.choices=[]
        for child in children:
            if child.isChecked() is True:
                print('child')
                self.choices.append(child)

        for c in secondChildren:
            if c.isEnabled():
                self.choices.append(c)				

        #show the dialog
        #self.dlg.show()

        #Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            for c in self.choices:
                if c.text() == "Street Network Analysis":
                    loadApplyModel.run()

                elif c.text()=="Road Graph Analysis":
                    networkAnalysis.run()

                elif c.text()=='?':
                    self.runThis()
            
