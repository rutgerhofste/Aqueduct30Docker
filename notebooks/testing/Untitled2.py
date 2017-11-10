
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import geopandas as gpd


# In[2]:

get_ipython().magic('matplotlib inline')


# In[3]:

fname = "/volumes/repos/Aqueduct30Docker/notebooks/testing/samplefiles/testShape.shp"


# In[ ]:

def categorize(attributes):
    type(attributes)


# In[85]:

def addFeatures(fname):
    f = Reader(fname)
    for item in test.records():
        attributes = item.attributes
        geometry = item.geometry
        feature = ShapelyFeature(geometry,ccrs.PlateCarree(),facecolor='blue',edgecolor="black",alpha=0.5)
        ax.add_feature(feature)


# In[86]:

fig = plt.figure(figsize=(20, 100))
ax = plt.axes(projection=ccrs.Robinson())
extents = [-20,20,30,40]
ax.set_extent(extents, crs=None)
ax.coastlines(resolution='50m')

addFeatures(fname)





# In[75]:


    


# In[ ]:

f = Reader(fname)
for item in test.records():
    attributes = item.attributes
    geometry = item.geometry
    feature = ShapelyFeature(geometry,ccrs.PlateCarree())
    ax.add_feature(feature)
    


# In[66]:

# Using Cartopy


shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='blue',edgecolor='red')


ax.add_feature(shape_feature)





# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[4]:




# In[48]:

fig = plt.figure(figsize=(20, 100))
ax = plt.axes(projection=ccrs.Robinson())
extents = [-20,20,30,40]
ax.coastlines(resolution='50m')
ax.set_extent(extents, crs=None)


test = Reader(fname)
test.records()
for item in test.records():
    attributes = item.attributes
    geometry = item.geometry
    print(type(geometry))
    feature = ShapelyFeature(geometry,ccrs.PlateCarree())
    ax.add_feature(feature)

    
    


# In[8]:

shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='blue',edgecolor='red')

