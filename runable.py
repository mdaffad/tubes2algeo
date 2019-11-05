import cv2
import numpy as np
import scipy
import scipy.spatial
import imageio
import pickle
import random
import os
import math
import matplotlib.pyplot as plt

# Feature extractor
def ImageExtract(image_path, vector_size=32):
    image = imageio.imread(image_path, pilmode="RGB")
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        Construct = cv2.KAZE_create()
        # Dinding image keypoints
        KeyPoints = Construct.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        KeyPoints = sorted(KeyPoints, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        KeyPoints, Descript = Construct.compute(image, KeyPoints)
        # Flatten all of them in one big vector - our feature vector
        Descript = Descript.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if Descript.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            Descript = np.concatenate([Descript, np.zeros(needed_size - Descript.size)])
    except cv2.error as e:
        print ("Error: "), e
        return None

    return Descript


def BatchExtractor(images_path, pickled_db_path="features.pck"):
    
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # files.sort(key=lambda f: int(filter(str.isdigit, f)))

    result = {}
    
    for f in files:
        print ("Extracting features from image %s" %(f))
        name = f.split('/')[-1].lower()
        result[name] = ImageExtract(f)
        print(result[name])
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as pickledfile:
        pickle.dump(result, pickledfile)

class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path,'rb') as pickledfile:
            self.data = pickle.load(pickledfile)
        self.names = []
        self.matrix = []
        countPic = 0
        for (k, v) in sorted(self.data.items()):
            self.names.append(k)
            self.matrix.append(v)
            countPic += 1
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    # def cos_cdist(self, vector):
    #     # getting cosine distance between search image and images database
    #     v = vector.reshape(1, -1)
    #     return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def cos_cdist(self, vector):
        countPic = self.names.size
        # print(countPic)

        v = vector.reshape(1, -1)
        print(v[0][0])
        # print(v[0])
        
        EuclideanData = []

        print(countPic)


        for i in range(countPic-1) :
            dotProduct = 0.0;
            for j in range(2048) :
                dotProduct += (self.matrix[i][j]*v[0][j])
            

            sumVectorW = 0;
            for j in range(2048) :
                sumVectorW += math.pow((self.matrix[i][j]),2)
            sumVectorW = math.sqrt(sumVectorW)
            sumVectorV
            for j in range(2048) :
                sumVectorV += math.pow(v[0][j],2)
            sumVectorV = math.sqrt(sumVectorV)

        return np.array(EuclideanData)
    def EuclideanDistances(self, vector):
        countPic = self.names.size
        # print(countPic)

        v = vector.reshape(1, -1)
        print(v[0][0])
        # print(v[0])
        
        EuclideanData = []

        print(countPic)


        for i in range(countPic-1) :
            sumVector = 0;
            for j in range(2048) :
                sumVector += math.pow((self.matrix[i][j]-v[0][j]),2)
            EuclideanData.append(math.sqrt(sumVector))
        return np.array(EuclideanData)

    def match(self, image_path, topn=5):
        features = ImageExtract(image_path)
        img_distances = self.EuclideanDistances(features)
        print(img_distances)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()

def show_img(path):
    img = imageio.imread(path, pilmode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    # images_path = input("Input Directory Files : ")

    images_path = '/home/aufa/Downloads/Try/'
    
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    
    searchingPic = '/home/aufa/Downloads/Try/2.jpg'
    # searchingPic = input("Input Directory Picture : ")
    
    BatchExtractor(images_path)

    ma = Matcher('features.pck')

    # EuclideanDistances('features.pck')
    
    print ('Query image ==========================================')
    show_img(searchingPic)
    names, match = ma.match(searchingPic, topn=3)
    print ('Result images ========================================')
    for i in range(3):
        # we got cosine distance, less cosine distance between vectors
        # more they similar, thus we subtruct it from 1 to get match value
        print ('Match %s' %(match[i]))
        show_img(os.path.join(images_path, names[i]))
run()