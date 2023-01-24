# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 21:31:52 2022

@author: zhang
"""

import pandas as pd
import numpy as np
import os

#生成所需文件夹
def mkdirs(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('--- new folder... ---')
        print('--- OK ---')
    else:
        print('--- There is this folder! ---')

behpath = 'D:/hcp/social_nomiss.csv'
beh = pd.read_csv(behpath)
cols = list(beh.columns[3:])
dirpath = 'D:/hcp/palm'
for col in cols:
    mkdirs(f'{dirpath}/{col}_pscalar_0127')

#从design matrix文件夹复制文件过去
import shutil
for col in cols:
    shutil.copy(f'{dirpath}/C.con' ,f'{dirpath}/{col}_pscalar_0127')
    shutil.copy(f'{dirpath}/EB.CSV' ,f'{dirpath}/{col}_pscalar_0127')
    shutil.copy(f'D:/hcp/design_matrix_follow_hcp/M_{col}.mat' ,f'{dirpath}/{col}_pscalar_0127')
