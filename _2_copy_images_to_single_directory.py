import shutil
import os
from pathlib import Path
import argparse
from tqdm import tqdm
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

def getImagesPaths(dataset_path):
    return filter(lambda path: os.path.isfile(path), list(Path(dataset_path).rglob("./*[!.json]")))


def copy_images(dataset_path, images_path):
    try:
        (os.mkdir(images_path))
    except OSError as error:
        pass

    images_paths = getImagesPaths(dataset_path)
    with ThreadPoolExecutor(100) as exe:
        for path in tqdm(images_paths):
            filename = os.path.basename(path)
            new_path = os.path.join(images_path, f"{filename}")
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