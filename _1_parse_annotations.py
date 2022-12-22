from pathlib import Path
from tqdm import tqdm
import argparse
import json
import os


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

def getAnnotationsPaths(dataset_path: str) -> list:
    '''
    returns a list with annotations paths from the given dataset
        
    args:
         dataset_path: path to dataset
    '''
    return list(Path(dataset_path).rglob("./*/*.json")) 

def parseAnnotations(dataset_path: str, annotations_path: str):
    '''
    Makes a directory with transformed annotations

    args:
        dataset_path: path to dataset
        annotations_path: path to where save the folder with annotations
    '''
    try:
        Path(annotations_path).mkdir(parents=True)
    except OSError as error:
        pass
    annPaths = getAnnotationsPaths(dataset_path)
    for annPath in tqdm(annPaths):
        with open(annPath, "r", encoding="utf8") as annotation:
            formatedAnnotations = []
            annData = json.loads(annotation.read())
            imgHeight = annData["size"]["height"]
            imgWidth = annData["size"]["width"]
            for obj in annData["objects"]:
                classId = str(classIdMapper[int(obj["classId"])])
                points = obj["points"]["exterior"]
                p1 = points[1]
                p0 = points[0] 
                objWidth = p1[0] - p0[0]
                objHeight = p1[1] - p0[1]

                objCenterXNorm = (p0[0] + (objWidth/2) )/imgWidth
                objCenterYNorm = (p0[1] + (objHeight/2) )/imgHeight
                objWidthNorm = objWidth / imgWidth
                objHeightNorm = objHeight / imgHeight

                formatedAnnotations.append(" ".join([str(classId),
                                            str(objCenterXNorm),
                                            str(objCenterYNorm),
                                            str(objWidthNorm),
                                            str(objHeightNorm),
                                            "\n"]))

            filename = os.path.basename(annPath)
            filenameWithoutExtension = filename.split(".")[0]
            
            annotation_path = os.path.join(annotations_path,  f"{filenameWithoutExtension}.txt")
            with open(annotation_path, "w", encoding="utf8") as formatedAnnotationTxt:
                formatedAnnotationTxt.writelines(formatedAnnotations)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str)
    parser.add_argument("-d", "--dataset-path", type=str)
    parser.add_argument("-a", "--annotations-path", type=str)
    parser.add_argument("-y", "--yolo-path", type=str)
    args = parser.parse_args()
    parseAnnotations(args.dataset_path, args.annotations_path)

if __name__ == "__main__":
    main()