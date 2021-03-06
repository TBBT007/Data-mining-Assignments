# -*- coding: utf-8 -*-
"""fuzzy_c_means.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ds-tm5_3c4pIDLDrttLnbzC1x676miIy
"""

import numpy as np
import pandas as pd
# import skfuzzy as fuzzy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score as db_score

import math
from scipy.spatial import distance
#fuzzy
def fuzzy(x,c=2):
  # initialise centroids
  indices = np.arange(x.shape[0])
  # for i in range(x.shape[0]):
    # indices[i] = i
  np.random.seed(1)
  choices = np.random.choice(indices,c)
  # print(choices)
  centroids = np.empty((c, x.shape[1]))
  # centroids.shape = 
  for i in range(c):
    centroids[i] = x[choices[i]]
  #find membership
  i = 0
  # print(centroids)
  while (True): # new_centroid - centroid < eps
    # print(f"iteration :  + {i}")
    if i!=0:
      centroids = new_centroids
    i+=1
    # print(centroids)
    membership_vals = membership(x,centroids,c) # x[0] X c
    labels = find_labels( x, membership_vals,c)
    new_centroids = find_center(x, labels,membership_vals,c)
    diff =0
    for j in range(c):
      diff += distance.euclidean(centroids[j],new_centroids[j])
    if i>6:
      break
  return labels,centroids
  #iterate till threshold

  # return centroids and labels
def membership(x,centroids,c):
  # x X c
  membership_vals = np.empty((x.shape[0] ,c))
  # membership_vals.shape= 
  for i in range(c):
    for j in range(x.shape[0]):
      mem = 0
      num = distance.euclidean(x[j],centroids[i])
      if num!=0:
        for k in centroids:
          dist  = distance.euclidean(x[j],k)
          if dist!=0:
            mem += (num/dist)**2
          else:
            mem = 0
            break
        # if math.isnan(mem):
          # mem = 0
        if mem!=0:
          mem = mem**-1 
        # else:
          # mem=1
      else:
        mem=1
      membership_vals[j][i] = mem
  # print("membership done")
  return membership_vals
  # return 

def find_center(x,labels,membership_vals,c):
  new_centroids = []
  # new_centroids.shape = (c,)
  for i in range(c):
    num=np.zeros(x.shape[1])
    den=0
    for j in range(x.shape[0]):
      # print(labels)
      if labels[j]==i:
        num = np.add(num,(membership_vals[j][i]**2)*x[j])
        den += membership_vals[j][i]**2
    # print("num")
    # print(num)
    # print("den")
    # print(den)
    if den==0:
      cen= num
      # print(i)
      # print(membership_vals[j][i])
    else:
      cen = num/den
    new_centroids.append(cen)
  return np.array(new_centroids)

def find_labels(x, memberships,c):
  labels = np.empty((x.shape[0],))
  # labels.shape = (
  for i in range(x.shape[0]):
    # max_mem = np.amax(x[i])
    # index = x[i].index(max(x[i]))
    # print(memberships[i])
    index = np.where(memberships[i] == np.amax(memberships[i]))
    # print("index")
    # print(memberships[i])
    # print(index)
    labels[i] = index[0][0]
    # print(labels)
  return labels

# def distance(p1,p2):
  # return np.linalg.norm(p1-p2)

sil = []
db = []
for j in range(1,57):
  df = pd.read_csv(str(j)+".csv",header=None)
  X = df.to_numpy()
  X = X[:,:-1]
  # print(np.isnan(X).any() and np.isinf(X).any())
  sil_each = []
  db_each = []
  np.random.seed(j)
  for i in range(2,12):
    cmeans = fuzzy(X,i)
    # print("done")
    sil_each.append(silhouette_score(X,cmeans[0]))
    db_each.append(db_score(X,cmeans[0]))
  sil.append(sil_each)
  db.append(db_each)
  print("done")

sil.append([0,0,0,0,0,0,0,0,0,0])
db.append([0,0,0,0,0,0,0,0,0,0])
for j in range(8,57):
  df = pd.read_csv(str(j)+".csv",header=None)
  X = df.to_numpy()
  X = X[:,:-1]
  # print(np.isnan(X).any() and np.isinf(X).any())
  sil_each = []
  db_each = []
  np.random.seed(j)
  for i in range(2,12):
    cmeans = fuzzy(X,i)
    # print("done")
    sil_each.append(silhouette_score(X,cmeans[0]))
    db_each.append(db_score(X,cmeans[0]))
  sil.append(sil_each)
  db.append(db_each)
  print("done")

sil.append([0,0,0,0,0,0,0,0,0,0])
db.append([0,0,0,0,0,0,0,0,0,0])
sil =[]
db =[]
for j in range(7,8):
  df = pd.read_csv(str(j)+".csv",header=None)
  X = df.to_numpy()
  X = X[:,:-1]
  # print(np.isnan(X).any() and np.isinf(X).any())
  sil_each = []
  db_each = []
  np.random.seed(j)
  for i in range(2,12):
    cmeans = fuzzy(X,i)
    # print("done")
    sil_each.append(silhouette_score(X,cmeans[0]))
    db_each.append(db_score(X,cmeans[0]))
  sil.append(sil_each)
  db.append(db_each)
  print("done")

sil

DF = pd.DataFrame(sil)
DF.to_csv("sil.csv")

DF = pd.DataFrame(db)
DF.to_csv("db.csv")

sil_db = []
for i in sil:
  sil_db_i = i

sil = np.array(sil)
db = np.array(db)
np.concatenate((sil,db),axis=1)

sil_db = np.concatenate((sil,db),axis=1)
print(sil_db.shape)

DF = pd.DataFrame(sil_db)
DF.to_csv("sil_db.csv")