import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy
img = plt.imread('a.jpg')
width=img.shape[0]
height=img.shape[1]
print(img.shape)

img=img.reshape(width*height,3)
kmeans=KMeans(n_clusters=10).fit(img)
lables=kmeans.predict(img)
clusters=kmeans.cluster_centers_
img2=numpy.zeros_like(img)

for i in range(len(img)):
    img2[i] = clusters[lables[i]]
img2=img2.reshape(width,height,3)
plt.imshow(img2)
plt.show()







