
# # CS 429: Information Retrieval
# <br>
# 
# ## Lecture 14: Language Models, Part II
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology
# ### Spring 2014

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

# In[2]:

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


# Out[2]:

#     Jesse Doe 
#     Mrs. Jesse Jones 
#     Dr. Jane Doe 
#     Jesse Jones 
#     Ms. Jane Jones 
#     Jane Doe 
#     Mr. Jesse Jones 
#     Jesse Doe 
#     Mr. John Smith 
#     Jesse Jones 
#     Jesse Smith 
#     Dr. Jesse Jones 
#     Jesse Smith 
#     Jane Smith 
#     Ms. Jesse Smith 
#     Mr. John Doe 
#     Dr. John Doe 
#     Mrs. John Smith 
#     Dr. Jane Doe Sr. 
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

# In[3]:

from collections import Counter

def doc2model(doc):
    """ Convert a document d into a language model M_d. """
    counts = Counter(doc)
    for term in counts:
        counts[term] /= 1. * len(doc)
    return counts

m_d = doc2model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'])
print m_d


# Out[3]:

#     Counter({'the': 0.2, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1})
# 

# In[4]:

import numpy as np

def sample_from_model(m_d, length):
    """ Sample length words from language model m_d. """
    counts = np.random.multinomial(length, m_d.values(), size=1)[0]
    words = []
    for i, count in enumerate(counts):
        words.extend(count * [m_d.keys()[i]])
    return words
    
print sample_from_model(m_d, 10)


# Out[4]:

#     ['united', 'united', 'united', 'united', 'states', 'won', 'nine', 'nine', 'the', 'medals']
# 

# In[5]:

def pr_q_given_m(q, m_d):
    """ Compute P(q|M_d), the probability of language model M_d generating query q. """
    product = 1.
    for qi in q:
        product *= m_d[qi]
    return product

print 'Pr([the, olympics] | d)=', pr_q_given_m(['the', 'olympics'], m_d)
print 'Pr([united, states] | d)=', pr_q_given_m(['united', 'states'], m_d)
print 'Pr([olympics, united, states] | d)=', pr_q_given_m(['olympics', 'united', 'states'], m_d)
    


# Out[5]:

#     Pr([the, olympics] | d)= 0.02
#     Pr([united, states] | d)= 0.01
#     Pr([olympics, united, states] | d)= 0.001
# 

# In[6]:

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


# Out[6]:

#     m_d2: Counter({'states won': 0.1111111111111111, 'won nine': 0.1111111111111111, 'the olympics': 0.1111111111111111, 'united states': 0.1111111111111111, 'gold medals': 0.1111111111111111, 'the united': 0.1111111111111111, 'medals in': 0.1111111111111111, 'in the': 0.1111111111111111, 'nine gold': 0.1111111111111111})
#     
#     m_d3 Counter({'in the': 0.16666666666666666, 'states won': 0.08333333333333333, 'the slalom': 0.08333333333333333, 'won nine': 0.08333333333333333, 'the olympics': 0.08333333333333333, 'united states': 0.08333333333333333, 'gold medals': 0.08333333333333333, 'the united': 0.08333333333333333, 'medals in': 0.08333333333333333, 'nine gold': 0.08333333333333333, 'slalom in': 0.08333333333333333})
# 

# In[7]:

sample_from_model(m_d3, 10)


# Out[7]:

#     ['states won',
#      'states won',
#      'the slalom',
#      'the slalom',
#      'won nine',
#      'the olympics',
#      'the olympics',
#      'the united',
#      'medals in',
#      'in the']

# In[8]:

m_d4 = doc2ngram_model(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 4)
sample_from_model(m_d4, 10)


# Out[8]:

#     ['nine gold medals in',
#      'nine gold medals in',
#      'won nine gold medals',
#      'the united states won',
#      'medals in the olympics',
#      'states won nine gold',
#      'states won nine gold',
#      'states won nine gold',
#      'united states won nine',
#      'united states won nine']

# **Why not just set $n=10000$?**

# In[9]:

# 4-gram model:
print 'Pr([the olympics] | m_d4)=', pr_q_given_m(['the olympics'], m_d4)


# Out[9]:

#     Pr([the olympics] | m_d4)= 0.0
# 

# In[10]:

# 2-gram model
print 'Pr([the olympics] | m_d2)=', pr_q_given_m(['the olympics'], m_d2)


# Out[10]:

#     Pr([the olympics] | m_d2)= 0.111111111111
# 

# In[11]:

# Even for unigram model
print 'Pr([the, olympics, zebra] | m_d)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d)


# Out[11]:

#     Pr([the, olympics, zebra] | m_d)= 0.0
# 

