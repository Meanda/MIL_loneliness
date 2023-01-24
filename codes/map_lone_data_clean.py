# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:36:22 2022

Target: Merge behavioral covariates and variables into the same table. 
    Make sure there shoud be two versions: raw data and corrected data
    Clean the data according to the criteria
Outline:
    1. load related covariates and variables and merge them
    2. clean data (N = 978)
    3. gender codes: M=1; F=0
    4. generate basic descriptive information and output files
    5. exclude outliers after normalization (thus no output file with raw data, here N = 970)
input file:
    'D:/hcp/S1200_behavior.csv'
    'D:/hcp/S1200_behavior_restricted.csv'
    rsfMRI: 'D:/hcp/HCPYA_rfMRI_file_check.tsv'
    EB: '122418','168240','376247'
output file:
    'D:/hcp/MAP_lone_covariates_overview.csv'
    'D:/hcp/MAP_lone_covariates_raw.csv'
    'D:/hcp/MAP_lone_covariates_scaled_nools.csv'
@author: zhang
"""
import pandas as pd
import numpy as np

#load related covariates and variables and merge them together
hcpbeh_path = 'D:/hcp/S1200_behavior.csv'
hcpre_path = 'D:/hcp/S1200_behavior_restricted.csv'

hcpre = pd.read_csv(hcpre_path, usecols=['Subject','Gender','Age_in_Yrs','SSAGA_Educ'])
hcpbeh = pd.read_csv(hcpbeh_path, usecols=['Subject','MMSE_Score','MeanPurp_Unadj','Loneliness_Unadj',
                                           'LifeSatisf_Unadj','PosAffect_Unadj'])
hcp_df = hcpre.combine_first(hcpbeh)
order = ['Subject','Gender','Age_in_Yrs','MMSE_Score','SSAGA_Educ','MeanPurp_Unadj','Loneliness_Unadj','LifeSatisf_Unadj','PosAffect_Unadj']
hcp_df = hcp_df[order]

#clean data
#step 1: get the list of participants with complete rsfMRI data, finally output this list.
check = pd.read_csv('D:/hcp/HCPYA_rfMRI_file_check.tsv',sep='\t')
check = check.set_index('subID')
for col in check.columns:
    check = check[check[col]=='ok=(1200, 91282)']
check = check.reset_index()
subid = list(check['subID'])
pd.DataFrame(subid).to_csv('D:/hcp/rsfMRI_check_list.csv',index=False)

#step 2: exclude participants with missing value in any variable
hcp_df = hcp_df[hcp_df['Subject'].isin(subid)]
hcp_df = hcp_df.dropna(how='any')

#exclude participants with no EB information
miss_eb = ['122418','168240','376247']
hcp_df = hcp_df[~hcp_df['Subject'].isin(miss_eb)]

#exclude participants with MMSE scores no more than 26
final = hcp_df[hcp_df['MMSE_Score']>26]

#M=1; F=0
final = final.replace('F',0)
final = final.replace('M',1)

#generate basic descriptive information，including skewness (偏斜度) and kurtosis (峰度)
final_ow = final.iloc[:,2:].describe().T
skew_l = list()
kurt_l = list()
for col in final.columns[2:]:
    skew_l.append(final[col].skew())
    kurt_l.append(final[col].kurt())

final_ow['skewness'] = skew_l
final_ow['kurtosis'] = kurt_l
final_ow = final_ow.reset_index()
final_ow = final_ow.round(2)

#output raw data and descriptive information
final_ow.to_csv('D:/hcp/MAP_lone_covariates_overview.csv', index=False) #descriptive information
final.to_csv('D:/hcp/MAP_lone_covariates_raw.csv', index=False)

##exclude participants whose value of any variable or covariate is outlier
#input the data
final = pd.read_csv('D:/hcp/MAP_lone_covariates_raw.csv')
#normalization
from sklearn import preprocessing

scaler = preprocessing.StandardScaler()
df_scaled = scaler.fit_transform(final.iloc[:,5:])
df_scaled = pd.DataFrame(df_scaled, columns=final.columns[5:])
final.iloc[:,5:] = df_scaled
ow = final.describe().T
#exclude outliers
for col in final.columns[5:]:
    final = final[abs(final[col])<=3]
#output data
final.to_csv('D:/hcp/MAP_lone_covariates_scaled_nools.csv', index=False)




    






