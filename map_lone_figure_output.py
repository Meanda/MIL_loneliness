# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:55:16 2022
draw the figure 1B in article - scatterplot with regression line
xlabel:MIL; ylabel: GBC or FC
input file: 'D:/hcp/MAPnLone/MAP_lone_beh_brain.csv'
output file: 'D:/hcp/MAPnLone/MAP_GBC_scatter.jpg';
    'D:/hcp/MAPnLone/MAP_FC31pv_scatter.jpg'
    'D:/hcp/MAPnLone/MAP_FC31pd_scatter.jpg'
    'D:/hcp/MAPnLone/MAP_FC8Av_scatter.jpg'
@author: zhang
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import seaborn as sns
from sklearn.linear_model import LinearRegression
import scipy.stats as st

#load input file
behpath = 'D:/hcp/MAPnLone/MAP_lone_beh_brain.csv'
final = pd.read_csv(behpath)


#normalization
from sklearn import preprocessing
scaler = preprocessing.StandardScaler()
df_scaled = scaler.fit_transform(final.iloc[:,6:])
df_scaled = pd.DataFrame(df_scaled, columns=final.columns[6:])
final.iloc[:,6:] = df_scaled

# exclude outliers
#final = final[abs(final['GBC_R_AAIC_ROI'])<=3]

##GBC
#calculate correlation and significance
correlation, p_value = st.pearsonr(final['MeanPurp_Unadj'],final['GBC_R_AAIC_ROI'])

#set regression model
mil = final['MeanPurp_Unadj'].tolist()
gbc = final['GBC_R_AAIC_ROI'].tolist()
regressor = LinearRegression()
regressor = regressor.fit(np.reshape(mil,(-1,1)),np.reshape(gbc,(-1,1)))
print(regressor.coef_, regressor.intercept_)

#scatter plot
#set figure size
mp.figure(figsize=(10,10))
#set spines' color and width
ax = mp.axes()
ax.spines['bottom'].set_linewidth('3.0')
ax.spines['left'].set_linewidth('3.0')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#draw the fiture
mp.scatter(x=final['MeanPurp_Unadj'],y=final['GBC_R_AAIC_ROI'],marker='o',color='k',linewidths=3)
#set label and thickness of ticks
mp.xlabel('Meaning in life',fontsize=30)
mp.ylabel('GBC of right AAIC',fontsize=30)
mp.xticks(fontsize=30)
mp.yticks(fontsize=30)
#regressive prediction line
mp.plot(np.reshape(mil,(-1,1)),regressor.predict(np.reshape(mil,(-1,1))),color='r',linewidth=3)
#add annotation of r value and p-value
mp.text(1,6, f'r = {round(correlation,2)}',fontsize=30)
mp.text(1,5, 'p < 0.001',fontsize=30)
#storage
#mp.show()
mp.savefig('D:/hcp/MAPnLone/MAP_GBC_scatter.jpg')
mp.close()

##FC 31pv
#calculate correlation and significance
correlation, p_value = st.pearsonr(final['MeanPurp_Unadj'],final['FC_R_31pv_ROI'])
p_value = round(p_value, 4)

#set regression model
mil = final['MeanPurp_Unadj'].tolist()
gbc = final['FC_R_31pv_ROI'].tolist()
regressor = LinearRegression()
regressor = regressor.fit(np.reshape(mil,(-1,1)),np.reshape(gbc,(-1,1)))
print(regressor.coef_, regressor.intercept_)

