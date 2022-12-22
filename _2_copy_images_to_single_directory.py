


from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tqdm import tqdm
import multiprocessing as mp
import argparse
import shutil


def getImagesPaths(dataset_path: str)->list:
    '''
    returns a list with images paths from the given dataset
    args:
         dataset_path: path to dataset
    '''
    return list(filter(lambda path: Path.is_file(path), list(Path(dataset_path).rglob("./*[!.json]"))))


def copy_images(dataset_path: str, images_path: str):
    '''
    copies images to a single folder
    args:
         dataset_path: path to dataset
         images_path: path to where save the folder with images
    '''
    try:
        (Path(images_path).mkdir(parents=True, exist_ok=True))
    except OSError as error:
        pass

    image_files_paths = getImagesPaths(dataset_path)
    new_image_files_paths = [Path(images_path) / f"{path.name}" for path in image_files_paths]
    with ThreadPoolExecutor(100) as executor:
            executor.map(shutil.copy, image_files_paths, new_image_files_paths)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str)
    parser.add_argument("-d", "--dataset-path", type=str)
    parser.add_argument("-a", "--annotations-path", type=str)
    parser.add_argument("-y", "--yolo-path", type=str)
    args = parser.parse_args()
    copy_images(args.dataset_path, args.images_path)

if __name__ == "__main__":
    main()