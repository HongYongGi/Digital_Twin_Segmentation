"""
Log

* Written by HongYongGi  

"""

# Package
import os, glob, shutil
import nibabel as nib
import numpy as np
import pandas as pd
import pydicom
from tqdm import tqdm
import ipywidgets as widgets
from datetime import date
import SimpleITK as sitk
import dicom2nifti
import dicom2nifti.settings as settings
settings.disable_validate_slice_increment()


# Utils function
def load_data(path):
    file_name  = os.path.basename(path)
    if 'nii' in file_name:
        nii = nib.load(path)
        affine = nii.affine
        header = nii.header
        nii = nii.get_fdata()
        return nii, affine, header
    elif 'mha' in file_name:
        mha = sitk.ReadImage(path)
        mha = sitk.GetArrayFromImage(mha)
        return mha
    elif 'dcm' in file_name:
        dcm = pydicom.dcmread(path)
        return dcm
    elif 'raw' in file_name:
        raw = np.fromfile(path, dtype=np.uint16, sep="")
        return raw
    elif 'csv' in file_name:
        csv = pd.read_csv(path)
        return csv

    else:
        print('Not supported file format')
        return None

def convert_mha_nii(
    mha_file_path : str, 
    nii_file_path : str ):
    image = sitk.ReadImage(mha_file_path)
    sitk.WriteImage(image, nii_file_path, True)
    
def convert_nrrd_nii(
    nrrd_file_path: str,
    nii_file_path: str):    
    image = sitk.ReadImage(nrrd_file_path)
    sitk.WriteImage(image, nii_file_path, True)
    
def convert_dicom_nii(
    dicom_dir_path: str,
    nii_file_path: str):
    try:
        dicom2nifti.dicom_series_to_nifti(dicom_dir_path, './temp.nii', reorient_nifti=False)
        temp     = nib.load('./temp.nii')
        header   = temp.header
        affine   = temp.affine
        data     = temp.get_fdata()
        save_nii = nib.Nifti1Image(data, affine, header)
        nib.save(save_nii, nii_file_path)
        os.remove('./temp.nii')
    except:
        print("Can't convert dicom to nii")
        print(dicom_dir_path)
        
def makedir(path):
    try:
        os.makedirs(path)
    except:
        pass
    