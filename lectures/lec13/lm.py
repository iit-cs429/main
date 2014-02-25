
# # CS 429: Information Retrieval
# <br>
# 
# ## Lecture 13: Language Models, Part I
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology
# ### Spring 2014

# # Last week...
# 
# We ranked documents by: 
# 
# $P(R=1|d, q)$
# 
# where $R=1$ means document $d$ is relevant to query $q$.
# 
# **Problem:** hard to estimate this value without $d,q$ pairs labeled with relevance.

# # Language Models
# 
# **Idea:**
# 
# Rank documents by:
# 
# $P(q|d)$
# 
# The probability that the process that generated $d$ would also generate $q$.
# 
# No variable for relevance.

# # Generative models
# - Each document is a list of strings from a language.
# - Consider all the possible documents the author could have written
#   - How many of them would contain the term "zebra"?
# - Consider the query $q$
#   - What is the probability that the author of document $d$ would have written down $q$?
#   - $P(q|M_d)$

# # Finite State Machine
# 
# Let a *language* $L$ be a set of documents $\{d_1 \ldots d_n\}$.
# 
# A finite-state machine $M_L$ accepts a document $d$ as input and outputs "yes" if $d \in L$; otherwise it outputs "no."
# 
# $M_L$ consists of:
# 
# - a set of **states** $S = \{s_1 \ldots s_m\}$
# - an input **vocabulary** $V$, a finite set of acceptable terms
# - a **transition function** $\delta : V \times S \mapsto S$ 
#   - When in state $s_i$, if term $w \in V$ is read, the state changes to $s_j$

# <img src="files/fsm.png" width="50%"/>
# 
# 
# - <font color="green">Mr. John Smith Jr.</font> &nbsp;&nbsp; start $\rightarrow$ prefix $\xrightarrow{Mr.}$ first $\xrightarrow{John}$ last $\xrightarrow{Smith}$ suffix $\xrightarrow{Jr.}$ accept
# - <font color="green">Jane Doe</font>
# - <font color="red">Mr. Jr.</font>

# # Weighted Finite State Machine
# 
# <img src="files/wfsm.png" width="50%"/>
# 
# 
# - $P($<font color="green">Mr. John Smith Jr.</font>$)= 0.4 * 1.0 * 1.0 * .05 * 1.0 = 0.02$ 
# - $P($<font color="green">Jane Doe</font>$) = 0.6 * 1.0 * 0.95 = 0.57$
# - $P($<font color="red">Mr. Jr.</font>$) = 0.0$

# # Generative Model
# 
# Rather than simply assigning probabilities to documents, we can use a weighted finite state machine to **generate** documents.

# In[103]:

# Generate names.
# Assume all words are equally likely, but state transitions follow previous FSM.

prefixes = ['Mr. ', 'Ms. ', 'Mrs. ', 'Dr. ']
firsts = ['John ', 'Jane ', 'Jesse ']
lasts = ['Smith ', 'Jones ', 'Doe ']
suffixes = ['Jr. ', 'Sr. ', 'III ']

def sample(alist):
    """ Sample an element of a list. """
    return alist[random.randint(0, len(alist) - 1)]

import random
num_documents = 20
for i in range(num_documents):
    doc = ''
    if random.random() <= 0.4:  # prefix
        doc += sample(prefixes)
    doc += sample(firsts) + sample(lasts)
    if random.random() <= .05:  # suffix
        doc += sample(suffixes)
    print doc


# Out[103]:

#     Mrs. John Jones 
#     Ms. Jesse Jones 
#     Jane Jones 
#     Jane Jones 
#     John Doe 
#     Jane Doe 
#     Mrs. Jesse Jones 
#     John Smith 
#     Mr. John Smith 
#     Dr. Jesse Jones 
#     John Doe 
#     Mr. Jane Smith 
#     Jesse Doe 
#     Jesse Doe 
#     Ms. John Jones 
#     Jane Doe 
#     Jesse Jones 
#     Jesse Doe 
#     Jesse Jones 
#     Jesse Jones 
# 

