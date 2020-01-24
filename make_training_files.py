 #CREATES ANNOTATION FILE: one line per annotation

import pathlib
import argparse
import xml.etree.ElementTree as ET
from os import getcwd

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default="", help='dataset folder')
parser.add_argument('--classes', type=str, default="", help='dataset folder')
args = parser.parse_args()


coco_classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
metal_classes = ["bolt", "nail", "nut", "screw", "spring"]
chem_classes = ["acetone", "beaker", "blender", "draino", "hydrogen_peroxide", "sulfuric_acid"]
house_classes = ["door_handle"]
pipe_classes = ["steel", "pvc"]
weapon_classes = ["bullet", "knife", "container", "gun", "screwdriver"]



dataset_folder = args.dataset
annotation_folder = dataset_folder + "/Annotations"
image_folder = dataset_folder + "/JPEGImages/"

# define the path
currentDirectory = pathlib.Path(image_folder)
print("current dir: ", currentDirectory)

# define the pattern
currentPattern = "*.jpg"

import os
relevant_path = image_folder
included_extensions = ['jpg','jpeg', 'png', 'JPG', 'PNG', 'JPEG']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]

image_names_file = open(dataset_folder+'/image_names.txt', 'w')

for currentFile in file_names:
    f = pathlib.PosixPath(currentFile)
    print(f.stem)
    image_names_file.write(currentFile+"\n")

image_names_file.close()

if (args.classes == "coco"):
    classes = coco_classes
elif (args.classes == "metal"):
    classes = metal_classes
elif (args.classes == "chemical"):
    classes = chem_classes
elif (args.classes == "weapon"):
    classes = weapon_classes
elif (args.classes == "pipe"):
    classes = pipe_classes
elif (args.classes == "house"):
    classes = house_classes

def convert_annotation(image_id, annotations_file):
    ff = pathlib.PosixPath(image_id).stem
    in_file = open(annotation_folder+"/"+ff+'.xml')
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        # relative path
        annotations_file.write(image_folder+image_id+',')
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text))
        annotations_file.write(" " + ",".join([str(a) for a in b]) + ',' + classes[cls_id]+'\n')


image_ids = open(dataset_folder+'/image_names.txt').read().strip().split()
annotations_file = open(dataset_folder+'/annotations.txt', 'w')
for image_id in image_ids:
    convert_annotation(image_id, annotations_file)
    #list_file.write('\n')
annotations_file.close()


# Running directly from the repository:
# keras_retinanet/bin/train.py pascal /path/to/VOCdevkit/VOC2007
