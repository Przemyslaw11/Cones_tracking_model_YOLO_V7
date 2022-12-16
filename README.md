# Cones_tracking_model
Model was made as an exercise in the science club : AGH_RACING

# Model's basic documentation:
 - Dataset consists of [?]GB photos of cones in Supervisely format. Training set consists [?]% of all photos and testing set consists [?]% of all photos.
 
  ## Model properties:
  in progress:)
  
  ## Configuration:
  
 # ⚫STEP 1 
  - Clone YOLOv7
  
        $ git clone https://github.com/WongKinYiu/yolov7
        $ cd yolov7
        $ pip install -qr requirements.txt
        
# ⚪STEP 2
  
  - Move file: 'cones.yaml' to yolov7\data
  - Prepare your dataset. Data is in the Supervisely format originally, but yolov7 requires YOLOv7 PyTorch TXT format.
    
    You can AUTOMATICALLY preprocess data using execute_all.py script in the Repo:
    
        python execute_all.py -d {path_to_your_dataset} -y {path_to_your_yolo_folder} -i {path_to_your_images_folder} -a {path_to_your_annotations_folder}
     
     or by using the scripts separately:
     
        python3 _1_parse_annotations.py -i {path_to_your_images_folder} -d {path_to_your_dataset} -a {path_to_your_annotations_folder} -y {path_to_your_yolo_folder}
        python3 _2_copy_images_to_single_directory.py -i {path_to_your_images_folder} -d {path_to_your_dataset} -a {path_to_your_annotations_folder} -y {path_to_your_yolo_folder}
        python3 _3_partition_data.py -i {path_to_your_images_folder} -d {path_to_your_dataset} -a {path_to_your_annotations_folder} -y {path_to_your_yolo_folder}
 #
 
        The final sample result in your YOLOv7 folder should look like this:
        
              yolov7
              |
              ├───images
              |   ├── test
              |   |   └─────────  amz_00000.jpg
              |   |               amz_00000.txt
              |   |               amz_00003.jpg
              |   |               amz_00003.txt
              |   |               amz_00006.jpg
              |   |               amz_00006.txt
              |   |               amz_00011.jpg
              |   |               amz_00011.txt
              |   |               amz_00013.jpg
              |   |               amz_00013.txt
              |   ├── train
              |   |   └─────────  amz_00001.jpg
              |   |               amz_00001.txt
              |   |               amz_00002.jpg
              |   |               amz_00002.txt
              |   |               amz_00004.jpg
              |   |               amz_00004.txt
              |   |               amz_00005.jpg
              |   |               amz_00005.txt
              |   |               amz_00007.jpg
              |   |               amz_00007.txt
              |   |     
              |   |     
              |   └── val
              |       └─────────  amz_00022.jpg
              |                   amz_00022.txt
              |                   amz_00033.jpg
              |                   amz_00033.txt
              |                   amz_00051.jpg
              |                   amz_00051.txt
              |                   amz_00063.jpg
              |                   amz_00063.txt
              |                   amz_00069.jpg
              |                   amz_00069.txt
              |   
              └── data
                  └─── cones.yaml 
                  
                 
# ⚫STEP 3
Run 'train_command.txt' on your automatically moved and preprocessed dataset or use one of the following commands:

      ⚪ CPU training
      $ python train.py --img 640 --cfg cfg/training/yolov7-tiny.yaml  --batch-size 1 --epochs 10 --data cones.yaml --weights '' --workers 1 --device cpu --name cones


      ⚫ Single GPU training

        train p5 models
      $ python train.py --workers 8 --device 0 --batch-size 32 --data cones.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights '' --name yolov7 --hyp data/hyp.scratch.p5.yaml

        train p6 models
      $ python train_aux.py --workers 8 --device 0 --batch-size 16 --data cones.yaml --img 1280 1280 --cfg cfg/training/yolov7-w6.yaml --weights '' --name yolov7-w6 --hyp data/hyp.scratch.p6.yaml


      ⚪ Multiple GPU training

        train p5 models
      $ python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train.py --workers 8 --device 0,1,2,3 --sync-bn --batch-size 128 --data cones.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights '' --name yolov7 --hyp data/hyp.scratch.p5.yaml

        train p6 models
      $ python -m torch.distributed.launch --nproc_per_node 8 --master_port 9527 train_aux.py --workers 8 --device 0,1,2,3,4,5,6,7 --sync-bn --batch-size 128 --data cones.yaml --img 1280 1280 --cfg cfg/training/yolov7-w6.yaml --weights '' --name yolov7-w6 --hyp data/hyp.scratch.p6.yaml


 ## Dataset is available under the following link:
 - https://www.fsoco-dataset.com/download

   
