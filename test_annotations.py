from matplotlib.font_manager import font_scalings
from IPython.display import Image  # for displaying images
import os 
import random
from PIL import Image, ImageDraw
import numpy as np
import json
import glob
from time import time_ns
from pathlib import Path
import argparse

random.seed(time_ns())
class_id_to_name_mapping = None

classIdMapper = {9993505:0,
                 9993514:1, 
                 9993506:2, 
                 9993507:3,
                 9993508:4,
                 9993509:5,
                 9993510:6,
                 9993511:7,
                 9993512:8,
                 9993513:9}
def create_class_id_to_name_mapping(dataset_path):
    class_id_to_name_mapping = {}
    with open(os.path.join(dataset_path, "meta.json")) as meta:
        meta_dict = json.loads(meta.read())
        for obj_class in meta_dict["classes"]:
            class_id = classIdMapper[obj_class["id"]]
            name = obj_class["title"]
            class_id_to_name_mapping[class_id] = name
    return class_id_to_name_mapping

def plot_bounding_box(image, annotation_list,class_id_to_name_mapping):
    annotations = np.array(annotation_list)
    w, h = image.size
    
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    
    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0), (x1,y1)))
        
        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))], font_scalings=10)

    image.save('example_bounding_box.png')


def plot_img_with_bb(annotation_path, images_path, class_id_to_name_mapping):
    annotation_list = None
    with open(annotation_path, "r") as file:
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.strip().split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x ] for x in annotation_list]

    #Get the corresponding image file
    ann_name_wo_extension= os.path.basename(annotation_path).split(".")[0]
    image_pattern = os.path.join(images_path, f"{ann_name_wo_extension}*")
    image_path = glob.glob(image_pattern)[0]
    assert os.path.exists(image_path)

    image = Image.open(image_path)

    plot_bounding_box(image, annotation_list, class_id_to_name_mapping)

def get_random_ann_path(annotations_path):
    annotation_paths = list(Path(annotations_path).rglob("*"))
    return random.choice(annotation_paths)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str)
    parser.add_argument("-d", "--dataset-path", type=str)
    parser.add_argument("-a", "--annotations-path", type=str)
    args = parser.parse_args()
    class_id_to_name_mapping = create_class_id_to_name_mapping(args.dataset_path)
    plot_img_with_bb(get_random_ann_path(args.annotations_path), args.images_path, class_id_to_name_mapping)

if __name__ == "__main__":
    main()