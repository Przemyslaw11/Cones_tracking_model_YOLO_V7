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
    return filter(lambda path: Path.is_file(path), list(Path(dataset_path).rglob("./*[!.json]")))


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

    images_paths = getImagesPaths(dataset_path)
    with ThreadPoolExecutor(100) as exe:
        for path in tqdm(images_paths):
            filename = path.name
            new_path = Path(images_path) / f"{filename}"
            exe.submit(shutil.copy, path, new_path) 

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