#scatter plot
#set figure size
mp.figure(figsize=(10,10))
#set spines' color and width
ax = mp.axes()
ax.spines['bottom'].set_linewidth('3.0')
ax.spines['left'].set_linewidth('3.0')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#draw the fiture
mp.scatter(x=final['MeanPurp_Unadj'],y=final['FC_R_31pv_ROI'],marker='o',color='k',linewidths=3)
#set label and thickness of ticks
mp.xlabel('Meaning in life',fontsize=30)
mp.ylabel('FC with right 31pv',fontsize=30)
mp.ylim((-3,4))
mp.xticks(fontsize=30)
mp.yticks(fontsize=30)
#regressive prediction line
mp.plot(np.reshape(mil,(-1,1)),regressor.predict(np.reshape(mil,(-1,1))),color='r',linewidth=3)
#add annotation of r value and p-value
mp.text(1,4, f'r = {round(correlation,2)}',fontsize=30)
mp.text(1,3.5, 'p < 0.001',fontsize=30)
#storage
#mp.show()
mp.savefig('D:/hcp/MAPnLone/MAP_FC31pv_scatter.jpg')
mp.close()

##FC 31pd
#calculate correlation and significance
correlation, p_value = st.pearsonr(final['MeanPurp_Unadj'],final['FC_R_31pd_ROI'])
p_value = round(p_value, 4)
#set regression model
mil = final['MeanPurp_Unadj'].tolist()
gbc = final['FC_R_31pd_ROI'].tolist()
regressor = LinearRegression()
regressor = regressor.fit(np.reshape(mil,(-1,1)),np.reshape(gbc,(-1,1)))
print(regressor.coef_, regressor.intercept_)

#scatter plot
#set figure size
mp.figure(figsize=(10,10))
#set spines' color and width
ax = mp.axes()
ax.spines['bottom'].set_linewidth('3.0')
ax.spines['left'].set_linewidth('3.0')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#draw the fiture
mp.scatter(x=final['MeanPurp_Unadj'],y=final['FC_R_31pd_ROI'],marker='o',color='k',linewidths=3)
#set label and thickness of ticks
mp.xlabel('Meaning in life',fontsize=30)
mp.ylabel('FC with right 31pd',fontsize=30)
mp.xticks(fontsize=30)
mp.yticks(fontsize=30)
mp.ylim((-3,4))
#regressive prediction line
mp.plot(np.reshape(mil,(-1,1)),regressor.predict(np.reshape(mil,(-1,1))),color='r',linewidth=3)
#add annotation of r-value and p-value
mp.text(1,4, f'r = {round(correlation,2)}',fontsize=30)
mp.text(1,3.5, 'p < 0.001',fontsize=30)
#storage
#mp.show()
mp.savefig('D:/hcp/MAPnLone/MAP_FC31pd_scatter.jpg')
mp.close()

##FC 8Av
#calculate correlation and significance
correlation, p_value = st.pearsonr(final['MeanPurp_Unadj'],final['FC_R_8Av_ROI'])

#set regression model
mil = final['MeanPurp_Unadj'].tolist()
gbc = final['FC_R_8Av_ROI'].tolist()
regressor = LinearRegression()
regressor = regressor.fit(np.reshape(mil,(-1,1)),np.reshape(gbc,(-1,1)))
print(regressor.coef_, regressor.intercept_)

#scatter plot
#set figure size
mp.figure(figsize=(10,10))
#设置边框
ax = mp.axes()
ax.spines['bottom'].set_linewidth('3.0')
ax.spines['left'].set_linewidth('3.0')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#set spines' color and width
mp.scatter(x=final['MeanPurp_Unadj'],y=final['FC_R_8Av_ROI'],marker='o',color='k',linewidths=3)
#draw the fiture
mp.xlabel('Meaning in life',fontsize=30)
mp.ylabel('FC with Right 8Av',fontsize=30)
mp.xticks(fontsize=30)
mp.yticks(fontsize=30)
mp.ylim((-3,4))
#regressive prediction line
mp.plot(np.reshape(mil,(-1,1)),regressor.predict(np.reshape(mil,(-1,1))),color='r',linewidth=3)
#add annotation of r-value and p-value
mp.text(1,4, f'r = {round(correlation,2)}',fontsize=30)
mp.text(1,3.5, 'p < 0.001',fontsize=30)
#storage
#mp.show()
mp.savefig('D:/hcp/MAPnLone/MAP_FC8Av_scatter.jpg')
mp.close()



#区分性别

