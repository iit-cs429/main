
# # CS 429: Information Retrieval
# 
# <br>
# 
# ## Lecture 5: Index Compression
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology 
# ### Spring 2014
# 
# ---
# 

# Last time:
# 
# - How do we build an index that does not fit into memory? 
# 
# Today: 
# 
# - How do we compress the contents of an index?
# 

# # Why compress an inverted index?
# 

# - Save disk space
# - Fit as much in memory as possible (caching)
# - Faster transfer from disk to memory

# # What will we compress?
# 
# - Vocabulary
# - Postings lists
# 
# <br>
# 
# To help compression, we need to know
# 
# - How large should we expect the vocabulary to be?
#   - helpful to compress vocabulary
# - How are terms distributed throughout documents?
#   - helpful to compress postings lists

# # Will the vocabulary get *that* big?
# 
# - $T$ = number of tokens
# - $V$ = number of terms
# 
# Can we estimate $V$ as a function of $T$?
# 
# $V = f(T)$

# In[240]:

# Let's read in some documents.
# This is a dataset of 11K newsgroups posts: http://qwone.com/~jason/20Newsgroups/
from sklearn.datasets import fetch_20newsgroups
docs = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes')).data
print 'read %d docs' % len(docs)


# Out[240]:

#     read 11314 docs
# 

# In[241]:

# Let's look at a couple documents.
print docs[0]


# Out[241]:

#     I was wondering if anyone out there could enlighten me on this car I saw
#     the other day. It was a 2-door sports car, looked to be from the late 60s/
#     early 70s. It was called a Bricklin. The doors were really small. In addition,
#     the front bumper was separate from the rest of the body. This is 
#     all I know. If anyone can tellme a model name, engine specs, years
#     of production, where this car is made, history, or whatever info you
#     have on this funky looking car, please e-mail.
# 

# In[242]:

print docs[100]


# Out[242]:

#     1.  Software publishing SuperBase 4 windows v.1.3           --->$80
#     
#     2.  OCR System ReadRight v.3.1 for Windows                  --->$65
#     
#     3.  OCR System ReadRight  v.2.01 for DOS                    --->$65
#     
#     4.  Unregistered Zortech 32 bit C++ Compiler v.3.1          --->$ 250
#          with Multiscope windows Debugger,
#          WhiteWater Resource Toolkit, Library Source Code
#     
#     5.  Glockenspiel/ImageSoft Commonview 2 Windows
#          Applications Framework for Borland C++                 --->$70
#     
#     6.  Spontaneous Assembly Library With Source Code           --->$50
#     
#     7.  Microsoft Macro Assembly 6.0                            --->$50
#     
#     8.  Microsoft Windows v.3.1 SDK Documentation               --->$125
#     
#     9.  Microsoft FoxPro V.2.0                                  --->$75
#     
#     10.  WordPerfect 5.0 Developer's Toolkit                    --->$20
#     
#     11.  Kedwell Software DataBoss v.3.5 C Code Generator       --->$100
#     
#     12.  Kedwell InstallBoss v.2.0 Installation Generator       --->$35
#     
#     13.  Liant Software C++/Views v.2.1
#            Windows Application Framework with Source Code       --->$195
#     
#     14.  IBM OS/2 2.0 & Developer's Toolkit                     --->$95
#     
#     15.  CBTree DOS/Windows Library with Source Code            --->$120
#     
#     16.  Symantec TimeLine for Windows                          --->$90
#     
#     17.  TimeSlip TimeSheet Professional for Windows            --->$30
# 

# In[243]:

from collections import defaultdict
import re

# Count the number of terms and tokens in a list of documents.
def count_terms_and_toks(docs):
    terms = defaultdict(lambda: 0)  # Map from term to count.
    n_tokens = 0
    for d in docs:
        for tok in re.findall('[\w]+',d.lower()):
            terms[tok] += 1
            n_tokens += 1
    return terms, n_tokens


# In[244]:

terms, n_tokens = count_terms_and_toks(docs)
print 'found %d tokens and %d terms' % (n_tokens, len(terms))


# Out[244]:

#     found 2407154 tokens and 101660 terms
# 

# How does the number of terms vary with the number of tokens?

# In[245]:

# Compute T/V for different subsets of the documents.
T = []
V = []
for n_docs in [10, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 10000]:
    terms, n_tokens = count_terms_and_toks(docs[:n_docs])
    print 'found %d tokens and %d terms in %d docs' % (n_tokens, len(terms), n_docs)    
    T.append(n_tokens)
    V.append(len(terms))


# Out[245]:

