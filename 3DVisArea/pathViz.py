#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm
import itertools
import json

class pathViz(QtGui.QWidget):
    def __init__(self):
        super(pathViz, self).__init__()

        # add init here

    def loadPathFile(self, fileName, plotWidget, chargeIdCB):
    
        self.plotWidget = plotWidget
        widgetItems = self.plotWidget.items
        prevPlot = []
        
        """
        if len(widgetItems) > 3:
            for i in range(3, len(widgetItems)):
                prevPlot.append(widgetItems[i])
                
        self.plotWidget.removeItem(prevPlot)
        """

        self.chargeIdCB = chargeIdCB
        
        self.pathFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load Path File', '../Data')
        try:
            with open(self.pathFileName) as pathFile:
                pathData = pathFile.readlines()
        except IOError:
            return

        if not ".path" in self.pathFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a Path File")
            return
            
        fileName = "File Name: " + pathFileName
        self.plotWidget.clearItems()
            
    	dataLen = len(pathData)

        self.pos = np.empty((dataLen, 3))
        self.size = np.empty((dataLen))
        self.color = np.empty((dataLen, 4))
      
        self.chargeIdColorCode = {
                
                0: (1, 0, 0, .5), # Red
                1: (1, .5, 0, .5), # Orange
                2: (1, 1, 0, .5), # Yellow
                3: (.5, 1, 0, .5), # Spring Green
                4: (0, 1, 0, .5), # Green
                5: (0, 1, .5, .5), # Turquoise
                6: (0, 1, 1, .5), # Cyan
                7: (0, .5, 1, .5), # Ocean
                8: (0, 0, 1, .5), # Blue
                9: (.5, 0, 1, .5), # Violet
                10: (1, 0, 1, .5), # Magenta
                11: (1, 0, .5, .5), # Raspberry
                12: (51, 255, 255, .5),
                13: (192, 192, 192, .5),
                14: (0, 102, 102, .5),
                15: (102, 51, 0, .5),
                16: (49, 79, 79, .5),
                17: (255, 228, 225, .5),
                18: (240, 128, 128, .5),
                19: (216, 191, 216, .5)

                }


        idList = []
        self.chargeIdDic = {}

        for i, j in enumerate(pathData):
            
            pathData[i] = pathData[i].split(' ')
            self.pos[i] = tuple(pathData[i][0:3])
            
            idList.append(pathData[i][3])
            chargeID = int(pathData[i][3])
            
            if chargeID in self.chargeIdDic.keys():
                self.chargeIdDic.setdefault(chargeID, []).append(i)
            else:
                self.chargeIdDic[chargeID] = [i]

            self.size[i] = .5
            self.color[i] = self.chargeIdColorCode[chargeID]
            
        idList = list(set(idList)) 
        idList.sort()
        
        self.chargeIdCB.setEnabled(True)
        self.chargeIdCB.addItems(["View All"])
        self.chargeIdCB.addItems(idList)
        self.chargeIdCB.setCurrentIndex(0)

        """
        idList = list(set(idList))
        print idList
        self.normID = self.normalizeChargeID(idList)
        
        for i, j in enumerate(self.normID):
            self.color[i] = hot(self.normID[i])
            print self.color[i]
            self.coloristhere = True
        """
            
        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])

        self.plot = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.plotWidget.addItem(self.plot)
        self.plotAlreadyThere = True
        self.previousDataSize = dataLen
                   

    def selectPathChargeID(self, chargeIdCB):
        
        chargeID = chargeIdCB.currentText()
        
        print "ID", chargeID

        if chargeID == "View All":
            for i in range(0, len(self.pos)):
                self.size[i] = .5
        else:
            chargeID = int(chargeID)
            
            for i in range(0, len(self.pos)):
                self.size[i] = 0
               
            

            for k, v in self.chargeIdDic.iteritems():
                for i in range(0, len(self.pos)):
                    if chargeID == k:
                        self.size[v] = .5
                        
    def changeShape(self, shapeCB):
    
        print "shape", shapeCB.currentText()
    
        if shapeCB.currentText() == "3D Cube":
            print "in cube"
            self.cubeViz()

        else:
            self.plot.setGLOptions('additive')

    def cubeViz(self):
    
        self.plotWidget.clearItems()

    
        verts = np.array([
            [0, 0, 0], #0
            [0, 0, 1], #1
            [0, 1, 0], #2
            [0, 1, 1], #3
            [1, 0, 0], #4
            [1, 0, 1], #5
            [1, 1, 0], #6
            [1, 1, 1] #7
            ])

        faces = np.array([
            [0, 4, 6],
            [0, 6, 2],
            [1, 5, 7],
            [1, 7, 3],
            [2, 6, 3],
            [3, 7, 6],
            [0, 4, 1],
            [1, 5, 4],
            [4, 5, 7],
            [4, 6, 7],
            [0, 1, 3],
            [0, 2, 3]
            ])

        self.cube = verts[faces]
        
        with open(self.pathFileName) as file:
            pathData = file.readlines()

        xyz = np.empty([0,0], float)
        colors = np.zeros(shape=(len(pathData),4))
        
        maxPos = pathData[len(pathData) - 1].split(' ')

        xMax = float(maxPos[0])
        yMax = float(maxPos[1])
        zMax = float(maxPos[2])
        
        self.pathDataDic = {}
        idList = []
        
        print "0"
        
        """
        for i, j in enumerate(pathData):
            
            temp = pathData[i].split(' ')
            chargeID = temp[3]
            data = [temp[0], temp[1], temp[2], temp[4], temp[5]]
            
            if chargeID in self.pathDataDic.keys():
                self.pathDataDic.setdefault(chargeID, []).append(data)
            else:
                self.chargeIdDic[chargeID] = data
            
            
            self.pathDataDic.setdefault(temp[3], [temp[0], temp[1], temp[2], temp[3], temp[4]])
     
            if currentKey not in idList:
                idList.append(currentKey)    
            
            else:
                self.pathDataDic[currentKey].append([temp[0], temp[1], temp[2], temp[3], temp[4]])  
              
                
        print "1"
        print self.pathDataDic
        """
        
        self.pathDataDic = {}
        self.IdList = []
               
        for i, j in enumerate(pathData):
            
            pathData[i] = pathData[i].split(' ')
                        
            x = float(pathData[i][0])
            y = float(pathData[i][1])
            z = float(pathData[i][2])
            chargeID = int(pathData[i][3])
            currentTime = float(pathData[i][4])
            globalTime = float(pathData[i][5])
            
            # currently not using any time values
                        
            if xyz.size == 0:
                xyz = np.array([x, y, z])
            else:
                xyz = np.vstack((xyz, [x, y, z]))
                    
            self.color[i] = self.chargeIdColorCode[chargeID]
            #print self.color[i]
            
            if chargeID in self.pathDataDic.keys():
                self.pathDataDic[chargeID].append([x, y, z])
            else:
                self.pathDataDic[chargeID] = [x, y, z]
            
            #print self.pathDataDic
                
        #print json.dumps(self.pathDataDic, indent=4)
        print "2"


        colors = colors.repeat(36, axis=0)
        self.cube = np.tile(self.cube, (xyz.shape[0], 1, 1))
        xyz = xyz.repeat(36, axis=0).reshape(self.cube.shape[0],3,3)

        final = self.cube + xyz

        print "3"

        m1 = gl.GLMeshItem(vertexes=final, faceColors=colors, smooth=True, computeNormals=True)
        #self.progress.setValue(self.progress.value() + 1)

        m1.setGLOptions('opaque')
        self.plotWidget.addItem(m1)
