from PIL import Image
import random
import numpy
import math
import operator

#load data
image=Image.open('D:\\Courses\\SPRING19\\MachineLearning\\HW3\\color.JPG','r')
width, height=image.size
imagePixels=list(image.getdata())
data=bytes("",'utf-8')

K=3
initialCenters=set()
#choose K random centers
for x in range(K):
    center=random.randint(1,len(imagePixels))
    initialCenters.add(imagePixels[center])

oldCenters=set()
newCenters=initialCenters

while oldCenters != newCenters:
    oldCenters = newCenters
    clusterDict = dict([(key, []) for key in newCenters])
    for eachPixelTupleIndex in range(len(imagePixels)):
        print('Running K means ...',eachPixelTupleIndex)
        distanceDict={}
        for eachCenter in clusterDict:
            pixelValues=imagePixels[eachPixelTupleIndex]
            distanceList= numpy.subtract(pixelValues,eachCenter)
            distance=0
            for eachNumber in distanceList:
                distance+=eachNumber**2
            distance= math.sqrt(distance)
            distanceDict[eachCenter]=distance        
        bestCenter=min(distanceDict.items(), key=operator.itemgetter(1))[0]
        clusterDict[bestCenter].append(eachPixelTupleIndex)

    newCenters=set()
    for key,value in clusterDict.items():
        temp_center=(0,0,0)
        for eachValue in value:
            temp_center=tuple(map(operator.add, temp_center, imagePixels[eachValue]))

        totalSum=tuple(map(operator.add, key, temp_center))        
        pixelRed,pixelGreen,pixelBlue=totalSum[0],totalSum[1],totalSum[2]
        totalPixelsInCluster=len(clusterDict[key])        
        newCenterForEachCluster= (int(pixelRed/totalPixelsInCluster),int(pixelGreen/totalPixelsInCluster),int(pixelBlue/totalPixelsInCluster))  
        newCenters.add(newCenterForEachCluster)

# https://stackoverflow.com/questions/27445694/creating-image-through-input-pixel-values-with-the-python-imaging-library-pil
newIm = Image.new("RGB", (width, height))
pix = newIm.load()
for i in range(height):
    for j in range(width):
        print('Reconstructing Image',i)
        for center in clusterDict:
            if ((i - 1) * width + j) in clusterDict[center]:
                pix[j,i] = center
newIm.save("D:\\Courses\\SPRING19\\MachineLearning\\HW3\\newColor.png", "PNG")