#     found 1270 tokens and 545 terms in 10 docs
#     found 20449 tokens and 4941 terms in 100 docs
#     found 50303 tokens and 8848 terms in 200 docs
#     found 105452 tokens and 17725 terms in 500 docs
#     found 209464 tokens and 24469 terms in 1000 docs
#     found 435254 tokens and 39713 terms in 2000 docs
#     found 619554 tokens and 46003 terms in 3000 docs
#     found 858034 tokens and 54854 terms in 4000 docs
#     found 1123558 tokens and 63355 terms in 5000 docs
#     found 2155062 tokens and 92689 terms in 10000 docs
# 

# In[246]:

# Let's plot the results.
get_ipython().magic(u'pylab inline')
xlabel('T')
ylabel('V')
plot(T, V, 'bo')


# Out[246]:

#     Populating the interactive namespace from numpy and matplotlib
# 

#     [<matplotlib.lines.Line2D at 0x10fca4350>]

# image file:

# Is this linear, polynomial, something else?

# In[247]:

# Let's try a linear fit
import numpy as np
linear = np.polyfit(T, V, 1)  # fit slope and intercept
print 'linear fit=%.2f*x + %.2f' % (linear[0], linear[1])
plot(T, V, 'bo', label='data')  # bo = blue circle
plot(T, np.polyval(linear, T), 'r-', label='linear')  # r- = red solid line
legend(loc='best')


# Out[247]:

#     linear fit=0.04*x + 11949.85
# 

#     <matplotlib.legend.Legend at 0x10c10ca50>

# image file:

# # Heaps' Law
# 
# An observed relation between $V$ and $T$:
# 
# $V = k T^b$
# 
# for constants $k$ (typically $30 < k < 100$) and $b$ (typically $b \approx 0.5$)

# In[248]:

# How do we set k and b in Heaps' Law?
# Minimize mean squared error.
from scipy.optimize import curve_fit
help(curve_fit)


# Out[248]:

#     Help on function curve_fit in module scipy.optimize.minpack:
#     
#     curve_fit(f, xdata, ydata, p0=None, sigma=None, **kw)
#         Use non-linear least squares to fit a function, f, to data.
#         
#         Assumes ``ydata = f(xdata, *params) + eps``
#         
#         Parameters
#         ----------
#         f : callable
#             The model function, f(x, ...).  It must take the independent
#             variable as the first argument and the parameters to fit as
#             separate remaining arguments.
#         xdata : An N-length sequence or an (k,N)-shaped array
#             for functions with k predictors.
#             The independent variable where the data is measured.
#         ydata : N-length sequence
#             The dependent data --- nominally f(xdata, ...)
#         p0 : None, scalar, or M-length sequence
#             Initial guess for the parameters.  If None, then the initial
#             values will all be 1 (if the number of parameters for the function
#             can be determined using introspection, otherwise a ValueError
#             is raised).
#         sigma : None or N-length sequence
#             If not None, it represents the standard-deviation of ydata.
#             This vector, if given, will be used as weights in the
#             least-squares problem.
#         
#         Returns
#         -------
#         popt : array
#             Optimal values for the parameters so that the sum of the squared error
#             of ``f(xdata, *popt) - ydata`` is minimized
#         pcov : 2d array
#             The estimated covariance of popt.  The diagonals provide the variance
#             of the parameter estimate.
#         
#         See Also
#         --------
#         leastsq
#         
#         Notes
#         -----
#         The algorithm uses the Levenberg-Marquardt algorithm through `leastsq`.
#         Additional keyword arguments are passed directly to that algorithm.
#         
#         Examples
#         --------
#         >>> import numpy as np
#         >>> from scipy.optimize import curve_fit
#         >>> def func(x, a, b, c):
#         ...     return a*np.exp(-b*x) + c
#         
#         >>> x = np.linspace(0,4,50)
#         >>> y = func(x, 2.5, 1.3, 0.5)
#         >>> yn = y + 0.2*np.random.normal(size=len(x))
#         
#         >>> popt, pcov = curve_fit(func, x, yn)
#     
# 

# In[249]:

# V = k * T^b
def heaps(T, k, b):
    return k*(T**b)


# In[250]:

# Fit k and b
heap_parms,covar = curve_fit(heaps, T, V)
print 'Heaps fit is %.2f*T^%.2f' % (heap_parms[0], heap_parms[1])


# Out[250]:

#     Heaps fit is 23.49*T^0.57
# 

# In[251]:

# Compare linear fit and Heaps fit
plot(T, V, 'bo', label='data')
plot(T, np.polyval(linear, T), 'r-', label='linear')
plot(T, heaps(T, *heap_parms), 'k--', label='heaps')  # k-- = black dashed line
xlabel('T')
ylabel('V')
legend(loc='best')


# Out[251]:

#     <matplotlib.legend.Legend at 0x10c1aa8d0>

# image file:

# In[252]:

print 'Heaps predicts %d terms for %d tokens, truth is %d.' % (heaps(T[-1], *heap_parms), T[-1], V[-1])


# Out[252]:

#     Heaps predicts 92835 terms for 2155062 tokens, truth is 92689.
# 

