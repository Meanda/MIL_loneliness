# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 19:45:10 2022
merge social variables and GBCroi112
1. merge variables
2. exclude outliers of those social variables


@author: zhang
"""
import pandas as pd
import numpy as np
from nibabel import cifti2


#load behavioral file
f = f"D:/hcp/social_nomiss.csv"
df = pd.read_csv(f)
#load gbc parcellation csv file
path = f'D:/hcp/gbc_zstat_sub997.pscalar.nii'
img = cifti2.load(path)
array = img.get_data()

#check which parcel is significant
m_path = 'D:/hcp/palm/MeanPurp_Unadj_pscalar_fisherz_0314/results_dat_tstat_fwep_c2.pscalar.nii'
m_img = cifti2.load(m_path)
m_array = m_img.get_data()
sig_roi = np.where(m_array>=1.301)


roi112 = array[:,111]

df['roi112'] = roi112
for col in df.columns[3:]:
    df = df[abs(df[col])<=3]

df.to_csv("D:/hcp/social_nomiss_nools_GBCroi112.csv", index=False)



