
# coding: utf-8

# # Calculate Water Stress from dataframe
# 
# * Purpose of script: calculate total demand (Dom, IrrLinear, Liv, Ind) and Reduced Runoff and water stress.
# * Author: Rutger Hofste
# * Kernel used: python35
# * Date created: 20171002

# In[1]:

import time, datetime
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)


# In[2]:

INPUT_VERSION = 9
OUTPUT_VERSION = 4

S3_INPUT_PATH = "s3://wri-projects/Aqueduct30/processData/Y2017M09D15_RH_Add_Basin_Data_V01/output/"
S3_OUTPUT_PATH = "s3://wri-projects/Aqueduct30/processData/Y2017M10D02_RH_Calculate_Water_Stress_V01/output/"

EC2_INPUT_PATH = "/volumes/data/Y2017M10D02_RH_Calculate_Water_Stress_V01/input"
EC2_OUTPUT_PATH = "/volumes/data/Y2017M10D02_RH_Calculate_Water_Stress_V01/output"

INPUT_FILENAME = "Y2017M09D15_RH_Add_Basin_Data_V%0.2d" %(INPUT_VERSION)
OUTPUT_FILENAME = "Y2017M10D02_RH_Calculate_Water_Stress_V%0.2d" %(OUTPUT_VERSION)

TEST_BASINS = [292107,292101,292103,292108,292109]


# Read Pickle file instead of csv 

# In[3]:

get_ipython().system('rm -r {EC2_INPUT_PATH} ')
get_ipython().system('rm -r {EC2_OUTPUT_PATH} ')


# In[4]:

get_ipython().system('mkdir -p {EC2_INPUT_PATH} ')
get_ipython().system('mkdir -p {EC2_OUTPUT_PATH} ')


# In[5]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH} {EC2_INPUT_PATH} --recursive')


# In[6]:

import os
import pandas as pd


# In[7]:

dfBasins = pd.read_pickle(os.path.join(EC2_INPUT_PATH,INPUT_FILENAME+".pkl"))


# WS = Local WW / (avail runoff)  = Local WW / (Runoff_up + Runoff_local - WN_up)

# In[8]:

dfOut = dfBasins


# In[9]:

def calculateWaterStressYear(temporalResolution,year,df):
    dfTemp = df.copy()
    dfTemp["total_volume_naturalSupply_year_Y%0.4d" %(year)] = (dfTemp["upstream_total_volume_reducedmeanrunoff_year_Y1960Y2014"] + dfTemp["total_volume_reducedmeanrunoff_year_Y1960Y2014"]) 
    dfTemp["total_volume_availableSupply_year_Y%0.4d" %(year)] = dfTemp["total_volume_naturalSupply_year_Y%0.4d" %(year)] -                                                      dfTemp["upstream_total_volume_TotWN_year_Y%0.4d" %(year)]
    
    dfTemp["ws_year_Y%0.4d" %(year)] = dfTemp["total_volume_TotWW_year_Y%0.4d" %(year)] /                                        dfTemp["total_volume_availableSupply_year_Y%0.4d" %(year)]
    
    return dfTemp
    
def calculateWaterStressMonth(temporalResolution,year,month,df):
    dfTemp = df.copy()
    dfTemp["total_volume_naturalSupply_month_Y%0.4dM%0.2d" %(year,month)] = (dfTemp["upstream_total_volume_reducedmeanrunoff_month_Y1960Y2014M%0.2d" %(month)] + dfTemp["total_volume_reducedmeanrunoff_month_Y1960Y2014M%0.2d" %(month)]) 
    dfTemp["total_volume_availableSupply_month_Y%0.4dM%0.2d" %(year,month)] = (dfTemp["total_volume_naturalSupply_month_Y%0.4dM%0.2d" %(year,month)] -                                                                  dfTemp["upstream_total_volume_TotWN_month_Y%0.4dM%0.2d" %(year,month)])
    
    dfTemp["ws_month_Y%0.4dM%0.2d" %(year,month)] = dfTemp["total_volume_TotWW_month_Y%0.4dM%0.2d" %(year,month)] /                                                     dfTemp["total_volume_availableSupply_month_Y%0.4dM%0.2d" %(year,month)]
    return dfTemp
    
    


# In[10]:

temporalResolutions = ["year","month"]
year = 2014


# In[11]:

for temporalResolution in temporalResolutions:
    if temporalResolution == "year":
        months = [12]
        dfOut = calculateWaterStressYear(temporalResolution,year,dfOut)
        
    elif temporalResolution == "month":
        months = range(1,13)    
        for month in months:
            dfOut = calculateWaterStressMonth(temporalResolution,year,month,dfOut)


# In[ ]:

dfOut.to_csv(os.path.join(EC2_OUTPUT_PATH,OUTPUT_FILENAME+".csv"))


# In[ ]:

dfOut.to_pickle(os.path.join(EC2_OUTPUT_PATH,OUTPUT_FILENAME+".pkl"))


# In[ ]:

get_ipython().system('aws s3 cp {EC2_OUTPUT_PATH} {S3_OUTPUT_PATH} --recursive')


# In[ ]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)

