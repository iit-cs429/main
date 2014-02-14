
# # CS 429: Information Retrieval
# 
# <br>
# 
# ## Lecture 10: Query Expansion
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology 
# ### Spring 2014
# 
# ---

# Last time:
# 
# - Evaluation
#   - accuracy, precision, recall, MAP
#   
# This time:
# 
# - How can we incoporate user feedback to improve search?
# - How can we alter the user's query to improve search?

# # Relevance Feedback
# 
# - An *interactive* IR system in which 
# 
# 
# 1. The user enters a query.
# 2. The system returns results.
# 3. The user indicates which results are relevant.
# 4. GoTo 2.

# # How should we incorporate user feedback?

# - Create a new query that is similar to relevant documents but dissimilar to irrelevant documents.

# # Rocchio
# 
# $ \DeclareMathOperator*{\argmax}{arg\,max}$
# $\vec{q}^* \leftarrow \argmax_{\vec{q}} sim(\vec{q}, C_r) - sim(\vec{q}, C_{nr})$
# 
# - where $q$ is a query
# - $C_r$ is a set of relevant documents
# - $C_{nr}$ is a set of irrelevant documents
# - $sim$ is cosine similarity

# # Document Centroid
# 
# Recall that we represent each document as a vector of tf-idf values.
# 
# Given a collection of documents $D = \{d_1 \ldots d_N\}$, the centroid vector is:
# 
# $ \frac{1}{N} \sum_{\vec{d_j} \in D}\vec{d}_j $

# In[157]:

get_ipython().magic(u'pylab inline')
import numpy as np

points = [[1, 4],
          [.5, .5],
          [4, 6]]

centroid = np.sum(points, axis=0) / len(points)
scatter([p[0] for p in points], [p[1] for p in points])
scatter([centroid[0]], [centroid[1]], marker='x', s=60)


# Out[157]:

#     Populating the interactive namespace from numpy and matplotlib
# 

#     <matplotlib.collections.PathCollection at 0x10f690dd0>

# image file:

# Want a query that is closest to relevant documents, but far from irrelevant documents.
# 
# $\vec{q}^* = \frac{1}{|C_r|} \sum_{\vec{d_j} \in C_r}\vec{d}_j - \frac{1}{|C_{nr}|} \sum_{\vec{d}_j \in C_{nr}} \vec{d}_j$

# ![rocchio](files/rocchio.png)
# 
# Source: [MRS](http://nlp.stanford.edu/IR-book/pdf/09expand.pdf)

# But, we don't know the set of all relevant and irrelevant documents.
# 
# 
# $\vec{q}_m = \alpha \vec{q}_0 + \beta\frac{1}{D_r} \sum_{\vec{d}_j \in D_r} \vec{d}_j - \gamma\frac{1}{|D_{nr}|} \sum_{\vec{d_j} \in D_{nr}} \vec{d}_j$
# 
# - $\vec{q}_0$ is original query vector
# - $\alpha$, $\beta$, $\gamma$ are tunable parameters.
# 

# In[162]:

# Plot effect of relevance feedback as we change parameters.
import numpy as np
from numpy import array as npa
import random as rnd

def centroid(docs):
    return np.sum(docs, axis=0) / len(docs)

def rocchio(query, relevant, irrelevant, alpha, beta, gamma):
    return alpha * query + beta * centroid(relevant) - gamma * centroid(irrelevant) 

# Create some documents
relevant = npa([[1, 5], [1.1, 5.1], [0.9, 4.9], [1.0, 4.8]])
irrelevant = npa([[rnd.random()*6, rnd.random()*6] for i in range(30)])

# Create a query
query = npa([.1, .1])

# Compute two different Rocchio updates (beta=0.5, beta=0)
new_query_b5 = rocchio(query, relevant, irrelevant, 1., .75, .5)
new_query_b0 = rocchio(query, relevant, irrelevant, 1., .75, 0.)

# Plot them.
pos = scatter([p[0] for p in relevant], [p[1] for p in relevant])
neg = scatter([p[0] for p in irrelevant], [p[1] for p in irrelevant], marker='+', edgecolor='red')
q = scatter(query[0], query[1], marker='v', c=0.1, s=100)
newq_b5 = scatter([new_query_b5[0]], [new_query_b5[1]], marker='*', s=100, c=.9)
newq_b0 = scatter([new_query_b0[0]], [new_query_b0[1]], marker='d', s=100, c=.8)
plt.legend((pos, neg, q, newq_b5, newq_b0),
           ('relevant', 'irrelevant', 'query', 'beta=.5', 'beta=0'),
           scatterpoints=1,
           loc='lower right',
           ncol=3,
           fontsize=9)


# Out[162]:

#     <matplotlib.legend.Legend at 0x10dc936d0>

# image file:

# - $\gamma=0$ Often used, since we're more confident in relevant annotations than irrelevant.

# - One might decrease $\alpha$ as the number of relevant documents increase.

# # Does relevance feedback help precision or recall?

# - Mostly recall: "adding" similar terms to query vector from relevant documents.
# 
# - When would it not help?

# - Spelling correction?
# - Different language?
# - Synonyms?
# 
# 
# - Assumption 1: query is "close" to relevant documents
#   - feedback makes the query closer
#   
# - Assumption 2: relevant documents form one cluster.

# In[163]:

# What happens if there are two clusters of relevant examples?

import numpy as np
import random as rnd

points = [[1, 5], [1.1, 5.1], [0.9, 4.9], [1.0, 4.8],
          [5, 1.2], [4.9, 1.1], [5.1, 1.0], [4.8,1.2]]

centroid = np.sum(points, axis=0) / len(points)
pos = scatter([p[0] for p in points], [p[1] for p in points])
neg = scatter([rnd.random()*6 for i in range(30)], [rnd.random() * 6 for i in range(30)], marker='+', edgecolor='red')
centroid = scatter([centroid[0]], [centroid[1]], marker='x', s=100, edgecolor='green')
plt.legend((pos, neg, centroid),
           ('relevant', 'irrelevant', 'centroid'),
           scatterpoints=1,
           loc='lower left',
           ncol=3,
           fontsize=8)


# Out[163]:

#     <matplotlib.legend.Legend at 0x10f7ec950>

# image file:

# # Does relevance feedback affect search time?

# - Much longer queries
# - How to approximate?
#   - Use top $k$ most informative terms from relevant set.

# # Variants of relevance feedback
# 
# - Pseudo-relevance: Assume top $k$ documents are relevant.
# - Indirect relevance: Mine click logs.

# # Pseudo-relevance feedback
# 
# 1. Rank documents
# 2. Let $V$ be the top $k$ documents. We pretend these are all relevant.
# 3. Update $q$ according to Rocchio
# 
# We can iterate steps $2-4$ until ranking stops changing.
# 
# When would this work? When would this not work?

# # Explicit query expansion
# 
# - Thesaurus
# - Word co-occurrences
# - Mine reformulations from query log

# # WordNet
# 
# <http://wordnetweb.princeton.edu/perl/webwn>

# # Thesaurus discovery
# 
# **Idea:** Look for words that occur in same context.
# 
# - "He put the mug on the \_\_\_\_\_"

# In[164]:

from collections import Counter, defaultdict
from sklearn.datasets import fetch_20newsgroups
import re
docs = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'),
                          categories=['comp.graphics', 'comp.sys.mac.hardware', 'comp.sys.ibm.pc.hardware',
                                      'comp.os.ms-windows.misc']).data

# Count words that occur within a window of -n to +n of each word.
def term2contexts(docs, n):
    contexts = defaultdict(lambda: Counter())
    for d in docs:
        toks = re.findall('[\w]+', d.lower())
        for i in range(len(toks)):
            contexts[toks[i]].update(toks[i-n:i] + toks[i+1:i+n+1])
    return contexts

contexts = term2contexts(docs, 1)
print contexts['email']


# Out[164]:

