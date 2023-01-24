# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 20:52:23 2022
target: 1. get GBC value and FC value of those significant ROIs.
    2. correct the roi label of GBC's multiple comparison correction (MCC) file
        (it's not labelled as ROI's name, but ROI-ROI)
outline:
    1. get the right label (label map & label list)
    2. get significant GBC or FC according to the MCC file
    3. get raw value of those significant GBC or FC
    4. merge raw value into table including behavioral data
    5. correct the roi label of GBC's multiple comparison correction file
input file: 
    label:'D:/hcp/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR_LabelKey.txt'
    MCC:'D:/hcp/MAPnLone/cerebrum_gbc/results_dat_tstat_fwep_c2.pscalar.nii'
        'D:/hcp/MAPnLone/cerebrum_RAAIC_FC/results_dat_tstat_cfwep_c2.pscalar.nii'
    raw data: 
        'D:/hcp/rsfMRI_GBC_cerebrum_MAPnLONE_970.pscalar.nii'
        'D:/hcp/MAPnLone/cerebrum_RAAIC_FC/rsfMRI_RAAIC_FC_cerebrum_MAPnLONE_970.pscalar.nii'
    behavioral: 
        'D:/hcp/MAP_lone_covariates_scaled_nools.csv'
output file:
    'D:/hcp/MAPnLone/MAP_lone_beh_brain.csv'
    'D:/hcp/MAPnLone/cerebrum_gbc/relabelled_results_dat_tstat_fwep_c2.pscalar.nii'
@author: zhang
"""
import sys
sys.path.append('C:/Users/zhang/OneDrive/工作笔记/代码/预处理')
import nibabel as nib
import pandas as pd
import numpy as np
import scipy.stats as st
from ioTools import CiftiReader as CR
from ioTools import save2cifti
from ioTools import GiftiReader as GR
from nibabel import cifti2
import nibabel as nib
import glob
import os
import matplotlib.pyplot as mp
import seaborn as sns

#generate an empty df
final = pd.DataFrame()

##get the right label
label_path = 'D:/hcp/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR_LabelKey.txt'
label_df = pd.read_table(label_path, usecols=['GLASSERLABELNAME'])
label = list(label_df['GLASSERLABELNAME'])

##get significant GBC or FC according to the MCC file
#input MCC file
gbc_path = 'D:/hcp/MAPnLone/cerebrum_gbc/results_dat_tstat_fwep_c2.pscalar.nii'
fc_path = 'D:/hcp/MAPnLone/cerebrum_RAAIC_FC/results_dat_tstat_cfwep_c2.pscalar.nii'
#get significant GBC
gimg = cifti2.load(gbc_path)
garray = gimg.get_data()
gsig_roi = np.where(garray>=1.597)
gsig_roi = list(gsig_roi[1])
#get significant FC
fimg = cifti2.load(fc_path)
farray = fimg.get_data()
fsig_roi = np.where(farray>=2)
fsig_roi = list(fsig_roi[1])


##get raw value of those significant GBC or FC
#input raw data file
gbc_p = 'D:/hcp/rsfMRI_GBC_cerebrum_MAPnLONE_970.pscalar.nii'
fc_p = 'D:/hcp/MAPnLone/cerebrum_RAAIC_FC/rsfMRI_RAAIC_FC_cerebrum_MAPnLONE_970.pscalar.nii'
#get raw value of GBC
g_img = nib.load(gbc_p)
g_array = g_img.get_fdata()
for i in gsig_roi:
    final[f'GBC_{label[i]}'] = g_array[:,i]
#get raw value of FC
f_img = nib.load(fc_p)
f_array = f_img.get_fdata()
for i in fsig_roi:
    final[f'FC_{label[i]}'] = f_array[:,i] 
#input behavioral file
beh = pd.read_csv('D:/hcp/MAP_lone_covariates_scaled_nools.csv')
#merge them together
final = pd.concat([beh,final],axis=1)
#storage the new file
final.to_csv('D:/hcp/MAPnLone/MAP_lone_beh_brain.csv')


##correct the roi label of GBC's multiple comparison correction file
#get the right label
label_path = 'D:/hcp/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR_LabelKey.txt'
label_df = pd.read_table(label_path, usecols=['INDEX','LABEL','GLASSERLABELNAME'])
labelnames = list(label_df.iloc[0:360,2])
#input the MCC file and get the variable to change
path = 'D:/hcp/MAPnLone/cerebrum_gbc/results_dat_tstat_fwep_c2.pscalar.nii'
img = cifti2.load(path)
array = img.get_fdata()
indexmap1 = img.header.get_index_map(1)
indexmap0 = img.header.get_index_map(0)
mapmodels = indexmap1._maps
#change label
for idx, i in enumerate(mapmodels[2:]):
    mapmodels[idx+2].name = labelnames[idx]
indexmap1._maps = mapmodels
#generate a new MCC file
matrix = cifti2.Cifti2Matrix()
matrix.append(indexmap0)
matrix.append(indexmap1)
header = cifti2.Cifti2Header(matrix)
img = cifti2.Cifti2Image(array, header)
#storage
cifti2.save(img, f'D:/hcp/MAPnLone/cerebrum_gbc/relabelled_results_dat_tstat_fwep_c2.pscalar.nii')


    
