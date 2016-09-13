#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm 

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        layout = QtGui.QVBoxLayout()
        
        self.view = gl.GLViewWidget()
        self.view.setFixedSize(600, 600)
        self.view.setCameraPosition(distance=10000)
        self.view.setCameraPosition(azimuth=180)
        
        grid = gl.GLGridItem()
        grid.scale(1,1,1)
        self.view.addItem(grid)

        loadButton = QtGui.QPushButton("Load")
        loadButton.clicked.connect(self.loadData)

        self.progress = QtGui.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(True)
        
        layout.addWidget(loadButton)
        layout.addWidget(self.view)
        layout.addWidget(self.progress)

        # verts and faces to create a cube
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
        
        self.setLayout(layout)
        self.show()
        
    def loadData(self):
    
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '../Data')
        try:
            with open(self.fileName) as file:
                xyzData = file.readlines()
        except IOError:
            return
        
        #fileName = "/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/Data/DataT300Vx0.3Vy0Vz0R1Energy.xyz"
        #fileName = "/Users/soorinpark/Downloads/DataT300Vx5Vy0Vz0R1Energy.xyz"
        #fileName = "/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/Data/DataT300Vx0.3Vy0Vz0R1.perc"

        #with open(fileName) as file:
        #    xyzData = file.readlines()

        del xyzData[:2]

        self.progress.setMaximum(len(xyzData) * 2 + 1)
        self.progress.setValue(0)

        #xyz = np.empty((len(xyzData), 3), float)
        #xyz = np.empty((0, 3), float)
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
        
        
            
        """
            xyz[i][0] = xyzData[i][0]
            xyz[i][1] = xyzData[i][1]
            xyz[i][2] = xyzData[i][2]
            energy.append(xyzData[i][4])
            """
    
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
        self.view.addItem(m1)
    
        
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

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
