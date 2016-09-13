#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm
import itertools

class trapViz(QtGui.QWidget):
    def __init__(self):
        super(trapViz, self).__init__()
        
    def loadTrapFile(self, fileName, trapChargeIdCB, plotWidget, trapShapeCB):
    
        self.trapChargeIdCB = trapChargeIdCB
        self.plotWidget = plotWidget
        self.trapShapeCB = trapShapeCB
        
        self.trapChargeIdCB.clear()

        trapFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load Trap File', '../Data')
        try:
            with open(trapFileName) as trapFile:
                trapData = trapFile.readlines()
        except IOError:
            return

        if not ".trap" in trapFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a Trap File")
            return
            
        fileName = "File Name: " + trapFileName
        self.plotWidget.clearItems()

    	dataLen = len(trapData)

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
        self.trapDataDic = {}
        self.plotDic = {}

        for i, j in enumerate(trapData):
            temp = trapData[i].split(' ')
            
            if (len(temp) == 2):
                currentKey = temp[0]
                self.trapDataDic.setdefault(temp[0], [])
                if currentKey not in idList:
                    idList.append(currentKey)
            else:
                self.trapDataDic[currentKey].append(temp)
            
            
        for k,v in self.trapDataDic.iteritems():
            
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
        self.trapChargeIdCB = trapChargeIdCB
        self.trapChargeIdCB.setEnabled(True)
        self.trapChargeIdCB.addItems(["View All"])
        self.trapChargeIdCB.addItems(idList)
        self.trapChargeIdCB.setCurrentIndex(0)

        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])

        
        self.plotWidget = plotWidget
       
        for k,v in self.plotDic.iteritems():
            self.plotWidget.addItem(self.plotDic[k])

        self.plotAlreadyThere = True
        self.previousDataSize = dataLen
        
    def selectTrapChargeID(self):
        
        chargeID = str(self.trapChargeIdCB.currentText())
        if chargeID != "View All":
            for k,v in self.plotDic.iteritems():
                try:
                    plotWidget.removeItem(self.plotDic[k])
                    print "removed: ", k, self.plotDic[k]
                except ValueError:
                    pass
        
        for k,v in self.plotDic.iteritems():
            if k == chargeID:
                print "added: ", k, self.plotDic[k]
                plotWidget.addItem(self.plotDic[k])
        """ 

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

        """

	def trapShapeCB(self):
	
		chargeID = str(self.trapChargeIdCB.currentText())
	
        if chargeID == "View All":
        	chargeID = 0
        	self.trapChargeIdCB.blockSignals(True)
        	self.trapChargeIdCB.setCurrentIndex(1)
        	self.trapChargeIdCB.blockSignals(False)
			    
        if self.trapShapeCB.currentText() == "3D Cube":
            
            self.trapShapeCB.blockSignals(True)
            self.trapShapeCB.removeItem(0)
            self.trapShapeCB.blockSignals(False)
            self.cubeViz(chargeID)

            
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
                
        for site in self.trapDataDic[chargeID]:
        
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
