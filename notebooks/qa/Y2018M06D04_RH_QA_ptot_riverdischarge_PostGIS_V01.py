
# coding: utf-8

# In[1]:

""" Create a table with sample data from the ptot and riverdischarge results.
-------------------------------------------------------------------------------

Author: Rutger Hofste
Date: 20180604
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""


TESTING = 1
OVERWRITE_OUTPUT = 1
SCRIPT_NAME = 'Y2018M06D04_RH_QA_ptot_riverdischarge_PostGIS_V01'
OUTPUT_VERSION = 1

DATABASE_ENDPOINT = "aqueduct30v05.cgpnumwmfcqc.eu-central-1.rds.amazonaws.com"
DATABASE_NAME = "database01"

INPUT_TABLE_LEFT_NAME = 'hybas06_v04'
INPUT_TABLE_RIGHT_NAME = 'y2018m05d29_rh_total_demand_postgis_30spfaf06_v01_v02'
OUTPUT_TABLE_NAME = SCRIPT_NAME.lower() + "_v{:02.0f}".format(OUTPUT_VERSION)
OUTPUT_SCHEMA = "test"

# Filter 
TEMPORAL_RESOLUTION = "month"
YEAR = 1970
MONTH = 1
PFAFID_RANGE_MIN = 1
PFAFID_RANGE_MAX = 200000

print("Input Table Left: " , INPUT_TABLE_LEFT_NAME, 
      "\nInput Table Right: " , INPUT_TABLE_RIGHT_NAME, 
      "\nOutput Table: " , OUTPUT_SCHEMA +"."+OUTPUT_TABLE_NAME)


# In[2]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version


# In[3]:

# imports
import re
import os
import numpy as np
import pandas as pd
from datetime import timedelta
from sqlalchemy import *
pd.set_option('display.max_columns', 500)


# In[4]:

F = open("/.password","r")
password = F.read().splitlines()[0]
F.close()

engine = create_engine("postgresql://rutgerhofste:{}@{}:5432/{}".format(password,DATABASE_ENDPOINT,DATABASE_NAME))
connection = engine.connect()

sqls = []

if OVERWRITE_OUTPUT:
    sqls.append("DROP TABLE IF EXISTS {}.{};".format(OUTPUT_SCHEMA,OUTPUT_TABLE_NAME))
    sqls.append("DROP TABLE IF EXISTS {}.temp_right".format(OUTPUT_SCHEMA))


# In[5]:

sqls.append(
"CREATE TABLE {}.temp_right AS "
"SELECT * FROM {} "
"WHERE "
"pfafid_30spfaf06 > {} AND "
"pfafid_30spfaf06 < {} AND "
"temporal_resolution = '{}' AND "
"year = {} AND "
"month = {};".format(OUTPUT_SCHEMA ,INPUT_TABLE_RIGHT_NAME,PFAFID_RANGE_MIN,PFAFID_RANGE_MAX,TEMPORAL_RESOLUTION,YEAR,MONTH))


# In[6]:

sqls.append(
"CREATE TABLE {}.{} AS "   
"SELECT "
"hybas06_v04.pfaf_id, "
"hybas06_v04.geom, "
"month, "
"year, "
"area_m2_30spfaf06, "
"area_count_30spfaf06, "
"pdomww_m_30spfaf06, "
"pindww_m_30spfaf06, "
"pirrww_m_30spfaf06, "
"plivww_m_30spfaf06, "
"ptotww_m_30spfaf06, "
"pdomwn_m_30spfaf06, "
"pindwn_m_30spfaf06, "
"pirrwn_m_30spfaf06, "
"plivwn_m_30spfaf06, "
"ptotwn_m_30spfaf06, "
"riverdischarge_m_30spfaf06, "
"pfafid_30spfaf06 "
"FROM hybas06_v04 "
"INNER JOIN test.temp_right ON test.temp_right.pfafid_30spfaf06 = hybas06_v04.pfaf_id".format(OUTPUT_SCHEMA,OUTPUT_TABLE_NAME)
)


# In[7]:

for sql in sqls:
    print(sql)
    result = engine.execute(sql)   


# In[8]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)


# Previous runs:

# In[9]:

engine.dispose()


# In[ ]:



