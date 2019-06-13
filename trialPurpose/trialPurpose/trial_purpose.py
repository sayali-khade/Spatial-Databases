# -*- coding: utf-8 -*-
"""
/***************************************************************************
 trialPurpose
                                 A QGIS plugin
 tp
                              -------------------
        begin                : 2019-04-20
        git sha              : $Format:%H$
        copyright            : (C) 2019 by sayali khade
        email                : sayalikhade@gmail.com
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


#from PyQt4 import QtCore
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from trial_purpose_dialog import trialPurposeDialog
import os.path
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer, QgsDataSourceURI
from qgis.core import *
from PyQt4.QtGui import *  
import qgis
from PyQt4.QtSql import QSqlDatabase
from qgis.gui import *
from qgis.networkanalysis import *
from collections import *

try:
    from PyQt4.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = type("")

rbDict = {}

class trialPurpose:
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
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'trialPurpose_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&trial_purpose')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'trialPurpose')
        self.toolbar.setObjectName(u'trialPurpose')

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
        return QCoreApplication.translate('trialPurpose', message)


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
        self.dlg = trialPurposeDialog()

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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/trialPurpose/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'trial'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&trial_purpose'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_list = []
       
        for layer in layers:
            layer_list.append(layer.name())

        print(layer_list)
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        self.dlg.qlkbtn1.clicked.connect(self.onClickBtn1)
        self.dlg.qlkbtn2.clicked.connect(self.onClickBtn2)
        self.dlg.qlkbtn3.clicked.connect(self.onClickBtn3)


        # Reuse the path to DB to set database name
        uri = QgsDataSourceURI()
        uri.setDatabase('F:/UTA/SEM 5/Adv DB/UTA_Final_DB/test.sqlite')
        db = QSqlDatabase.addDatabase('QSPATIALITE');
        db.setDatabaseName(uri.database())

        polygonNameList=[]
        polygonTypeList = []
        placemarksNameList = []
        if db.open():            
            query = db.exec_(""" SELECT name FROM Final_poly ORDER BY name """)
            while query.next():
                record = query.record()
                polygonNameList.append(record.value(0))

            query = db.exec_(""" SELECT distinct btype FROM final_poly where btype NOT NULL """)
            while query.next():
                record = query.record()
                polygonTypeList.append(record.value(0))
                #print(polygonTypeList)

            query = db.exec_(""" SELECT distinct name FROM Final_point ORDER BY name """)
            while query.next():
                record = query.record()
                placemarksNameList.append(record.value(0))
                
        #self.dlg.polygonCombo.clear()
        self.dlg.qcombo1.clear()
        self.dlg.qcombo2.clear()
        self.dlg.q2combo.clear()
        self.dlg.q3combo1.clear()
        self.dlg.q3combo2.clear()


        self.dlg.qcombo1.addItems(polygonNameList)
        self.dlg.qcombo2.addItems(polygonTypeList)
        self.dlg.q2combo.addItems(polygonNameList)
        self.dlg.q3combo1.addItems(placemarksNameList)
        self.dlg.q3combo2.addItems(placemarksNameList)

        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

   
    
    def onClickBtn1(self):
        print('onClickBtn1')
        dist_range = self.dlg.numberOfElements.text()
        aptName = self.dlg.qcombo1.currentText()
        aptType = self.dlg.qcombo2.currentText()

        # Reuse the path to DB to set database name
        uri = QgsDataSourceURI()
        uri.setDatabase('F:/UTA/SEM 5/Adv DB/UTA_Final_DB/test.sqlite')
        db = QSqlDatabase.addDatabase('QSPATIALITE');
        db.setDatabaseName(uri.database())
        
        myList=[]
        
        if db.open():       
            query = db.exec_("SELECT src.id,src.name From Final_poly src, Final_poly dest where st_contains(st_buffer(st_transform(dest.geom, 3857), {0}), st_transform(src.geom,3857)) AND dest.name='{1}' AND src.Btype='{2}'   ".format(dist_range,aptName,aptType));
            while query.next():
                record = query.record()
                myList.append(record.value(0))

            print(myList)
            selectedLayerIndex = "final_poly"
            self.iface.setActiveLayer(QgsMapLayerRegistry.instance().mapLayersByName( selectedLayerIndex )[0])
            layer = self.iface.activeLayer()
            self.iface.mapCanvas().setSelectionColor( QColor('red'))
            layer.selectByIds(myList)

    def onClickBtn2(self):
        print('onClickBtn2')
      
        aptName = self.dlg.q2combo.currentText()
        
        # Reuse the path to DB to set database name
        uri = QgsDataSourceURI()
        uri.setDatabase('F:/UTA/SEM 5/Adv DB/UTA_Final_DB/test.sqlite')
        db = QSqlDatabase.addDatabase('QSPATIALITE');
        db.setDatabaseName(uri.database())
        
        myList=[]
        
        if db.open():       
            query = db.exec_("Select id from Final_poly where name='{0}'".format(aptName));
            while query.next():
                record = query.record()
                myList.append(record.value(0))

            print(myList)
            selectedLayerIndex = "final_poly"
            self.iface.setActiveLayer(QgsMapLayerRegistry.instance().mapLayersByName( selectedLayerIndex )[0])
            layer = self.iface.activeLayer()
            self.iface.mapCanvas().setSelectionColor( QColor('green'))
            layer.selectByIds(myList)
    
    def find_shortest_path(self,graph, start, end, path =[]): 
        path = path + [start] 
        if start == end: 
            return path 
        shortest = None
        for node in graph[start]: 
            if node not in path: 
                newpath = self.find_shortest_path(graph, node, end, path) 
                if newpath: 
                    if not shortest or len(newpath) < len(shortest): 
                        shortest = newpath 
        return shortest 
    
   

    def onClickBtn3(self):
     # Reuse the path to DB to set database name
        uri = QgsDataSourceURI()
        uri.setDatabase('F:/UTA/SEM 5/Adv DB/UTA_Final_DB/test.sqlite')
        db = QSqlDatabase.addDatabase('QSPATIALITE');
        db.setDatabaseName(uri.database())
        FromL = self.dlg.q3combo1.currentText()
        ToL = self.dlg.q3combo2.currentText()

        FromLocation=[]
        ToLocation=[]
        
        if db.open():       
            query = db.exec_("SELECT * from Final_line");
            while query.next():
                record = query.record()
                if(record.value(14)!=None and record.value(15)!=None):
                    FromLocation.append(record.value(14))
                    ToLocation.append(record.value(15))
               
        print(type(FromLocation))
       
        graph=defaultdict(list)
        for i in range(0,len(FromLocation)):
            graph[FromLocation[i]].append(ToLocation[i])
    
        print(graph)
        print(self.find_shortest_path(graph,FromL,ToL))


