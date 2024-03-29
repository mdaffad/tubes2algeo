import cv2
import numpy as np
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

        Construct = cv2.KAZE_create()

        KeyPoints = Construct.detect(image)

        KeyPoints = sorted(KeyPoints, key=lambda x: -x.response)[:vector_size]

        KeyPoints, Descript = Construct.compute(image, KeyPoints)

        Descript = Descript.flatten()

        needed_size = (vector_size * 64)
        if Descript.size < needed_size:

            Descript = np.concatenate([Descript, np.zeros(needed_size - Descript.size)])
    except cv2.error as e:
        print ("Error: "), e
        return None

    return Descript


# Ekstrak dari file database pickle
def BatchExtractor(images_path, pickled_db_path="features.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    
    for f in files:
        print ("Extracting features from image %s" %(f))
        name = f.split('/')[-1].lower()
        result[name] = ImageExtract(f)
        print(result[name])

    with open(pickled_db_path, 'wb') as pickledfile:
        pickle.dump(result, pickledfile)

# Kelas untuk memproses kemiripan gambar
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

    def cos_cdist(self, vector):
        countPic = self.names.size

        v = vector.reshape(1, -1)
        
        CosineData = []

        sumVectorV = 0    
        for j in range(2048) :
            sumVectorV += math.pow(v[0][j],2)
        sumVectorV = math.sqrt(sumVectorV)

        for i in range(countPic-1) :
            dotProduct = 0.0;
            for j in range(2048) :
                dotProduct += (self.matrix[i][j]*v[0][j])
            

            sumVectorW = 0;
            for j in range(2048) :
                sumVectorW += math.pow((self.matrix[i][j]),2)
            sumVectorW = math.sqrt(sumVectorW)

            
            result = dotProduct/(sumVectorV*sumVectorW)
            CosineData.append(1-result)  


        return np.array(CosineData)
    def EuclideanDistances(self, vector):
        countPic = self.names.size

        v = vector.reshape(1, -1)
      
        EuclideanData = []

        for i in range(countPic-1) :
            sumVector = 0;
            for j in range(2048) :
                sumVector += math.pow((self.matrix[i][j]-v[0][j]),2)
            EuclideanData.append(math.sqrt(sumVector))
        
        return np.array(EuclideanData)

    def match(self, image_path, topn, option):
        features = ImageExtract(image_path)

        if (option == True):
          img_distances = self.EuclideanDistances(features)
        elif (option == False):
          img_distances = self.cos_cdist(features)

        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


# Fungsi untuk run proses pencocokan gambar    
def run(option, address, top, images_path):
    
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    
    BatchExtractor(images_path)

    ma = Matcher('features.pck')

    names, match = ma.match(address, top, option)

    result = []
    
    for i in range(top):
        if(option):
            print ('Match %s' %(match[i]))
        else :
            print ('Match %s' %(1-match[i]))
        result.append(os.path.join(images_path, names[i]))
    print(result)
    return np.array(result)

    