# # How are terms distributed across documents?
# 
# - How many times does the most frequent term occur? The $i$th most frequent term?

# In[253]:

# Let's plot and see.
# Recall that terms is a dict from term to frequency
print terms.items()[:5]


# Out[253]:

#     [(u'3ds2scn', 1), (u'l1tbk', 1), (u'porkification', 1), (u'mbhi8bea', 1), (u'woods', 15)]
# 

# In[254]:

# Sort frequency values in descending order
freqs = sorted(terms.values(), reverse=True)
print 'top 10 frequencies are', freqs[:10]


# Out[254]:

#     top 10 frequencies are [95622, 62381, 47659, 41940, 40610, 38542, 32494, 27802, 26975, 25011]
# 

# In[255]:

ranks = range(1, len(freqs)+1)
plot(ranks, freqs, 'bo', label='data')
legend(loc='best')
xlabel('rank')
ylabel('frequency')


# Out[255]:

#     <matplotlib.text.Text at 0x10b117990>

# image file:

# In[261]:

print '%d/%d terms occur once.' % (len([x for x in freqs if x == 1]), len(freqs))


# Out[261]:

#     50114/92689 terms occur once.
# 

# In[259]:

# That was ugly. The values decrease too rapidly. Let's try a log-log plot.
l_ranks = np.log10(ranks)
l_freqs = np.log10(freqs)
plot(l_ranks, l_freqs, 'bo', label='data')
legend(loc='best')
xlabel('log(rank)')
ylabel('log(frequency)')


# Out[259]:

#     <matplotlib.text.Text at 0x1098b9a10>

# image file:

# # Zipf's Law
# 
# Another empirical law that states that the frequency of a term is inversely proportional to its rank.
# 
# Let $f_i$ be the frequency of the $i$th most common term.
# 
# $ f_i \propto \frac{1}{i} $ 
# 
# equivalently
# 
# $ f_i = k$ $i^b $ for constant $k$ and $b=-1$
# 
# (c.f. Heap's law: $V = kT^b$)

# In[257]:

# Define the Zipf function and fit the k parameter.
def zipfs(i, k):
    return k / i
zipf_parms,covar = curve_fit(zipfs, ranks, freqs)
print 'Zipf fit is %.2f*T^-1' % zipf_parms[0]


# Out[257]:

#     Zipf fit is 123419.09*T^-1
# 

# In[258]:

plot(l_ranks, l_freqs, 'bo', label='data')
xlabel('log(rank)')
ylabel('log(frequency)')
plot(l_ranks, log10(zipfs(ranks, *zipf_parms)), 'k--', label='zipf')  # k-- = black dashed line
legend(loc='best')


# Out[258]:

#     <matplotlib.legend.Legend at 0x10b122ed0>

# image file:

# In[263]:

vocab = sorted(terms.keys())
print vocab[:10]


# Out[263]:

#     [u'0', u'00', u'000', u'0000', u'00000', u'000000', u'00000000', u'0000000004', u'00000000b', u'00000001']
# 

# In[270]:

from sys import getsizeof
getsizeof(1)


# Out[270]:

#     24

# # Dictionary compression
# 
# - Fixed-width storage
# - One big string
# - Blocked storage
# - Front encoding

# # Fixed-width storage
# 
# ![fixed](files/fixed.png)
# 
# [MRS](http://nlp.stanford.edu/IR-book/pdf/05comp.pdf)
# 
# Space = $(20 + 4 + 4)V  = 28V$ bytes
# 
# Why is 20 bytes / term wasteful?

# Average term $\approx$ 8 bytes

# # One big string
# 
# ![string](files/string.png)
# 
# [MRS](http://nlp.stanford.edu/IR-book/pdf/05comp.pdf)

# Assuming average term is 8 bytes, 
# 
# Space = $(8 + 4 + 4 + 3)V = 19V$ bytes (reduction from $28V$)

# # Blocked storage
# 
# Reduce number of term pointers:
# 
# ![block](files/block.png)
# 
# [MRS](http://nlp.stanford.edu/IR-book/pdf/05comp.pdf)

# - Assume $k$ blocks, we store only $k$ term pointers (instead of $V$)
# - But, we also need to add one byte per term for offsets (term length)
# 
# Space = $(8 + 4 + 4)V + k + V = 17V + k$ bytes (reduction from $19V$)
# 
# Why not use $k=1$?

# # Front encoding
# 
# ![front](files/front.png)
# 
# [MRS](http://nlp.stanford.edu/IR-book/pdf/05comp.pdf)
# 
# Savings depends on chosen prefixes.

# # Compression Results
# 
# ![sizes](files/sizes.png)
# 
# [MRS](http://nlp.stanford.edu/IR-book/pdf/05comp.pdf)
# 
# Note that 28V / 19V $\approx$ 11.2 / 7.6

# In[ ]:



