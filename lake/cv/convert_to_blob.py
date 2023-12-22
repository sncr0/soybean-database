import numpy as np
import os
import cv2
import glob
import csv

## ==================================================================================================
# Convert to object which can be stored as BLOB
## ==================================================================================================
labels = ["broadleaf", "grass", "soil", "soybean"]
blob_file_name = "./blob_final.csv"

# Load the dataset and preprocess the images
X = []
Y = []
image_size = (224, 224)  # Adjust to match VGG16 input size

for label in labels:
    dataset_path = "/home/samuel/NYU/DBS/proj/lake/cv/dataset/" + label + "/"
    print(dataset_path)
    file_paths = glob.glob(dataset_path + "*")
    counter = 0
    for file_path in file_paths:
        image = cv2.imread(file_path)
        img = cv2.resize(image, image_size)
        img_flattened = img.flatten()
        counter = counter + 1
        if counter%1 == 0:
            X.append(img)
            Y.append(label)

# Convert labels to numerical values
label_to_index = {label: index for index, label in enumerate(labels)}
Y = [label_to_index[label] for label in Y]

X_flattened = []

for row in X:
    X_flattened.append(row.flatten())

# Convert lists to NumPy arrays
X_flattened = np.array(X_flattened)
Y = np.array(Y)

data_to_save = []
for (feature, label) in zip(X_flattened, Y):
    pair = np.insert(feature, 0, label)
    data_to_save.append(pair)

data_to_save = np.array(data_to_save)
np.savetxt(blob_file_name, data_to_save, fmt= '%d', delimiter=" ")

## ==================================================================================================
# Reload the data
## ==================================================================================================
reloaded_data = np.loadtxt(blob_file_name, delimiter=' ', dtype = "uint8")
reloaded_X = []
reloaded_Y = []

for row in reloaded_data:
    reloaded_Y.append(row[0])
    
    reloaded_X.append(row[1::].reshape(img.shape))
assert(np.array_equal(np.array(X), reloaded_X))


