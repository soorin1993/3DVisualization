#Just the surface area
        
        for i, j in enumerate(xyzData):

            xyzData[i] = xyzData[i].split('\t')

            del xyzData[i][0]
            del xyzData[i][3]
            del xyzData[i][3]

            #print xyzData[i]

            if float(xyzData[i][0]) >= xMax:
                xMax = float(xyzData[i][0])

            if float(xyzData[i][1]) >= yMax:
                yMax = float(xyzData[i][1])

            if float(xyzData[i][2]) >= zMax:
                zMax = float(xyzData[i][2])
       

        # plot x-plane
        indexX1 = 0
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                
                pos[indexX1] = (x, y, 0)
                size[indexX1] = .5
                color[indexX1] = (0.0, 1.0, 0.0, 0.5)
                #print indexX1, pos[indexX1]
                indexX1 = indexX1 + 1
        
        indexX2 = indexX1
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                
                pos[indexX2] = (x, y, zMax)
                size[indexX2] = .5
                color[indexX2] = (0.0, 1.0, 0.0, 0.5)
                #print indexX2, pos[indexX2]
                indexX2 = indexX2 + 1
        

        # plot y-plane
        indexY1 = indexX2
        for y in range(0, int(yMax) + 1):
            for z in range(0, int(zMax) + 1):

                pos[indexY1] = (0, y, z)
                size[indexY1] = .5
                color[indexY1] = (0.0, 1.0, 0.0, 0.5)
                #print indexY1, pos[indexY1]
                indexY1 = indexY1 + 1

        indexY2 = indexY1
        for y in range(0, int(yMax) + 1):
            for z in range(0, int(zMax) + 1):

                pos[indexY2] = (xMax, y, z)
                size[indexY2] = .5
                color[indexY2] = (0.0, 1.0, 0.0, 0.5)
                #print indexY2, pos[indexY2]
                indexY2 = indexY2 + 1

        # plot z-plane
        indexZ1 = indexY2
        for z in range(0, int(zMax) + 1):
            for x in range(0, int(xMax) + 1):

                pos[indexZ1] = (x, 0, z)
                size[indexZ1] = .5
                color[indexZ1] = (0.0, 1.0, 0.0, 0.5)
                #print indexZ1, pos[indexZ1]
                indexZ1 = indexZ1 + 1


        indexZ2 = indexZ1
        for z in range(0, int(zMax) + 1):
            for x in range(0, int(xMax) + 1):

                pos[indexZ2] = (x, yMax, z)
                size[indexZ2] = .5
                color[indexZ2] = (0.0, 1.0, 0.0, 0.5)
                #print indexZ2, pos[indexZ2]
                indexZ2 = indexZ2 + 1

        print indexZ2


    
        print xMax, yMax, zMax
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                for z in range(0, int(zMax) + 1):
                    pos[x+y+z] = (x, y, z)
                    print pos[x+y+z]
                    size[x+y+z] = .5
                    color[x+y+z] = (0.0, 1.0, 0.0, 0.5)