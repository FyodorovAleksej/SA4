from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random as rdm

def equalList(list1, list2, accur):
    if (len(list1) != len(list2)):
        raise ArithmeticError("lens are not equals")
    for i in range(0, len(list1)):
        if not equalator(list1[i], list2[i], accur):
            return False
    return True

def divisionTurple(point, length):
    return (point[0]/length, point[1]/length, point[2]/length)

def accuracyEqual(value1, value2, accur):
    return abs(value1 - value2) < accur

def minIndex(collection):
    index = 0
    min = collection[0]
    for i in range(0, len(collection)):
        if (collection[i] < min):
            index = i
            min = collection[i]
    return index

def delta(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

def equalator(point1, point2, accur):
    return accuracyEqual(point1[0], point2[0], accur) and accuracyEqual(point1[1], point2[1], accur) and accuracyEqual(point1[2], point2[2], accur)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

points = []
N = 30
MIN = 0
MAX = 100
CLUSTERS = 3
ACCUR = 0.003
COLORS = ['r', 'b', 'y']
for i in range(0, N):
    points.append((rdm.randint(MIN, MAX), rdm.randint(MIN, MAX), rdm.randint(MIN, MAX)))
print(points)
clusterIndex = []
unicValues = []
for i in range(0, N):
    if points[i] not in unicValues:
        unicValues.append(points[i])
print(unicValues)
for i in range(0, CLUSTERS):
    index = rdm.randint(0, len(unicValues))
    while(index in clusterIndex or index >= len(unicValues)):
        index += 1
        if (index >= len(unicValues)):
            index = 0
    clusterIndex.append(index)
print(clusterIndex)
kClusters = [unicValues[i] for i in clusterIndex]
print(kClusters)

oldkClusters = kClusters.copy()
flag = True
clusterValues = [[] for i in range(0, CLUSTERS)]

while flag:

    for point in points:
        pointLength = []
        for cluster in kClusters:
            pointLength.append(delta(cluster, point))
        clusterValues[minIndex(pointLength)].append(point)

    for cindex in range(0 , CLUSTERS):
        pointSum = (0, 0, 0)
        for point in clusterValues[cindex]:
            pointSum = np.add(pointSum, point)
        kClusters[cindex] = divisionTurple(pointSum, len(clusterValues[cindex]))
    flag = not equalList(kClusters, oldkClusters, ACCUR)
    oldkClusters = kClusters.copy()
    print(kClusters)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

print("-------------------------------------------------")
print("Result K:")
print(kClusters)
for i in range(0, CLUSTERS):
    color = COLORS[i]
    print("\n\n---------------------------\n")
    print("Cluster #" + str(i) + ":")
    print("Center = " + str(kClusters[i]))
    print("Points:")
    ax.scatter(kClusters[i][0], kClusters[i][1], kClusters[i][2], c=COLORS[i], marker='D')
    for point in clusterValues[i]:
        print(point)
        ax.scatter(point[0], point[1], point[2], c=color, marker='.')

plt.savefig("result", fmt="png")
plt.show()