# If a query does not appear in document $d$, then $P(q|M_d)=0$.
# 
# 
# - Want to allow some chance that a word not in $d$ will appear.

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

# In[18]:

def doc2model_smooth(doc, smooth_term, vocab):
    """ Convert a document d into a language model M_d. """
    counts = Counter(doc)
    for term in vocab:
        counts[term] = (counts[term] + smooth_term) / (1. * len(doc) + smooth_term * len(vocab))
    return counts

vocab = ['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'olympics', 'zebra', 'a']
m_d_smooth1 = doc2model_smooth(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 1, vocab)
m_d_smooth10 = doc2model_smooth(['the', 'united', 'states', 'won', 'nine', 'gold', 'medals', 'in', 'the', 'olympics'], 10, vocab)
print 'unsmoothed model:', m_d
print '\nsmoothed model1:', m_d_smooth1
print '\nsmoothed model10:', m_d_smooth10


# Out[18]:

#     unsmoothed model: Counter({'the': 0.2, 'united': 0.1, 'gold': 0.1, 'states': 0.1, 'won': 0.1, 'nine': 0.1, 'in': 0.1, 'olympics': 0.1, 'medals': 0.1})
#     
#     smoothed model1: Counter({'the': 0.14285714285714285, 'united': 0.09523809523809523, 'gold': 0.09523809523809523, 'states': 0.09523809523809523, 'won': 0.09523809523809523, 'nine': 0.09523809523809523, 'in': 0.09523809523809523, 'olympics': 0.09523809523809523, 'medals': 0.09523809523809523, 'a': 0.047619047619047616, 'zebra': 0.047619047619047616})
#     
#     smoothed model10: Counter({'the': 0.1, 'united': 0.09166666666666666, 'gold': 0.09166666666666666, 'states': 0.09166666666666666, 'won': 0.09166666666666666, 'nine': 0.09166666666666666, 'in': 0.09166666666666666, 'olympics': 0.09166666666666666, 'medals': 0.09166666666666666, 'a': 0.08333333333333333, 'zebra': 0.08333333333333333})
# 

# In[19]:

print 'Pr([the, olympics, zebra] | m_d_smooth1)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d_smooth1)
print 'Pr([the, olympics, zebra] | m_d_smooth10)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d_smooth10)


# Out[19]:

#     Pr([the, olympics, zebra] | m_d_smooth1)= 0.000647878198899
#     Pr([the, olympics, zebra] | m_d_smooth10)= 0.000763888888889
# 

# **Problem with Laplace smoothing:**
# 
# - Assumes that all unseen words are equally likely.
#   - Effectively adds $\epsilon$ occurrences to every document. 

# In[21]:

print 'Pr([the, olympics, zebra] | m_d_smooth10)=', pr_q_given_m(['the', 'olympics', 'zebra'], m_d_smooth10)
print 'Pr([the, olympics, a] | m_d_smooth10)=', pr_q_given_m(['the', 'olympics', 'a'], m_d_smooth10)


# Out[21]:

#     Pr([the, olympics, zebra] | m_d_smooth10)= 0.000763888888889
#     Pr([the, olympics, a] | m_d_smooth10)= 0.000763888888889
# 

# - $d_1:$ the, cat
# - $d_2:$ dog, cat
# 
# 
# - $q:$ dog, the
# 
# Should return $d_2$.
# 

# But, Laplace smoothing means missing the word "dog" is just as bad as missing the word "the".
# 
# 
# $\begin{align} P_{smooth}(q|M_d) = \prod_{t \in q} P(t|M_d) = \prod_{t \in q} \frac{tf_{t, d} + \epsilon}{L_d + V\epsilon} \end{align}$
# 
# $\begin{align} P_{smooth}(q|M_{d_1}) = P(dog|M_{d_1}) * P(the|M_{d_1}) = \frac{\epsilon}{2 + V\epsilon} * \frac{1 + \epsilon}{2 + V\epsilon} \end{align}$
# 
# $\begin{align} P_{smooth}(q|M_{d_2}) = P(dog|M_{d_2}) * P(the|M_{d_2}) = \frac{1 + \epsilon}{2 + V\epsilon} * \frac{\epsilon}{2 + V\epsilon} \end{align}$

# # Smoothing with collection frequency
# 
# Let $cf_t$ be the collection frequency of term $t$
# 
# - That is, the total number of times it occurs (as opposed to $df_t$).

# Then if term $t$ does not appear in document $d$. 
# 
# - We want $P(t|M_d) < \frac{cf_t}{T}$
# - $T=$ total number of tokens in all documents.

# Let $M_c$ be the language model for the entire document collection:
# 
# 
# $\begin{align} P(t|M_c) = \frac{cf_{t}}{T} \end{align}$

# # Dirichlet Smoothing
# 
# 
# $\begin{align} P_{dir}(t|M_d) = \frac{tf_{t, d} + \alpha P(t|M_c)}{L_d + \alpha} \end{align}$
# 
# - $\alpha:$ tunable parameter
# - Larger $\alpha \rightarrow$ more smoothing.

# # Interpolation Smoothing
# 
# Alternatively, we can *interpolate* between the document probability and the collection probability:
# 
# $\begin{align}P_{interp}(t|M_d) & = & \lambda P(t|M_d) + (1-\lambda) P(t|M_c)\\
# & = & \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T} 
# \end{align}$
# 
# - $\lambda$ is a tunable parameter.
# - Smaller $\lambda \rightarrow$ more smoothing.
# - This is also called *Jelinek-Mercer* smoothing.

# Thus, the new query likelihood is:
# 
# 
# $\begin{align} P_{interp}(q|M_d) = \prod_{t \in q} P_{interp}(t|M_d) = \prod_{t \in q} \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T}  \end{align}$

# # Interpolation Example
# 
# (from [MRS](http://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf) p. 246)
# 
# - $d_1:$ Xyzzy reports a proﬁt but revenue is down
# - $d_2:$ Quorus narrows quarter loss but revenue decreases further
# - $\lambda=.5$
# 
# Suppose the query is **revenue down**. Then:
# 
# $P_{interp}(q|d_1) = $
# 
# $P_{interp}(q|d_2) = $
# 
# $\begin{align}P_{interp}(t|M_d) & = & \lambda P(t|M_d) + (1-\lambda) P(t|M_c)\\
# & = & \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T} 
# \end{align}$
# 

# # Interpolation Example
# 
# (from [MRS](http://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf) p. 246)
# 
# - $d_1:$ Xyzzy reports a proﬁt but revenue is down
# - $d_2:$ Quorus narrows quarter loss but revenue decreases further
# - $\lambda=.5$
# 
# Suppose the query is revenue down. Then:
# 
# $P_{interp}(q|d_1) = [(1/8 + 2/16)/2] * [(1/8 + 1/16)/2] = 1/8 * 3/32 = 3/256$
# 
# $P_{interp}(q|d_2) = [(1/8 + 2/16)/2] * [(0/8 + 1/16)/2] = 1/8 * 1/32 = 1/256$
# 

# Where are the following quantities used, if at all?
# 
# 
# - Term frequency in a document
# - Collection frequency of a term
# - Document frequency of a term
# - Length normalization of a term
# 
# 
# $\begin{align} P_{interp}(q|M_d) = \prod_{t \in q} P_{interp}(t|M_d) = \prod_{t \in q} \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T}  \end{align}$

# **Should amount of smoothing ($\lambda)$ depend on query length?**

# ![qlength](files/qlength.png)
# 
# Source: [Zhai & Lafferty, 2004](http://galton.uchicago.edu/~lafferty/pdf/smooth-tois.pdf)

# # Language Model vs. tf-idf
# 
# ![lmvstfidf](files/lmvstfidf.png)
# 
# Source: [MRS](http://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf)
# 
# 
# 
# $\begin{align} P_{interp}(q|M_d) = \prod_{t \in q} P_{interp}(t|M_d) = \prod_{t \in q} \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T}  \end{align}$
# 
# vs.
# 
# $ S_{tfidf}(q, d) = \sum_{t \in q} \begin{align} (1 + \log(tf_{t, d})) * \log(\frac{N}{df_t}) \end{align}$

# <table>
# <tr><td>docID</td> <td>Document text</td></tr>
# <tr> <td>1</td> <td>click go the shears boys click click click</td> </tr>
# <tr> <td>2</td> <td>click click</td></tr>
# <tr> <td>3</td> <td>metal here</td></tr>
# <tr> <td>4</td> <td>metal shears click here</td></tr>
# </table>
# 
# <table>
# <tr><td>Query</td> <td>Doc 1</td> <td>Doc 2</td> <td>Doc 3</td> <td>Doc 4</td></tr>
# <tr><td>click</td><td> </td><td> </td><td> </td><td> </td></tr>
# <tr><td>shears</td><td> </td><td> </td><td> </td><td> </td></tr>
# <tr><td>click shears</td><td> </td><td> </td><td> </td><td> </td></tr>
# </table>
# 
# Let $\lambda=0.5$.
# 
# $\begin{align} P_{interp}(q|M_d) = \prod_{t \in q} P_{interp}(t|M_d) = \prod_{t \in q} \lambda \frac{tf_{t, d}}{L_d} + (1-\lambda) \frac{cf_{t}}{T}  \end{align}$
# 
# (Source: [MRS](http://nlp.stanford.edu/IR-book/pdf/12lmodel.pdf))
