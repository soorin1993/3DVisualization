#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm
import itertools

class xyzViz(QtGui.QWidget):
    def __init__(self):
        super(xyzViz, self).__init__()
        # add init here

    def loadXYZFile(self, fileName, plotWidget, plotAlreadyThere, xPlaneLabel, yPlaneLabel, zPlaneLabel):
        
        self.plotWidget = plotWidget
        widgetItems = self.plotWidget.items
        prevPlot = []
        
        """
        if len(widgetItems) > 3:
            for i in range(3, len(widgetItems)):
                prevPlot.append(widgetItems[i])
                
        print prevPlot
        self.plotWidget.removeItem(prevPlot)
        """
        
        self.xyzFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load XYZ File', '../Data')
        try:
            with open(self.xyzFileName) as xyzFile:
                self.xyzData = xyzFile.readlines()
        except IOError:
            return

        if not ".xyz" in self.xyzFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a xyz File")
            return
            
        self.xyzFileName.replace("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/Data/", "")
        fileName.setText("File Name: " + self.xyzFileName)
        self.plotWidget.clearItems()

        if plotAlreadyThere:
            for i in range(0, self.previousDataSize):
                self.size[i] = 0
        
        #All the data points
        energy = []

        del self.xyzData[:2]
        dataLen = len(self.xyzData)
        
        self.pos = np.empty((dataLen, 3))
        self.size = np.empty((dataLen))
        self.color = np.empty((dataLen, 4))

        self.coloristhere = False

        for i, j in enumerate(self.xyzData):
            
            self.xyzData[i] = self.xyzData[i].split('\t')
            #print self.xyzData[i]
            del self.xyzData[i][0] # delete "C"
            self.pos[i] = tuple(self.xyzData[i][0:3])
            self.size[i] = .5
            energy.append(self.xyzData[i][3])

        maxPos = self.pos[dataLen - 1]
        self.normEnergy = self.normalizeEnergy(energy)
   		
        for i, j in enumerate(self.normEnergy):
            self.color[i] = matplotlib.cm.hot(self.normEnergy[i])
            self.coloristhere = True

		# insert surfaceArea code here if needed

        self.xMaxPos = int(maxPos[0])
        self.yMaxPos = int(maxPos[1])
        self.zMaxPos = int(maxPos[2])

        xPlaneLabel.setText("X-Plane: Max %i" % self.xMaxPos)
        yPlaneLabel.setText("Y-Plane: Max %i" % self.yMaxPos)
        zPlaneLabel.setText("Z-Plane: Max %i" % self.zMaxPos)

        self.plot = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.plotWidget.addItem(self.plot)
        plotAlreadyThere = True
        self.previousDataSize = dataLen
        
    def makeSurfaceArea(self):
        
        self.surfaceMade = True
        self.newPos = [None] * len(self.pos)
        self.newColor = [None] * len(self.color)

        if self.surfaceAreaButton.isChecked():
           
            self.xPlaneLE.setEnabled(False)
            self.yPlaneLE.setEnabled(False)
            self.zPlaneLE.setEnabled(False)

            for i in range(0, len(self.pos)):
                self.size[i] = 0

            for i in range(0, len(self.pos)):
                
                self.newPos[i] = self.pos[i].tolist()
                self.newColor[i] = self.color[i].tolist()

                if self.pos[i][0] == 0:
                    self.xVerts1.append(self.newPos[i])
                    self.xColors1.append(self.newColor[i])
                    self.size[i] = .5
                
                elif self.pos[i][0] == 14:
                    self.xVerts2.append(self.newPos[i])
                    self.xColors2.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][1] == 0:
                    self.yVerts1.append(self.newPos[i])
                    self.yColors1.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][1] == 14:
                    self.yVerts2.append(self.newPos[i])
                    self.yColors2.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][2] == 0:
                    self.zVerts1.append(self.newPos[i])
                    self.zColors1.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][2] == 14:
                    self.zVerts2.append(self.newPos[i])
                    self.zColors2.append(self.newColor[i])
                    self.size[i] = .5

        else:

            self.xPlaneLE.setEnabled(True)
            self.yPlaneLE.setEnabled(True)
            self.zPlaneLE.setEnabled(True)


    def normalizeEnergy(self, energy):
        
        normEnergy = []
        energy = map(float, energy)
        minEnergy = min(energy)
        maxEnergy = max(energy)

        for i in range(0, len(energy)):
            
            norm = (energy[i] - minEnergy) / (maxEnergy - minEnergy)
            normEnergy.append(norm)
            #print norm
        
        return normEnergy
        
    def cubeViz(self):
    
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

        faceColors = np.array([
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3],
            [1, 0, 0, 0.3]

        ])

        self.cube = verts[faces]
        print self.xyzFileName
        
        with open(self.xyzFileName) as file:
            xyzData = file.readlines()

        del xyzData[:2]

        xyz = np.empty([0,0], float)
        colors = np.zeros(shape=(len(xyzData),4))
        energy = []
        
        maxPos = xyzData[len(xyzData) - 1].split('\t')

        xMax = float(maxPos[1])
        yMax = float(maxPos[2])
        zMax = float(maxPos[3])
        
        for i, j in enumerate(xyzData):
            
            xyzData[i] = xyzData[i].split('\t')
            del xyzData[i][0] # delete "C"
            
            x = float(xyzData[i][0])
            y = float(xyzData[i][1])
            z = float(xyzData[i][2])
            
            if xyz.size == 0:
                xyz = np.array([x, y, z])
            
            """ This is for all data
            else:
                xyz = np.vstack((xyz, [x, y, z]))
            """
            
            # This is for surface Area
            if (x == 0 or x == xMax or y == 0 or y == yMax or z == 0 or z == zMax):
                xyz = np.vstack((xyz, [x, y, z]))
            
            #self.progress.setValue(self.progress.value() + 1)
            energy.append(xyzData[i][3])
  
        normEnergy = self.normalizeEnergy(energy)
        for i in range(0, len(normEnergy)):
            colors[i] = matplotlib.cm.hot(normEnergy[i])
            #self.progress.setValue(self.progress.value() + 1)

        """
        # data that contains [x, y, z, color]
        data = [[0, 0, 0, .5], [0, 0, 1, .25]]
        #data = [[0, 0, 0, .123], [0, 0, 1, .234], [0, 1, 0, .345], [0, 1, 1, .456], [1, 0, 0, .567], [1, 0, 1, .678], [1, 1, 0, .789], [1, 1, 1, .890]]
        data = np.array(data)

        xyz = np.empty((len(data), 3), int)
        colors = np.zeros(shape=(len(data),4))
        #colors = np.array([[1, 0, 0, 1], [0, 1, 0, 1]])

        for i in range(0, len(data)):
            xyz[i][0] = data[i][0]
           xyz[i][1] = data[i][1]
           xyz[i][2] = data[i][2]
            colors[i] = matplotlib.cm.hot(data[i][3])

        """

        colors = colors.repeat(36, axis=0)
        self.cube = np.tile(self.cube, (xyz.shape[0], 1, 1))
        xyz = xyz.repeat(36, axis=0).reshape(self.cube.shape[0],3,3)

        final = self.cube + xyz

        """
        print len(final), len(colors)
        for i in range(0, len(final)):
            print cube[i], "+\n", xyz[i], "=\n",  final[i], "\n|", colors[i]
            print "----------------------------------"
            if (i+1) % 12 == 0:
                print "----------------------------------\n"
        """

        print final.size, colors.size

        m1 = gl.GLMeshItem(vertexes=final, faceColors=colors, smooth=False, computeNormals=False)
        #self.progress.setValue(self.progress.value() + 1)

        m1.setGLOptions('opaque')
        self.plotWidget.addItem(m1)        
        
    
    def changeShape(self, shapeCB, transSlider):
    
        if shapeCB.currentText() == "3D Cube":
            transSlider.blockSignals(True)
            #self.plot.setGLOptions('opaque')
            self.cubeViz()

        else:
            self.plot.setGLOptions('additive')
            transSlider.blockSignals(False)
    
    def changeTrans(self, value):
      
        
        alpha = float(value)/float(100)
        try:
            if self.coloristhere:
                
                for i in range(0, len(self.normEnergy)):
                    self.color[i] = matplotlib.cm.hot(self.normEnergy[i], alpha)

            if value >= 98:
            
                self.plot.setGLOptions('translucent')
       
            else:

                self.plot.setGLOptions('additive')
        except AttributeError:
            QtGui.QMessageBox.about(self, "Error", "Must load a xyz file first.")


    def viewAllAreas(self, viewAll, xPlaneLE, yPlaneLE, zPlaneLE):

            if viewAll.isChecked():

                xPlaneLE.setEnabled(False)
                yPlaneLE.setEnabled(False)
                zPlaneLE.setEnabled(False)
                
                for i in range(0, len(self.pos)):
                    self.size[i] = .5

            else:

                xPlaneLE.setEnabled(True)
                yPlaneLE.setEnabled(True)
                zPlaneLE.setEnabled(True)
    
    def changeViewAreas(self, plotAlreadyThere, xPlaneLE, yPlaneLE, zPlaneLE): 
   
        if not plotAlreadyThere:
            QtGui.QMessageBox.about(self, "Error", "Must load a xyz file first.")

        xPlaneArea = self.parseAreaInput(xPlaneLE, self.xMaxPos)
        yPlaneArea = self.parseAreaInput(yPlaneLE, self.xMaxPos)
        zPlaneArea = self.parseAreaInput(zPlaneLE, self.xMaxPos)
        
        visualizeThese = []
        for i in range(0, len(self.pos)):
            for x in range(0, len(xPlaneArea)):
                for y in range(0, len(yPlaneArea)):
                    for z in range(0, len(zPlaneArea)):
                        self.size[i] = 0
                        if ((self.pos[i][0] == xPlaneArea[x]) and (self.pos[i][1] == yPlaneArea[y]) and (self.pos[i][2] == zPlaneArea[z])): 
                            visualizeThese.append(i)
                            
        for j in range(0, len(visualizeThese)):
            self.size[visualizeThese[j]] = .5
            #print j, self.pos[visualizeThese[j]]

    def parseAreaInput(self, planeArea, maxPos):
        
        planeAreaLE = planeArea
        planeArea = str(planeArea.text())
        planeArea = planeArea.split(",")
        
        temp1 = []
        temp2 = []

        for i in range(0,len(planeArea)):
            if "-" in planeArea[i]:
                
                temp = planeArea[i].split("-")
                foo = int(temp[0]) 
                bar = int(temp[1])
                temp1 = range(foo, bar+1)
                planeArea.extend(temp1)
                temp2.append(planeArea[i])
            
        
        for i in range(0,len(temp2)):
            planeArea.remove(temp2[i])  
    
        if not planeArea[0]:
            planeArea = range(0, maxPos)
            planeAreaLE.setText("0-%i" % maxPos) 
        else:
            planeArea = map(int, planeArea)
            planeArea.sort()

        return planeArea

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