# # Language Model
# 
# A weighted finite state machine that can
# 
# - generate documents
# - generate queries
# - assign probabilities to documents/queries
# 
# 
# **Idea:**
# 
# - Construct a language model $M_d$ for each document $d$.
# - For each query $q$, compute the probability that $M_d$ generated $q$: $P(q|M_d)$
# - Rank documents by $P(q|M_d)$.

# <img src="files/lm2.png" width="50%"/>
# 
# **How can we construct a language model from a document?**

# Long history in natural language processing:
# 
# - parse trees
# 
# ![parse](files/parse.jpg)
# 
# Source: [Wikipedia](http://en.wikipedia.org/wiki/Parse_tree)
# 
# - [sentence generators](http://writing-program.uchicago.edu/toys/randomsentence/)
# 

# But, grammar has little effect on information retrieval.
# 
# - queries are rarely grammatical

# # Unigram Language Models
# 
# - Ignore word order.
# - Generate each word independently.

# $\begin{align} P(q|M_d) = \prod_{t \in q} P(t|M_d) = \prod_{t \in q} \frac{tf_{t, d}}{L_d} \end{align}$
# 
# - $q:$ query consisting of terms $t$
# - $M_d:$ language model for document $d$
# - $tf_{t, d}:$ frequency of term $t$ in document $d$
# - $L_d:$ number of tokens in $d$

# # Unigram Language Models
# 
# <img src="files/uni.png" width="50%"/>

# In[104]:

from collections import Counter

def doc2model(doc):
    """ Convert a document d into a language model M_d. """
    counts = Counter(doc)
    for term in counts:
        counts[term] /= 1. * len(doc)
    return counts

m_d = doc2model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'])
print m_d


# Out[104]:

#     Counter({'the': 0.2, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1})
# 

# In[105]:

import numpy as np

def sample_from_model(m_d, length):
    """ Sample length words from language model m_d. """
    counts = np.random.multinomial(length, m_d.values(), size=1)[0]
    words = []
    for i, count in enumerate(counts):
        words.extend(count * [m_d.keys()[i]])
    return words
    
print sample_from_model(m_d, 10)


# Out[105]:

#     ['united', 'united', 'gold', 'states', 'in', 'in', 'olympics', 'olympics', 'the', 'the']
# 

# In[106]:

def pr_q_given_m(q, m_d):
    """ Compute P(q|M_d), the probability of language model M_d generating query q. """
    product = 1.
    for qi in q:
        product *= m_d[qi]
    return product

print 'Pr([the, olympics] | d)=', pr_q_given_m(['the', 'olympics'], m_d)
print 'Pr([united, states] | d)=', pr_q_given_m(['united', 'states'], m_d)
print 'Pr([olympics, united, states] | d)=', pr_q_given_m(['olympics', 'united', 'states'], m_d)
    


# Out[106]:

#     Pr([the, olympics] | d)= 0.02
#     Pr([united, states] | d)= 0.01
#     Pr([olympics, united, states] | d)= 0.001
# 

# In[107]:

def doc2ngram_model(doc, n):
    """ Convert a document d into a language model M_d. """
    counts = Counter()
    for i in range(len(doc) - 1):
        counts.update([' '.join(doc[i:i+n]) for i in range(len(doc) - n + 1)])
    length = sum(counts.values())
    for term in counts:
        counts[term] /= 1. * length
    return counts

m_d2 = doc2ngram_model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 2)
m_d3 = doc2ngram_model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'slalom', 'in', 'the', 'olympics'], 2)

print 'm_d2:', m_d2

print '\nm_d3', m_d3


# Out[107]:

