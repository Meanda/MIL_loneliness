#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 02:46:39 2021
generate dscalar.nii files with the 4th dimension as subject (GBC,falff)
input file:
    hcp-brain:/nfs/m1/hcp/falff.dscalar.nii
    hcp-subject-function: /nfs/m1/hcp/100206/MNINonLinear/Results/falff.dscalar.nii(rsfc_ColeParcel2Vertex.dscalar.nii)
    hcp
    hcpd-all: /nfs/e1/HCPD/fmriresults01/falff.dscalar.nii
    hcpd-cerebellum: 
    hcpd-beh: '/nfs/z1/userhome/ZhangYaJie/Desktop/hcpd_simplified/norepeat_fulladj_simplified.csv'
    hcp-beh: /nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/social_fulladj.csv
    hcp-mricheck: /nfs/m1/hcp/HCPYA_rfMRI_file_check.tsv'
    ROI:/nfs/z1/userhome/ZhangYaJie/Desktop/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii 
output file:
    /nfs/z1/userhome/ZhangYaJie/Desktop/{dataset}_simplified/{brain_type}_sub{len(mri_check)}.dscalar.nii
    /nfs/z1/userhome/ZhangYaJie/Desktop/{dataset}_simplified/{brain_type}_sub{len(mri_check)}.dscalar.nii
@author: ZhangYaJie
"""

import sys
sys.path.append('/nfs/z1/userhome/ZhangYaJie/codes')

import nibabel as nib
import pandas as pd
import numpy as np
import scipy.stats as st
from ioTools import CiftiReader as CR
from ioTools import save2cifti
import glob
import os

"""
"""
#generate a nii file or dscalar nii file with all subjects' GBC data
brain_type = 'rsfc_ColeParcel2Vertex'
dataset = 'hcp'
#get the subjects' index list
mri_check = pd.read_csv('/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/social_nomiss.csv')
mri_check = mri_check.dropna(how='any')
sub_idx = list(mri_check.index.values)
subid = list(mri_check['Subject'])
#get the initiative GBC array
final_img = CR(f'/nfs/m1/hcp/{subid[0]}/MNINonLinear/Results/{brain_type}.dscalar.nii')
final_array = final_img.get_data()
# calculate the mean value of FC as GBC
final_array = np.mean(final_array,axis=0)
final_array = final_array.reshape(1,len(final_array))
for idx, sub in enumerate(subid[1:]):
    mean_list = list()
    img = CR(f'/nfs/m1/hcp/{sub}/MNINonLinear/Results/{brain_type}.dscalar.nii')
    data = img.get_data()
    data = np.mean(data,axis=0)
    data = data.reshape(1,len(data))
    final_array = np.concatenate((final_array,data),axis=0)
    print(f'{idx+2} subjects are over.' )
#fisher z transformation
final_array = np.arctanh(final_array)
#normalization
from sklearn import preprocessing
scaler = preprocessing.StandardScaler()
final_array = scaler.fit_transform(final_array)

structures = final_img.brain_structures
roi = structures[0:2]
model = final_img.brain_models(roi)
index_count = model[0].index_count + model[1].index_count
final_array = final_array[:,0:index_count]
save2cifti(f'/nfs/z1/userhome/ZhangYaJie/Desktop/{dataset}_simplified/{brain_type}_sub{len(mri_check)}.dscalar.nii',final_array,model)

#falff
brain_type = 'falff'
dataset = 'hcp'
mri_check = pd.read_csv('/nfs/m1/hcp/HCPYA_rfMRI_file_check.tsv', sep='\t')
mri_check = mri_check.dropna(how='any')
sub_idx = list(mri_check.index.values)

falff_img = CR('/nfs/m1/hcp/falff.dscalar.nii')
falff_data = falff_img.get_data()
falff_data = falff_data[sub_idx,:]
structures = falff_img.brain_structures
roi = structures[0:2]
model = falff_img.brain_models(roi)
index_count = model[0].index_count + model[1].index_count
falff_data = falff_data[:,0:index_count]
save2cifti(f'/nfs/z1/userhome/ZhangYaJie/Desktop/{dataset}_simplified/{brain_type}_sub{len(mri_check)}.dscalar.nii',falff_data,model)


