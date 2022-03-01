# OverlapTransformer

The code for our paper submitted to IROS 2022:  

**OverlapTransformer: An Efficient and Rotation-Invariant Transformer Network for LiDAR-Based Place Recognition.**  

OverlapTransformer is a novel lightweight neural network exploiting the range image representation of LiDAR sensors to achieve fast execution with less than 4 ms per frame.  

<img src="https://github.com/haomo-ai/OverlapTransformer/blob/master/query_database.gif" >  

Fig. 1 An animation for finding the top1 candidate with **OverlapTransformer** on sequence 1-1 (database) and 1-3 (query) of **Haomo dataset**.

<img src="https://github.com/haomo-ai/OverlapTransformer/blob/master/haomo_dataset.png" >  

Fig. 2 **Haomo dataset** which is collected by **HAOMO.AI** will be released soon. 


## Dependencies

We are using pytorch-gpu for neural networks.

A nvidia GPU is needed for faster retrival.
OverlapTransformer (OT) is also fast enough when using the neural network on CPU.

To use a GPU, first you need to install the nvidia driver and CUDA.

- CUDA Installation guide: [link](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

- System dependencies:

  ```bash
  sudo apt-get update 
  sudo apt-get install -y python3-pip python3-tk
  sudo -H pip3 install --upgrade pip
  ```

- Python dependencies (may also work with different versions than mentioned in the requirements file)

  ```bash
  sudo -H pip3 install -r requirements.txt
  ```
  
## How to use
We currently only provide the training and test tutorials for KITTI sequences in this repository. The tutorials for Haomo dataset will be open-source once Haomo dataset is released.  

For a quick test of the training and testing procedures, you could use our [pretrained model]().  

### Data structure

We will recommend you follow our data structure.

#### OT structure


```bash
├── more_chosen_normalized_data_1208_1_01.npy
├── config
│   ├── config_haomo.yml
│   └── config.yml
├── modules
│   ├── loss.py
│   ├── netvlad.py
│   ├── overlap_transformer_haomo.py
│   └── overlap_transformer.py
├── test
│   ├── gt_0.3overlap_1.2tau_bet_two_traj.npy
│   ├── test_haomo_topn_prepare.py
│   ├── test_haomo_topn.py
│   ├── test_kitti00_PR_prepare.py
│   ├── test_kitti00_PR.py
│   ├── test_results_haomo
│   │   ├── predicted_des_L2_dis_bet_traj_forward.npz
│   │   └── recall_list.npy
│   └── test_results_kitti
│       └── predicted_des_L2_dis.npz
├── tools
│   ├── read_all_sets.py
│   ├── read_samples_haomo.py
│   ├── read_samples.py
│   └── utils
│       ├── gen_curv_data.py
│       ├── gen_depth_data.py
│       ├── gen_intensity_data.py
│       ├── gen_normal_data.py
│       ├── gen_semantic_data.py
│       ├── __init__.py
│       ├── normalize_data.py
│       ├── split_train_val.py
│       └── utils.py
├── train
│   ├── training_overlap_transformer_haomo.py
│   └── training_overlap_transformer_kitti.py
├── valid
│   └── valid_seq.py
├── visualize
│   ├── des_list.npy
│   └── viz_haomo.py
└── weights
    ├── pretrained_overlap_transformer_haomo.pth.tar
    └── pretrained_overlap_transformer.pth.tar
```
#### Dataset structure
In the file [config.yaml](https://github.com/haomo-ai/OverlapTransformer/blob/master/config/config.yml), the parameters of _data_root_ are described as follows:






  
  
  