#     Counter({u'please': 31, u'me': 26, u'or': 21, u'to': 18, u'via': 15, u'address': 14, u'by': 13, u'and': 10, u'as': 7, u'send': 6, u'the': 6, u'addresses': 5, u'it': 5, u'if': 5, u'i': 5, u'replies': 4, u's': 4, u'thanks': 3, u'an': 3, u'sp': 3, u'at': 3, u'also': 2, u'your': 2, u'responses': 2, u'my': 2, u'with': 2, u'can': 2, u'have': 2, u'any': 2, u'you': 2, u'response': 2, u'request': 2, u'time': 2, u'canberra': 1, u'soon': 1, u'03051': 1, u'through': 1, u'edu': 1, u'anyoneand': 1, u'query': 1, u'mikael_fredriksson': 1, u'whose': 1, u'vatti': 1, u'mail': 1, u'weeks': 1, u'7197': 1, u'karlth': 1, u'fax': 1, u'his': 1, u'means': 1, u'very': 1, u'utah': 1, u'possible': 1, u'87131': 1, u'whichever': 1, u'every': 1, u'not': 1, u'advanced': 1, u'server': 1, u'try': 1, u'9570': 1, u'2393': 1, u'x': 1, u'tp923021': 1, u'gmbh': 1, u'schaefer': 1, u'gloege': 1, u'id': 1, u'80': 1, u'robert': 1, u'thank': 1, u'current': 1, u'enough': 1, u'reply': 1, u'khoros': 1, u'available': 1, u'ken': 1, u'we': 1, u'hansch': 1, u'300': 1, u'sole': 1, u'1933': 1, u'joe': 1, u'haston': 1, u'care': 1, u'advance': 1, u'c': 1, u'limits': 1, u'could': 1, u'etc': 1, u'corrections': 1, u'rodney': 1, u'com': 1, u'facility': 1, u'imagine': 1, u'prefer': 1, u'fredriksson': 1, u'directly': 1, u'johne': 1, u'7795966': 1, u'there': 1, u'2': 1, u'leehian': 1, u'that': 1, u'happily': 1, u'but': 1, u'capabilities': 1, u'ma': 1, u'submissions': 1, u'ihno': 1, u'growing': 1, u'similar': 1, u'6695': 1, u'508336': 1, u'documentation': 1, u'is': 1, u'good': 1, u'something': 1, u'in': 1, u'mouse': 1, u'karl': 1, u'information': 1, u'no': 1, u'get': 1, u'when': 1, u'd2002': 1, u'1': 1, u'tim': 1, u'valid': 1, u'wes1574': 1, u'faxes': 1, u'singapore': 1, u'66s': 1, u'dicta93': 1, u'after': 1, u'wnkretz': 1, u'annee': 1, u'a': 1, u'markus': 1, u'marchesf': 1, u'contact': 1, u'corporate': 1})
# 

# In[165]:

import math
# Compute inverse document frequency values for each term.
def compute_idfs(docs):
    idfs = Counter()
    for d in docs:
        toks = set(re.findall('[\w]+', d.lower()))
        idfs.update(toks)
    for d in dfs:
        idfs[d] = math.log(1.0 * len(docs) / idfs[d])
    return idfs

idfs = compute_idfs(docs)
print 'idf of the=', idfs['the'], ' of monitor=', idfs['monitor']


# Out[165]:

#     idf of the= 0.207475223156  of monitor= 2.86134763856
# 

# In[166]:

def cosine(term1, term2):
    context1 = contexts[term1]
    context2 = contexts[term2]
    sim = sum(idfs[term] * context1[term] * context2[term] for term in context1)
    return 1.0 * sim / (sum(context1.values()) + sum(context2.values()))

def find_closest_term(term, contexts):
    context1 = contexts[term]
    cosines = [(term2, cosine(term, term2)) for term2 in contexts]
    return sorted(cosines, key=lambda x: x[1], reverse=True)

print '\n'.join('%s  %.2f' % (w, v) for w, v in find_closest_term('email', contexts)[:10])


# Out[166]:

#     email  9.18
#     tell  6.66
#     let  6.53
#     reply  6.18
#     send  5.26
#     mail  4.70
#     help  4.38
#     give  3.86
#     respond  3.24
#     post  2.83
# 

# Google's $n$-gram data: 
# 
# <http://googleresearch.blogspot.com/2006/08/all-our-n-gram-are-belong-to-you.html>

# # How do we decide when to expand the query?

# - Few results returned.
# - Query log data
#   - Searches where few results are clicked.
