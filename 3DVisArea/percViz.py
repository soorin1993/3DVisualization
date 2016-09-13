#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm 
import itertools
import json
from sklearn.utils.extmath import cartesian

class percViz(QtGui.QWidget):
    def __init__(self):
        super(percViz, self).__init__()
        #main = MainWindow.MainWindow()

    def loadPercFile(self, fileName, percChargeIdCB, plotWidget, percShapeCB):
    	
    	self.plotWidget = plotWidget
    	self.percShapeCB = percShapeCB
    	self.percChargeIdCB = percChargeIdCB
    	
        percFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load Perc File', '../Data')
        try:
            with open(percFileName) as percFile:
                percData = percFile.readlines()
        except IOError:
            return

        if not ".perc" in percFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a Perc File")
            return
            
        fileName = "File Name" + percFileName
        self.plotWidget.clearItems() 
  
    	dataLen = len(percData)

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
        self.percDataDic = {}
        self.plotDic = {}

        for i, j in enumerate(percData):
        
            temp = percData[i].split(' ')
            
            if (len(temp) == 2):
                currentKey = int(temp[0])
                self.percDataDic.setdefault(currentKey, [])
                if currentKey not in idList:
                    idList.append(temp[0])
            else:
            	x = int(temp[0])
            	y = int(temp[1])
            	z = int(temp[2])
            	timeSpent = float(temp[3])
            	
                self.percDataDic[currentKey].append([x, y, z])
            
            
        for k,v in self.percDataDic.iteritems():
            
            dataLen = len(v)

            self.pos = np.empty((dataLen,3))
            self.size = np.empty((dataLen))
            self.color = np.empty((dataLen,4))

            for i,j in enumerate(v):
                
                self.pos[i] = tuple(v[i][0:3])
                self.size[i] = .5
                self.color[i] = self.chargeIdColorCode[int(k)]

            self.plotDic[k] = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)

        idList.sort()        
        self.percChargeIdCB = percChargeIdCB
        self.percChargeIdCB.setEnabled(True)
        self.percChargeIdCB.addItems(["View All"])
        self.percChargeIdCB.addItems(idList)
        self.percChargeIdCB.setCurrentIndex(0)

        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])

        
        self.plotWidget = plotWidget
       
        for k,v in self.plotDic.iteritems():
            self.plotWidget.addItem(self.plotDic[k])

        self.plotAlreadyThere = True
        self.previousDataSize = dataLen
                        
    def selectPercChargeID(self):
      
        chargeID = self.percChargeIdCB.currentText()
        
        if self.percShapeCB.currentText() == "3D Cube":
            self.cubeViz(int(chargeID))

        if chargeID != "View All":
            for k,v in self.plotDic.iteritems():
                try:
                    self.plotWidget.removeItem(self.plotDic[k])
                    print "removed: ", k, self.plotDic[k]
                except ValueError:
                    pass
        
        for k,v in self.plotDic.iteritems():
            if k == chargeID:
                print "added: ", k, self.plotDic[k]
                self.plotWidget.addItem(self.plotDic[k])
        
    def changeShape(self):
    
        chargeID = str(self.percChargeIdCB.currentText())
        
        if chargeID == "View All":
        	chargeID = 0
        	self.percChargeIdCB.blockSignals(True)
        	self.percChargeIdCB.setCurrentIndex(1)
        	self.percChargeIdCB.blockSignals(False)
			    
        if self.percShapeCB.currentText() == "3D Cube":
            
            self.percShapeCB.blockSignals(True)
            self.percShapeCB.removeItem(0)
            self.percShapeCB.blockSignals(False)
            self.cubeViz(chargeID)

        else:
            self.plot.setGLOptions('additive')

    def cubeViz(self, chargeID):
    
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
        
        chargeVisited = {}
        
        maxSite = 0
        minSite = 0
        
        #xyz = np.empty([0,0], float)
                
        for site in self.percDataDic[chargeID]:
        
            if maxSite == 0:
                maxSite = max(site)
            elif max(site) > maxSite:
                maxSite = max(site)
                
            if minSite == 0:
                minSite = min(site)
            elif min(site) < minSite:
                minSite = min(site)
                
            site = tuple(site)
            if site in chargeVisited.keys():
                chargeVisited[site]+= 1
            else:
                chargeVisited[site] = 0
        
        temp = range(minSite, maxSite + 1)
        
        xyz = cartesian((temp, temp, temp))
        temp = []

        colors = np.zeros(shape=(len(xyz), 4))
        
        for k,v in chargeVisited.iteritems():
            for i, j in enumerate(xyz):
                if k == tuple(j):
                    
                    colors[i] = self.chargeIdColorCode[v]
                    temp.append(i)
                
                elif (k != tuple(j)) and (i not in temp):
                    colors[i] = (1, 1, 1, .1)
        

        colors = colors.repeat(36, axis=0)
        self.cube = np.tile(self.cube, (xyz.shape[0], 1, 1))
        xyz = xyz.repeat(36, axis=0).reshape(self.cube.shape[0],3,3)

        final = self.cube + xyz

        m1 = gl.GLMeshItem(vertexes=final, faceColors=colors, smooth=False, vertexColors=colors)
        m1.setGLOptions('translucent')
        self.plotWidget.addItem(m1)
