#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:zhangyajie
target: generate parcellated GBC file from time series file
outline:
    1. parcellate time series file per run per subject
    2. generate FC file per run per subject
    3. generate averaged FC per subject
    4. generate GBC per subject
    
input file:
hcp:
    /nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/HCPYA_rfMRI_file_check.tsv
    /nfs/m1/hcp/100206/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii
    
hcpd:
    '/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/rsfMRI_check.csv'
    dtseries: '/nfs/e1/HCPD/fmriresults01/HCD0008117_V1_MR/MNINonLinear/Results/rfMRI_REST/rfMRI_REST_Atlas_MSMAll_hp0_clean.dtseries.nii'

output file:
     f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/{run}_Atlas_MSMAll_hp0_clean.ptseries.nii'
     f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/{run}_rsfMRI_FC.pscalar.nii'
     f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/rsfMRI_FCmean.pscalar.nii'
     f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/rsfMRI_GBC.pscalar.nii'
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
from nibabel import cifti2

#get subject ID list
file = '/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/HCPYA_rfMRI_file_check.tsv'
subid = pd.read_csv(file, usecols=['subID'],sep='\t')
#get parcel-wise template
parcel_map = nib.load('/nfs/z1/userhome/ZhangYaJie/Desktop/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR.pscalar.nii')
indexmap1 = parcel_map.header.get_index_map(1)
#get voxel-wise template
parcelindex_img = nib.load('/nfs/z1/userhome/ZhangYaJie/Desktop/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR.dscalar.nii')
parcelindex_data = parcelindex_img.get_fdata()
#match two template and get voxel indexes in each parcel
map_list = list(parcelindex_data.flatten())
map_set = list(set(map_list))
map_dict = dict()
for roi in map_set:
    map_dict[roi] = [ind for ind, x in enumerate(map_list) if x==roi]
##calculation
runs = ['rfMRI_REST1_LR','rfMRI_REST1_RL','rfMRI_REST2_LR','rfMRI_REST2_RL']
for idx, sub in enumerate(list(subid['subID'])[789:]):
    for run in runs:
        try: 
            ##parcellate time series file per run per subject
            sub_path = f'/nfs/m1/hcp/{sub}/MNINonLinear/Results/{run}/{run}_Atlas_MSMAll_hp2000_clean.dtseries.nii'
            file = os.path.exists(sub_path)
            if file:
                img = nib.load(sub_path)
                data = img.get_fdata()
                indexmap0 = img.header.get_index_map(0)
                ptseries = np.zeros((data.shape[0],len(map_set)))
                for ind, roi in enumerate(map_set):
                    ptseries[:,ind] = np.mean(data[:,map_dict[roi]],axis=1)
                pt_matrix = cifti2.Cifti2Matrix()
                pt_matrix.append(indexmap0)
                pt_matrix.append(indexmap1)
                pt_header = cifti2.Cifti2Header(pt_matrix)
                pt_img = cifti2.Cifti2Image(ptseries, pt_header)
                cifti2.save(pt_img, f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/{run}_Atlas_MSMAll_hp0_clean.ptseries.nii')
                print(f"sub {idx+789}'s {run}'s tseries is over.")
                ##generate FC file per run per subject
                fc = np.corrcoef(ptseries, rowvar=False)
                for i in range(len(fc)):
                    fc[i,i] = 0
                fc_indexmap0 = cifti2.Cifti2MatrixIndicesMap([0], 'CIFTI_INDEX_TYPE_SCALARS')
                map_names = [None] * fc.shape[0]
                label_tables = [None] * fc.shape[0]
                for mn, lbt in zip(map_names, label_tables):
                    named_map = cifti2.Cifti2NamedMap(mn, label_table=lbt)
                    fc_indexmap0.append(named_map)
                fc_matrix = cifti2.Cifti2Matrix()
                fc_matrix.append(fc_indexmap0)
                fc_matrix.append(indexmap1)
                fc_header = cifti2.Cifti2Header(fc_matrix)
                fc_img = cifti2.Cifti2Image(fc, fc_header)
                cifti2.save(fc_img,f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/{run}_rsfMRI_FC.pscalar.nii')
                print(f"sub {idx+789}'s {run}'s fc is over.")
            elif not file:
                pass
        except OSError:
            pass
        continue
    
    sub_dir = f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/'
    file_l = os.listdir(sub_dir)
    fc_l = list()
    ##generate averaged FC per subject
    for i in file_l:
        if 'FC' in os.path.splitext(i)[0]:
            fc_l.append(i)
    if fc_l != []:
        fc_img = nib.load(sub_dir + fc_l[0])
        fc_data = fc_img.get_fdata()
        fc_data = fc_data.reshape(fc_data.shape[0],fc_data.shape[1],1)
        for fc_file in fc_l[1:]:
            fc_img2 = nib.load(sub_dir + fc_file)
            fc_data2 = fc_img2.get_fdata()
            fc_data2 = fc_data2.reshape(fc_data2.shape[0],fc_data2.shape[1],1)
            fc_data = np.concatenate((fc_data,fc_data2),axis=2)
        #fisher z transformation
        fc_data = np.arctanh(fc_data)
        fc_mean = np.mean(fc_data, axis=2)
        fc_mean = fc_mean.reshape(fc_data.shape[0],fc_data.shape[1])
        fc_mean = np.tanh(fc_mean)
        fc_mean_img = cifti2.Cifti2Image(fc_mean, fc_header)
        cifti2.save(fc_mean_img,f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/rsfMRI_FCmean.pscalar.nii')
        print(f"sub {idx+789}'s mean fc is over.")
        ##generate GBC per subject
        fc_mean = np.arctanh(fc_mean)
        gbc = np.mean(fc_mean, axis=1)
        gbc = np.tanh(gbc)
        gbc = gbc.reshape(1,len(gbc))
        gbc_indexmap0 = cifti2.Cifti2MatrixIndicesMap([0], 'CIFTI_INDEX_TYPE_SCALARS')
        map_names = [None] * gbc.shape[0]
        label_tables = [None] * gbc.shape[0]
        for mn, lbt in zip(map_names, label_tables):
            named_map = cifti2.Cifti2NamedMap(mn, label_table=lbt)
            gbc_indexmap0.append(named_map)
        gbc_matrix = cifti2.Cifti2Matrix()
        gbc_matrix.append(gbc_indexmap0)
        gbc_matrix.append(indexmap1)
        gbc_header = cifti2.Cifti2Header(gbc_matrix)
        gbc_img = cifti2.Cifti2Image(gbc, gbc_header)
        cifti2.save(gbc_img, f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/rsfMRI_GBC.pscalar.nii')
        print(f'sub {idx+789} gbc is over.')
    elif fc_l == []:
        print(f"sub {idx+789} doesn't have rsfMRI files.")
        pass
        
                












