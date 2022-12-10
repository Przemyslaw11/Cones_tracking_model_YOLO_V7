import argparse
# from ._1_parse_annotations import main as m1
# from ._2_copy_images_to_single_directory import main as m2
# from ._3_partition_data import main as m3
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str)
    parser.add_argument("-d", "--dataset-path", type=str)
    parser.add_argument("-a", "--annotations-path", type=str)
    parser.add_argument("-y", "--yolo-path", type=str)
    args = parser.parse_args()
    os.system(f"python3 _1_parse_annotations.py -i {args.images_path} -d {args.dataset_path} -a {args.annotations_path} -y {args.yolo_path}")
    os.system(f"python3 _2_copy_images_to_single_directory.py -i {args.images_path} -d {args.dataset_path} -a {args.annotations_path} -y {args.yolo_path}")
    os.system(f"python3 _3_partition_data.py -i {args.images_path} -d {args.dataset_path} -a {args.annotations_path} -y {args.yolo_path}")

if __name__ == "__main__":
    main()
