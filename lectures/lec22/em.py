
# # CS 429: Information Retrieval
# <br>
# 
# ## Lecture 22: Expectation Maximization for Clustering
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology
# ### Spring 2014

# Below, we use expectation maximization to find the means of two clusters for two-dimensional data.
# 
# We assume diagonal covariance matrices.
# 
# The bivariate normal density in this case is:
# 
# $\begin{align}
# N(\vec{\mu}, \vec{\sigma}, \vec{x}) = \frac{1}{2\pi\sigma_1\sigma_2}
# \exp\left(- \frac{(x_1-\mu_1)^2}{2\sigma_1} + \frac{(x_2-\mu_2)^2}{2\sigma_2}\right)
# \end{align}
# $
# 
# Let $\vec{\mu^j}, \vec{\sigma^j}$ be the mean and variance for cluster $j$. We update at each iteration with:
# 
# 
# $\begin{align}
# \mu_j' = \frac{\sum_i N(\vec{\mu^j}, \vec{\sigma^j}, \vec{x_i})\vec{x_i}}{\sum_i N(\vec{\mu^j}, \vec{\sigma^j}, \vec{x_i})}
# \end{align}
# $
# 

# In[274]:

get_ipython().magic(u'pylab inline')
import numpy as np
from numpy import array as npa

def gauss(mean, covar, x):
    """
    Bivariate Gaussian distribution, assuming diagonal covariance.
    1/(2*pi*v1*v2) * exp(- 1/2 * (x1-mean1)**2/v1 + (x2-mean2)**2/v2)
    """
    Xmu = x[0]-mean[0]
    Ymu = x[1]-mean[1]
    z = Xmu**2 / (covar[0]**2) + Ymu**2 / (covar[1]**2)
    denom = 2 * np.pi * covar[0] * covar[1]
    return np.exp(-z / 2.) / denom

data = np.array([npa([0.,0.02]), npa([.1,0.005]), npa([-0.1,.01]),
                 npa([1.01,1.]), npa([.99,0.9]), npa([1.02,1.1])])

mean1 = npa([-.5, -.5])
covar1 = npa([.4, .4])
mean2 = npa([1.5, 1.5])
covar2 = npa([.4, .4])

def plotme(mean1, covar1, mean2, covar2, data):
    x, y = np.mgrid[-1.5:2.5:.01, -1.5:2.5:.01]
    pos = np.empty(x.shape + (2,))
    pos[:, :, 0] = x; pos[:, :, 1] = y
    contourf(x, y,
             [gauss(mean1, covar1, [xi, yi]) + gauss(mean2, covar2, [xi, yi])
              for (xi, yi) in zip(x, y)])
    scatter([d[0] for d in data], [d[1] for d in data], marker='v', color='w')

plotme(mean1, covar1, mean2, covar2, data)


# Out[274]:

#     Populating the interactive namespace from numpy and matplotlib
# 

# image file:

# In[275]:

def e_step(data, mean1, covar1, mean2, covar2):
    results = []
    for point in data:
        results.append([gauss(mean1, covar1, point),
                        gauss(mean2, covar2, point)])
    return results

def m_step(data, mean1, covar1, mean2, covar2, probs):
    new_mean1 = npa([0., 0.])
    new_mean2 = npa([0., 0.])
    for point, prob in zip(data, probs):
        new_mean1 += prob[0] * point
        new_mean2 += prob[1] * point
    new_mean1 /= sum(p[0] for p in probs)
    new_mean2 /= sum(p[1] for p in probs)
    return new_mean1, new_mean2

def iterate(data, mean1, covar1, mean2, covar2):
    probs = e_step(data, mean1, covar1, mean2, covar2)
    new_mean1, new_mean2 = m_step(data, mean1, covar1, mean2, covar2, probs)
    print 'new mean1=', new_mean1, '\nnew mean2=', new_mean2
    print 'difference in means=', np.sum(np.abs(new_mean1 - mean1) + np.abs(new_mean2 - mean2))
    plotme(new_mean1, covar1, new_mean2, covar2, data)
    return new_mean1, new_mean2

mean1, mean2 = iterate(data, mean1, covar1, mean2, covar2)


# Out[275]:

#     new mean1= [-0.02004906  0.01202256] 
#     new mean2= [ 1.01010493  1.02306492]
#     difference in means= 1.9588036624
# 

# image file:

# In[276]:

mean1, mean2 = iterate(data, mean1, covar1, mean2, covar2)


# Out[276]:

#     new mean1= [ 0.00123465  0.01372373] 
#     new mean2= [ 1.0050071   0.99909989]
#     difference in means= 0.0520477245206
# 

# image file:

# In[277]:

mean1, mean2 = iterate(data, mean1, covar1, mean2, covar2)


# Out[277]:

#     new mean1= [ 0.00242549  0.01400209] 
#     new mean2= [ 1.00449348  0.99771439]
#     difference in means= 0.00336831060153
# 

# image file:

# In[278]:

mean1, mean2 = iterate(data, mean1, covar1, mean2, covar2)


# Out[278]:

#     new mean1= [ 0.00249586  0.01402144] 
#     new mean2= [ 1.00445858  0.99762789]
#     difference in means= 0.000211134878354
# 

# image file:

# In[279]:

for i in range(10):
    mean1, mean2 = iterate(data, mean1, covar1, mean2, covar2)


# Out[279]:

#     new mean1= [ 0.00250007  0.01402263] 
#     new mean2= [ 1.00445635  0.99762242]
#     difference in means= 1.30901486128e-05
#     new mean1= [ 0.00250032  0.0140227 ] 
#     new mean2= [ 1.00445621  0.99762208]
#     difference in means= 8.10454092567e-07
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 5.0198829414e-08
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 3.11143275554e-09
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 1.92993729938e-10
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 1.19795852925e-11
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 7.43958714078e-13
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 4.62785192112e-14
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 2.99760216649e-15
#     new mean1= [ 0.00250033  0.01402271] 
#     new mean2= [ 1.0044562   0.99762205]
#     difference in means= 2.71917904859e-16
# 

# image file:

# In[ ]:



