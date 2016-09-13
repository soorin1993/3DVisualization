#!/usr/bin/env python
"""

OPV GUI
Written by Soo Park 2016 for Shaheen Group @ CU Boulder
Contact: soo.park@colorado.edu

"""

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
from matplotlib.cm import *
import itertools

import xyzViz, pathViz, percViz, trapViz

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # import modules
        xyz = xyzViz.xyzViz()
        path = pathViz.pathViz()
        perc = percViz.percViz()
        trap = trapViz.trapViz()
        
        # main layout declaration
        self.mainLayout = QtGui.QHBoxLayout() # main layout. plotLayout - xyzLayout - pathLayout
        self.plotLayout = QtGui.QVBoxLayout() # plot layout. 
        self.axisLabelLayout = QtGui.QHBoxLayout()
        self.xyzWidgetLayout = QtGui.QVBoxLayout() # xyzWidgetsLayout that is used for the xyzWidgets QGroupBox
        self.xyzLayout = QtGui.QVBoxLayout() # xyzLayout that contains xyzWidgets.
        self.pathWigetsLayout = QtGui.QVBoxLayout()
        self.pathLayout = QtGui.QVBoxLayout()
        self.percWidgetsLayout = QtGui.QVBoxLayout()
        self.percLayout = QtGui.QVBoxLayout()
        self.trapWidgetsLayout = QtGui.QVBoxLayout()
        self.trapLayout = QtGui.QVBoxLayout()
        self.paramWidgetsLayout = QtGui.QVBoxLayout()
        self.paramLayout = QtGui.QVBoxLayout()
        
		# Plotting and Grids
        self.plotWidget = gl.GLViewWidget()
        self.plotWidget.setFixedSize(600, 600)
        self.plotWidget.opts['distance'] = 100

        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        
        self.plotWidget.addItem(xgrid)
        self.plotWidget.addItem(ygrid)
        self.plotWidget.addItem(zgrid)

        xgrid.setSize(30, 30, 30)
        ygrid.setSize(30, 30, 30)
        zgrid.setSize(30, 30, 30)

        xgrid.translate(-15, 15, 0)
        ygrid.translate(15, 15, 0)
        zgrid.translate(15, 15, 0)

        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        xgrid.scale(1, 1, 1)
        ygrid.scale(1, 1, 1)
        zgrid.scale(1, 1, 1)
    
        pos = np.array([[30, 0, 0], [0, 30, 0], [0, 0, 30]])
        size = np.array([5, 5, 5])
        color = np.array([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])

        axis = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        axis.setGLOptions('translucent')
        self.plotWidget.addItem(axis)
       
        #self.axisLabelLayout.setContentsMargins(0, -10, 0, -10)
        self.axisLabelLayout.setSpacing(0)

        self.fileNameLabel = QtGui.QLabel("File Name: ")
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignLeft)
        spacer1 = QtGui.QSpacerItem(330, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        red = QtGui.QLabel()
        redImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/images/red_circle.png")
        redSmall = redImg.scaledToWidth(10)
        red.setPixmap(redSmall)
        red.setAlignment(QtCore.Qt.AlignLeft)
        redLabel = QtGui.QLabel("   - X-axis        ")
        redLabel.setAlignment(QtCore.Qt.AlignLeft)

        green = QtGui.QLabel()
        greenImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/images/green_circle.png")
        greenSmall = greenImg.scaledToWidth(10)
        green.setPixmap(greenSmall)
        green.setAlignment(QtCore.Qt.AlignLeft)
        greenLabel = QtGui.QLabel(" - Y-axis        ")
        greenLabel.setAlignment(QtCore.Qt.AlignLeft)

        blue = QtGui.QLabel()
        blueImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/images/blue_circle.png")
        blueSmall = blueImg.scaledToWidth(10)
        blue.setPixmap(blueSmall)
        blue.setAlignment(QtCore.Qt.AlignLeft)
        blueLabel = QtGui.QLabel("  - Z-axis        ")
        blueLabel.setAlignment(QtCore.Qt.AlignLeft)
        
        self.axisLabelLayout.addWidget(red)
        self.axisLabelLayout.addWidget(redLabel)
        self.axisLabelLayout.addWidget(green)
        self.axisLabelLayout.addWidget(greenLabel)
        self.axisLabelLayout.addWidget(blue)
        self.axisLabelLayout.addWidget(blueLabel)
        self.axisLabelLayout.addItem(spacer1)

        
        #self.plotLayout.addWidget(self.fileNameLabel)
        self.plotLayout.addLayout(self.axisLabelLayout)

        self.plotAlreadyThere = False
        self.currentPlotObj = None

        """
        XYZ Visualization
        """ 
        self.xyzWidgets = QtGui.QGroupBox("XYZ Visualization")

        loadButton = QtGui.QPushButton("Load XYZ File")
        
        xyzShapeLabel = QtGui.QLabel("Shape")
        self.xyzShapeCB = QtGui.QComboBox()
        self.xyzShapeCB.addItems(["Circle", "3D Cube"])
        self.xyzShapeCB.setCurrentIndex(0)

        transLabel = QtGui.QLabel("Transparency")
        self.transSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.transSlider.valueChanged[int].connect(xyz.changeTrans)

        visibleAreas = QtGui.QGroupBox("Visible Areas")
        visibleAreas.setToolTip("Cannot excede the maximum number indicated next to the labels")
        visibleAreasLayout = QtGui.QVBoxLayout()
        self.viewAll = QtGui.QRadioButton("View All Areas")

        self.surfaceAreaButton = QtGui.QRadioButton("Surface Area")
        self.surfaceAreaButton.toggled.connect(xyz.makeSurfaceArea)

        self.xPlaneLabel = QtGui.QLabel("X-Plane")
        self.xPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        self.yPlaneLabel = QtGui.QLabel("Y-Plane")
        self.yPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        self.zPlaneLabel = QtGui.QLabel("Z-Plane")
        self.zPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        
        self.xPlaneLE = QtGui.QLineEdit()
        self.yPlaneLE = QtGui.QLineEdit()
        self.zPlaneLE = QtGui.QLineEdit()

        submitButton = QtGui.QPushButton("Submit")

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
                
        doge = QtGui.QLabel()
        dogeImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/images/dogeicon.png")
        dogeSmall = dogeImg.scaledToWidth(100)
        doge.setPixmap(dogeSmall)
        doge.setAlignment(QtCore.Qt.AlignCenter)

        visibleAreasLayout.addWidget(self.viewAll)
        visibleAreasLayout.addWidget(self.surfaceAreaButton)
        visibleAreasLayout.addWidget(self.xPlaneLabel)
        visibleAreasLayout.addWidget(self.xPlaneLE)
        visibleAreasLayout.addWidget(self.yPlaneLabel)
        visibleAreasLayout.addWidget(self.yPlaneLE)
        visibleAreasLayout.addWidget(self.zPlaneLabel)
        visibleAreasLayout.addWidget(self.zPlaneLE)
        visibleAreasLayout.addWidget(submitButton)
        visibleAreas.setLayout(visibleAreasLayout)

        # adding widgets to respective layouts
        self.xyzWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.xyzWidgetLayout.addWidget(loadButton)
        self.xyzWidgetLayout.addWidget(xyzShapeLabel)
        self.xyzWidgetLayout.addWidget(self.xyzShapeCB)
        self.xyzWidgetLayout.addWidget(transLabel)
        self.xyzWidgetLayout.addWidget(self.transSlider)
        self.xyzWidgetLayout.addWidget(visibleAreas) # Doesn't work currently.
        self.xyzWidgetLayout.addItem(spacer)
        self.xyzWidgetLayout.addWidget(doge)
        self.xyzWidgets.setLayout(self.xyzWidgetLayout)
        
        # connections
        submitButton.clicked.connect(lambda: xyz.changeViewAreas(self.plotAlreadyThere, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE))
        loadButton.clicked.connect(lambda: xyz.loadXYZFile(self.fileNameLabel, self.plotWidget, self.plotAlreadyThere, self.xPlaneLabel, self.yPlaneLabel, self.zPlaneLabel))
        self.xyzShapeCB.currentIndexChanged.connect(lambda: xyz.changeShape(self.xyzShapeCB, self.transSlider))
        self.viewAll.toggled.connect(lambda: xyz.viewAllAreas(self.viewAll, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE))

        """
        PATH Visualization
        """ 
        self.pathWidgets = QtGui.QGroupBox("Path Visualization")
        self.pathWidgetLayout = QtGui.QVBoxLayout()

        self.loadPathButton = QtGui.QPushButton("Load Path File")

        self.pathChargeIdLabel = QtGui.QLabel("Charge ID")
        self.pathChargeIdCB = QtGui.QComboBox()
        self.pathChargeIdCB.setEnabled(False)
        
        pathShapeLabel = QtGui.QLabel("Shape")
        self.pathShapeCB = QtGui.QComboBox()
        self.pathShapeCB.addItems(["Circle", "3D Cube"])
        self.pathShapeCB.setCurrentIndex(0)

        self.pathWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pathWidgetLayout.addWidget(self.loadPathButton)
        self.pathWidgetLayout.addWidget(self.pathChargeIdLabel)
        self.pathWidgetLayout.addWidget(self.pathChargeIdCB)
        self.pathWidgetLayout.addWidget(pathShapeLabel)
        self.pathWidgetLayout.addWidget(self.pathShapeCB)
        self.pathWidgets.setLayout(self.pathWidgetLayout)
        
        self.loadPathButton.clicked.connect(lambda: path.loadPathFile(self.fileNameLabel, self.plotWidget, self.pathChargeIdCB))
        self.pathChargeIdCB.currentIndexChanged.connect(lambda: path.selectPathChargeID(self.pathChargeIdCB))
        self.pathShapeCB.currentIndexChanged.connect(lambda: path.changeShape(self.pathShapeCB))

    
        """
        PERC Visualization
        """
        self.percWidgets = QtGui.QGroupBox("Perc Visualization")
        self.percWidgetLayout = QtGui.QVBoxLayout()
        
        self.loadPercButton = QtGui.QPushButton("Load Perc File")
        
        self.percChargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.percChargeIdCB = QtGui.QComboBox()
        self.percChargeIdCB.setEnabled(False)
       
        percShapeLabel = QtGui.QLabel("Shape")
        self.percShapeCB = QtGui.QComboBox()
        self.percShapeCB.addItems(["Circle", "3D Cube"])
        self.percShapeCB.setCurrentIndex(0)

        self.percWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.percWidgetLayout.addWidget(self.loadPercButton)
        self.percWidgetLayout.addWidget(self.percChargeIdLabel)
        self.percWidgetLayout.addWidget(self.percChargeIdCB)
        self.percWidgetLayout.addWidget(percShapeLabel)
        self.percWidgetLayout.addWidget(self.percShapeCB)
        self.percWidgets.setLayout(self.percWidgetLayout)
        
        self.percChargeIdCB.currentIndexChanged.connect(lambda: perc.selectPercChargeID())
        self.loadPercButton.clicked.connect(lambda: perc.loadPercFile(self.fileNameLabel, self.percChargeIdCB, self.plotWidget, self.percShapeCB))
        self.percShapeCB.currentIndexChanged.connect(lambda: perc.changeShape())

        """
        TRAP Visualization
        """
        self.trapWidgets = QtGui.QGroupBox("Trap Visualization")
        self.trapWidgetLayout = QtGui.QVBoxLayout()
        
        self.loadTrapButton = QtGui.QPushButton("Load Trap File")
        
        self.trapChargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.trapChargeIdCB = QtGui.QComboBox()
        self.trapChargeIdCB.setEnabled(False)

        self.trapShapeCB = QtGui.QComboBox()
        self.trapShapeCB.addItems(["Circle", "3D Cube"])
        self.trapShapeCB.setCurrentIndex(0)
        
        self.trapChargeIdCB.currentIndexChanged.connect(lambda: trap.selectTrapChargeID())
        self.loadTrapButton.clicked.connect(lambda: trap.loadTrapFile(self.fileNameLabel, self.trapChargeIdCB, self.plotWidget, self.trapShapeCB))
        self.trapShapeCB.currentIndexChanged.connect(lambda: trap.changeShape())

        self.trapWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.trapWidgetLayout.addWidget(self.loadTrapButton)
        self.trapWidgetLayout.addWidget(self.trapChargeIdLabel)
        self.trapWidgetLayout.addWidget(self.trapChargeIdCB)
        self.trapWidgets.setLayout(self.trapWidgetLayout)
    
        """
        CONFIG layout
        """    
        
        """
        self.paramWidgets = QtGui.QGroupBox("Parameters")

        self.primaryLayout = QtGui.QVBoxLayout()
        self.secondaryLayout = QtGui.QGridLayout()
        
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setLayout(self.secondaryLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.loadParamButton = QtGui.QPushButton("Load Param File")
        #self.loadParamButton.clicked.connect(self.loadParamFile)
       
        self.saveButton = QtGui.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveFile)

        self.primaryLayout.addWidget(self.loadButton)
        self.primaryLayout.addWidget(self.saveButton)
        self.primaryLayout.addWidget(self.scrollArea)
       
        self.paramDic = []
        index = 0
        config = self.parseConfig()
        
        for key1, val1 in config.iteritems():
            for param in val1:
                #print param
                for key2, val2 in param.iteritems():
                    
                    if len(val2) == 1:
                        
                        self.paramName = QtGui.QLabel(key2)
                        self.paramName.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        self.lineEdit = QtGui.QLineEdit()
                        self.lineEdit.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.lineEdit, index, 1)
                        
                        self.paramObjects = []
                        self.paramObjects.append(self.paramName)
                        self.paramObjects.append(self.lineEdit)
                        self.paramDic.append(self.paramObjects)

                    else:
                        
                        #print key2, val2
                        self.paramName = QtGui.QLabel(key2)
                        self.paramName.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        self.comboBox = QtGui.QComboBox()
                       
                        for index2 in range(0, len(val2)):
                            if index2 > 0:
                                
                                self.comboBox.addItems(str(val2[index2]))
                                self.comboBox.setCurrentIndex(-1)
                                self.comboBox.setToolTip(val2[0])
                                self.secondaryLayout.addWidget(self.comboBox, index, 1)

                        self.paramObjects = []
                        self.paramObjects.append(self.paramName)
                        self.paramObjects.append(self.comboBox)
                        self.paramDic.append(self.paramObjects)
                               

                        if key2 == "method":
                            
                            self.comboBox.currentIndexChanged.connect(lambda: self.methodParamSetup())
                            

                    index = index + 1
   
        """
        # testing purposes
        #for index3, value3 in enumerate(self.paramDic):
        #    print self.paramDic[index3][0].text()

        #self.trapWidgets.setLayout(self.secondaryLayout)
				    
        self.xyzLayout.addWidget(self.xyzWidgets)
        self.plotLayout.addWidget(self.plotWidget)
        self.pathLayout.addWidget(self.pathWidgets)
        self.percLayout.addWidget(self.percWidgets)
        self.trapLayout.addWidget(self.trapWidgets)

        self.mainLayout.addLayout(self.plotLayout)
        self.mainLayout.addLayout(self.xyzLayout)
        self.mainLayout.addLayout(self.pathLayout)
        self.mainLayout.addLayout(self.percLayout)
        self.mainLayout.addLayout(self.trapLayout)


        self.previousDataSize = 0
        self.surfaceMade = False

        self.meshVerts = []
        self.xVerts1 = []
        self.xVerts2 = []
        self.yVerts1 = []
        self.yVerts2 = []
        self.zVerts1 = []
        self.zVerts2 = []
        self.xColors1 = []
        self.xColors2 = []
        self.yColors1 = []
        self.yColors2 = []
        self.zColors1 = []
        self.zColors2 = []

        self.setLayout(self.mainLayout)
        self.resize(800, 600)
        self.setWindowTitle("3D Visualization Area")
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
