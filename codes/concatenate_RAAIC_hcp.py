#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 03:54:51 2022

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
from nibabel import cifti2

#hcp
beh_path = '/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/MAP_lone_covariates_scaled_nools.csv'
df = pd.read_csv(beh_path)

#concatenate the gbc file
sub1 = list(df["Subject"])[0]
final_img = nib.load(f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub1}/rsfMRI_FCmean.pscalar.nii')
final_array = final_img.get_fdata()
final_array = final_array[291,:]
final_array = final_array.reshape(1,final_array.shape[0])

for idx, sub in enumerate(list(df['Subject'])[1:]):
    img = nib.load(f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/{sub}/rsfMRI_FCmean.pscalar.nii')
    data = img.get_fdata()
    data = data[291,:]
    data = data.reshape(1,data.shape[0])
    final_array = np.concatenate((final_array,data),axis=0)
    print(f'{idx+2} is over.')
    
final_array = np.arctanh(final_array)
indexmap1 = final_img.header.get_index_map(1)
indexmap0 = cifti2.Cifti2MatrixIndicesMap([0], 'CIFTI_INDEX_TYPE_SCALARS')
map_names = [None] * final_array.shape[0]
label_tables = [None] * final_array.shape[0]
for mn, lbt in zip(map_names, label_tables):
    named_map = cifti2.Cifti2NamedMap(mn, label_table=lbt)
    indexmap0.append(named_map)
matrix = cifti2.Cifti2Matrix()
matrix.append(indexmap0)
matrix.append(indexmap1)
header = cifti2.Cifti2Header(matrix)
img = cifti2.Cifti2Image(final_array, header)
cifti2.save(img, f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/rsfMRI_RAAIC_FC_MAPnLONE_{idx+2}.pscalar.nii')

#only remain cerebrum
"""

c_path = '/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/palm/gbc_sub997_parcel.pscalar.nii'
c_model = nib.load(c_path)
c_indexmap1 = c_img.header.get_index_map(1)
"""
array_c = final_array[:,:360]
c_namedmap = indexmap1._maps[1:363]
c_indexmap1 = cifti2.Cifti2MatrixIndicesMap([1], 'CIFTI_INDEX_TYPE_PARCELS')
for nm in c_namedmap:
    c_indexmap1.append(nm)

c_matrix = cifti2.Cifti2Matrix()
c_matrix.append(indexmap0)
c_matrix.append(c_indexmap1)
c_header = cifti2.Cifti2Header(c_matrix)
c_img = cifti2.Cifti2Image(array_c,c_header)
cifti2.save(c_img,f'/nfs/z1/userhome/ZhangYaJie/Desktop/hcp_simplified/parcel_ts_fc_gbc/rsfMRI_RAAIC_FC_cerebrum_MAPnLONE_{idx+2}.pscalar.nii')
               

