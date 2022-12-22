from sklearn.model_selection import train_test_split
from pathlib import Path
import argparse
import shutil
import os



def move_files_to_folder(list_of_files: list, destination_folder: str):
    '''
    moves files to the single destination folder
        
    args:
         list_of_files: list with the files which have to be moved
         destination_folder: path to where move the files from the given list
    '''     
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except Exception as err:
            print(f"{f} can't be moved due to {err}")

def partition_data(yolo_path: str, images_path: str, annotations_path: str):
    '''
    splits annotations and corresponing to them images into a training, testing and validation set.
    Folders are automatically made in yolo folder, to be ready to use them as fast as possible.

    args:
        yolo_path: path to yolo folder
        images_path: path to where take the images from
        annotations_path: path to where take the annotations from
    '''

    images_paths = sorted([Path(images_path) / x for x in os.listdir(images_path)])
    annotations_paths = sorted([Path(annotations_path) / x for x in os.listdir(annotations_path)])

    train_images, val_images, train_annotations, val_annotations = train_test_split(images_paths, annotations_paths, test_size=0.2, random_state=210)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size=0.5, random_state=420)

    images_train_path = Path(yolo_path) / "images"/ "train"
    images_val_path =   Path(yolo_path) / "images" / "val"
    images_test_path =  Path(yolo_path) / "images" / "test"
    labels_train_path = Path(yolo_path) / "images" / "train"
    labels_val_path =   Path(yolo_path) / "images" / "val"
    labels_test_path =  Path(yolo_path) / "images" / "test"
    try:
        Path(images_train_path).mkdir(parents=True, exist_ok=True) 
        Path(images_val_path).mkdir(parents=True, exist_ok=True) 
        Path(images_test_path).mkdir(parents=True, exist_ok=True)
        Path(labels_train_path).mkdir(parents=True, exist_ok=True)
        Path(labels_val_path).mkdir(parents=True, exist_ok=True) 
        Path(labels_test_path).mkdir(parents=True, exist_ok=True)

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
