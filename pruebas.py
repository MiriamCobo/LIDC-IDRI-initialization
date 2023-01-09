import sys
import os
from pathlib import Path
import glob
from configparser import ConfigParser
import pandas as pd
import numpy as np
import warnings
import pylidc as pl
from tqdm import tqdm
from statistics import median_high

from utils import is_dir_path,segment_lung
from pylidc.utils import consensus
from PIL import Image

warnings.filterwarnings(action='ignore')

# Read the configuration file generated from config_file_create.py
parser = ConfigParser()
parser.read('lung.conf')

#Get Directory setting
DICOM_DIR = is_dir_path(parser.get('prepare_dataset','LIDC_DICOM_PATH'))
MASK_DIR = is_dir_path(parser.get('prepare_dataset','MASK_PATH'))
IMAGE_DIR = is_dir_path(parser.get('prepare_dataset','IMAGE_PATH'))
CLEAN_DIR_IMAGE = is_dir_path(parser.get('prepare_dataset','CLEAN_PATH_IMAGE'))
CLEAN_DIR_MASK = is_dir_path(parser.get('prepare_dataset','CLEAN_PATH_MASK'))
META_DIR = is_dir_path(parser.get('prepare_dataset','META_PATH'))

if __name__ == '__main__':
    LIDC_IDRI_list= [f for f in os.listdir(DICOM_DIR) if not f.startswith('.')]
    LIDC_IDRI_list.sort()
    for patient in tqdm(LIDC_IDRI_list):
        pid = patient #LIDC-IDRI-0001~
        scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).first()
        nodules_annotation = scan.cluster_annotations()
        scan.visualize(annotation_groups=nodules_annotation)
        vol = scan.to_volume()
        print("Patient ID: {} Dicom Shape: {} Number of Annotated Nodules: {}".format(pid,
            vol.shape,len(nodules_annotation)))
        patient_image_dir = IMAGE_DIR+"/"+pid
        patient_mask_dir = MASK_DIR+"/"+pid