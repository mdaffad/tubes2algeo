import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
from pathlib import Path
import math

# Feature extractor
def extract_features(image_path, vector_size=32):
    image = imread(image_path, mode="RGB")
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print ("Error: "), e
        return None

    return dsc
def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print ('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    fp = open('pickled_db_path', 'wb')
    pickle.dump(result, fp)

class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path,'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)
    def euclidean_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        
        result = [0 for x in range(18)]
        for i in range(18):
            temp = [0 for x in range(2048)]
            for j in range (2048):
                temp[j] = pow((temp[j] - v[0][j]),2)
                print(temp[j], v[0][j])
                result[i] += temp[j]
            print(result[i])
            result[i] = pow(result[i], 0.5)
            
        return np.array(result) 

        
            
    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)
    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances_cos = self.cos_cdist(features)
        img_distances_euclidean = self.euclidean_cdist(features)
        
        
        for e in img_distances_cos:
            e = math.sin(e)

        print(img_distances_euclidean)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances_euclidean)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances_euclidean[nearest_ids].tolist()


def show_img(path):
    img = imread(path, mode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    current = os.getcwd()
    images_path = os.path.join(current,"resources/images")
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # getting 3 random images 
    sample = random.sample(files, 1)
    
    batch_extractor(images_path)

    ma = Matcher('features.pck')
        
    for s in sample:
        print ('Query image ==========================================')
        show_img(s)
        names, match = ma.match(s, topn=3)
        print ('Result images ========================================')
        for i in range(3):
            # we got cosine distance, less cosine distance between vectors
            # more they similar, thus we subtruct it from 1 to get match value
            print ('Match ' + str(match[i]))
            show_img(os.path.join(images_path, names[i]))
run()