#     m_d2: Counter({'states won': 0.1111111111111111, 'won nine': 0.1111111111111111, 'the olympics': 0.1111111111111111, 'united states': 0.1111111111111111, 'gold medals': 0.1111111111111111, 'the united': 0.1111111111111111, 'medals in': 0.1111111111111111, 'in the': 0.1111111111111111, 'nine gold': 0.1111111111111111})
#     
#     m_d3 Counter({'in the': 0.16666666666666666, 'states won': 0.08333333333333333, 'the slalom': 0.08333333333333333, 'won nine': 0.08333333333333333, 'the olympics': 0.08333333333333333, 'united states': 0.08333333333333333, 'gold medals': 0.08333333333333333, 'the united': 0.08333333333333333, 'medals in': 0.08333333333333333, 'nine gold': 0.08333333333333333, 'slalom in': 0.08333333333333333})
# 

# In[108]:

sample_from_model(m_d3, 10)


# Out[108]:

#     ['the slalom',
#      'won nine',
#      'the olympics',
#      'the olympics',
#      'the olympics',
#      'the united',
#      'the united',
#      'in the',
#      'nine gold',
#      'slalom in']

# In[109]:

m_d4 = doc2ngram_model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 4)
sample_from_model(m_d4, 10)


# Out[109]:

#     ['nine gold medals in',
#      'gold medals in the',
#      'won nine gold medals',
#      'the united states won',
#      'the united states won',
#      'medals in the olympics',
#      'states won nine gold',
#      'states won nine gold',
#      'united states won nine',
#      'united states won nine']

# **Why not just set $n=10000$?**

# In[110]:

# 4-gram model:
print 'Pr([the olympics] | m_d4)=', pr_q_given_m(['the olympics'], m_d4)


# Out[110]:

#     Pr([the olympics] | m_d4)= 0.0
# 

# In[111]:

# 2-gram model
print 'Pr([the olympics] | m_d2)=', pr_q_given_m(['the olympics'], m_d2)


# Out[111]:

#     Pr([the olympics] | m_d2)= 0.111111111111
# 

# In[112]:

# Even for unigram model
print 'Pr([the, olympics, zebra] | m_d)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d)


# Out[112]:

#     Pr([the, olympics, zebra] | m_d)= 0.0
# 

# If a query does not appear in document $d$, then $P(q|M_d)=0$.
# 
# 
# - Want to allow some chance that a word not in $d$ will appear.

# In[115]:

def doc2model_smooth(doc, smooth_term, vocab):
    """ Convert a document d into a language model M_d. """
    counts = Counter(doc)
    for term in vocab:
        counts[term] = (counts[term] + smooth_term) / (1. * len(doc) + smooth_term * len(vocab))
    return counts

vocab = ['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'olympics', 'zebra']
m_d_smooth1 = doc2model_smooth(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 1, vocab)
m_d_smooth10 = doc2model_smooth(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 10, vocab)
print 'unsmoothed model:', m_d
print '\nsmoothed model1:', m_d_smooth1
print '\nsmoothed model10:', m_d_smooth10


# Out[115]:

#     unsmoothed model: Counter({'the': 0.2, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1})
#     
#     smoothed model1: Counter({'the': 0.15, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1, 'zebra': 0.05})
#     
#     smoothed model10: Counter({'the': 0.10909090909090909, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1, 'zebra': 0.09090909090909091})
# 

# In[114]:

print 'Pr([the, olympics, zebra] | m_d_smooth1)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d_smooth1)
print 'Pr([the, olympics, zebra] | m_d_smooth10)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d_smooth10)


# Out[114]:

#     Pr([the, olympics, zebra] | m_d_smooth1)= 0.00075
#     Pr([the, olympics, zebra] | m_d_smooth10)= 0.00099173553719
# 

# # Smoothed Language Model
# 
# (Laplace smoothing)
# 
# $\begin{align} P_{smooth}(q|M_d) = \prod_{t \in q} P(t|M_d) = \prod_{t \in q} \frac{tf_{t, d} + \epsilon}{L_d + V\epsilon} \end{align}$
# 
# - $q:$ query consisting of terms $t$
# - $M_d:$ language model for document $d$
# - $tf_{t, d}:$ frequency of term $t$ in document $d$
# - $L_d:$ number of tokens in $d$
# - $\epsilon:$ amount to smooth
# - $V$: vocabulary size
