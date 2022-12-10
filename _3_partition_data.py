import os
import shutil
from sklearn.model_selection import train_test_split
from pathlib import Path
import argparse


def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

def partition_data(yolo_path, images_path, annotations_path):

    images_paths = sorted([os.path.join(images_path, x) for x in os.listdir(images_path)])
    annotations_paths = sorted([ os.path.join(annotations_path, x) for x in os.listdir(annotations_path)])

    train_images, val_images, train_annotations, val_annotations = train_test_split(images_paths, annotations_paths, test_size=0.2, random_state=210)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size=0.5, random_state=420)

    # os.join.path(yolo_path, "images", "train").mkdir(parents=True)
    images_train_path = os.path.join(yolo_path, "images", "train")
    images_val_path =   os.path.join(yolo_path, "images", "val")  
    images_test_path =  os.path.join(yolo_path, "images", "test")
    labels_train_path = os.path.join(yolo_path, "images", "train")
    labels_val_path =   os.path.join(yolo_path, "images", "val")
    labels_test_path =  os.path.join(yolo_path, "images", "test")
    try:
        Path(images_train_path).mkdir(parents=True) 
        Path(images_val_path).mkdir(parents=True) 
        Path(images_test_path).mkdir(parents=True)
        Path(labels_train_path).mkdir(parents=True)
        Path(labels_val_path).mkdir(parents=True) 
        Path(labels_test_path).mkdir(parents=True)
    except OSError as error:
        print(error)


    move_files_to_folder(train_images, images_train_path)
    move_files_to_folder(val_images, images_val_path)
    move_files_to_folder(test_images, images_test_path)
    move_files_to_folder(train_annotations, labels_train_path)
    move_files_to_folder(val_annotations, labels_val_path)
    move_files_to_folder(test_annotations, labels_test_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str)
    parser.add_argument("-d", "--dataset-path", type=str)
    parser.add_argument("-a", "--annotations-path", type=str)
    parser.add_argument("-y", "--yolo-path", type=str)
    args = parser.parse_args()
    partition_data(args.yolo_path, args.images_path, args.annotations_path)

if __name__ == "__main__":
    main()