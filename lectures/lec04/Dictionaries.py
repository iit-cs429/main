
# # CS 429: Information Retrieval
# 
# <br>
# 
# ## Lecture 4: Dictionaries
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
# - skip lists, phrase search, biword index, positional index
# 
# Today:
# 
# - Efficient retrieval of postings lists
# - Wildcard queries
# - Spelling correction

# Recall our friend the inverted index:
# 
# \begin{eqnarray*}
# cat & \rightarrow &1,9,62   \\
# dog & \rightarrow &1,2,9,31 \\
# zebra & \rightarrow &2,62,150   \\
# \end{eqnarray*}

# Given a query term "dog", how can we efficiently retrieve the matching postings list? 
# 
# **dictionary:** data structure to lookup posting list of a term.
# 
# What data structure should we use?

# - Hash table
# - Binary tree
# - B-tree

# # Hash Table
# 

# In[134]:

index = {'cat': [1, 9, 62],
         'dog': [1, 2, 9, 31],
         'zebra': [2, 62, 150]}


# In[135]:

query = 'dog'
print index['dog']  # hash lookup, O(1)


# Out[135]:

#     [1, 2, 9, 31]
# 

# How does this work?

# In[150]:

print hash('dog')
print hash('cat')
# See the Python's implementation of hash here: 
# http://stackoverflow.com/questions/2070276/where-can-i-find-source-or-algorithm-of-pythons-hash-function


# Out[150]:

#     -1925086808205474835
#     -799031295820617361
# 

# In[151]:

# What happens when two objects return the same hash?
print hash(-799031295820617361)


# Out[151]:

#     -799031295820617361
# 

# ![hashing](files/hashing.png)
# 
# Source: <http://www.laurentluce.com/posts/python-dictionary-implementation/>

# # Hash Table for Inverted Index
# 
# Pros:
# 
# - $O(1)$ lookup time
# - Simple
# 
# Cons:
# 
# - Cannot efficiently find minor variants (e.g., zebr*)

# # Binary Trees
# 
# ![binary](files/binary.png)
# 
# Source: [MRS Ch3](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf)

# # Binary Trees
# 
# Search time: $O(\log n)$
# 
# - Assumes a **balanced** tree

# ![unbalanced](files/unbalanced.png)

# # B-Trees
# 
# Like a binary tree, but nodes can have between *a* and  *b* children, instead of just 2.

# ![btree](files/btree.png)
# 
# B-Tree [2,4]

# # Wildcard queries with B-Trees
# 
# Search for "ana*"
# 
# ![wildcard](files/wildcard.png)

# # Spelling correction
# 
# - $k$-gram overlap
# - Levenshtein
# - Middle-ground

# # Levenshtein distance
# 
# How to convert string1 into string2 with the minimum number of operations?
# 
# fast $\rightarrow$ cats ?

# Operations:
# 
# - *insert*: fas $\xrightarrow{insert(t)}$ fas**t**
# - *delete*: fast $\xrightarrow{delete(t)}$ fas
# - *substitute*: fast $\xrightarrow{substitute(t,x)}$ fas**x**

# cats $\xrightarrow{substitute(c, f)}$ **f**ats $\xrightarrow{insert(s)}$ fa**s**ts $\xrightarrow{delete(s)}$ fast (3 operations)
# 
# or
# 
# cats $\xrightarrow{substitute(c, f)}$ **f**ats $\xrightarrow{substitute(t,s)}$ fa**s**s $\xrightarrow{substitute(s,t)}$ fas**t** (3 operations)
# 
# but definitely not:
# 
# cats $\xrightarrow{insert(f)}$ **f**cats $\xrightarrow{delete(c)}$ fats $\xrightarrow{delete(t)}$ fas $\xrightarrow{delete(s)}$ fa $\xrightarrow{insert(s)}$ fa**s** $\xrightarrow{insert(t)}$ fas**t** (6 operations)

# In[160]:

# Slow, recursive Levenshtein implementation (inspired by <http://en.wikipedia.org/wiki/Levenshtein_distance>)
def leven(s, t):
  # base case: empty strings
  if len(s) == 0:
      return len(t)  # cost of inserting all of t
  if len(t) == 0:
      return len(s)  # cost of inserting all of s
 
  # test if last characters match
  if s[-1] == t[-1]:
      cost = 0    # match; no cost
  else:
      cost = 1   # no match; cost of substituting one letter.
 
  # return minimum of (1) delete char from s, (2) delete char from t, and (3) delete char from both
  return min(leven(s[:-1], t) + 1,           # e.g., leven(fas, cats) + 1 (for deleting 't' from 'fast')
             leven(s, t[:-1]) + 1,           # e.g., leven(fast, cat) + 1 (for deleting 's' from 'cats')
             leven(s[:-1], t[:-1]) + cost);  # e.g., leven(fas, cat) + cost (for substituting 't' for 's')


# In[162]:

print leven('fast', 'cats')


# Out[162]:

#     3
# 

# ![leven](files/leven.png)
# 
# Source: [MRS CH3](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf)

# # Spelling correction with string edit distance
# 
# **Idea:** Find a term in the dictionary that has minimum edit distance to query term
# 

# *Tie-breaker*: term that is most frequent

# In[163]:

# Fetch a list of word counts.

from collections import defaultdict
import requests

# words: list of terms known to be spelled correctly.
word_counts = defaultdict(lambda: 1)  # Assume all words have been seen once
# Fetch list of word frequencies
words = [line.split() for line in requests.get('http://norvig.com/ngrams/count_big.txt').text.splitlines()]
# Add to words
for word, count in words:
    word_counts[word] += int(count)
print 'read', len(words), 'words'
print 'count(a)=', word_counts['a']
print 'count(apple)=', word_counts['apple']
print 'count(ajshdlfkjahdlkjh)=', word_counts['ajshdlfkjahdlkjh']


# Out[163]:

#     read 29136 words
#     count(a)= 21161
#     count(apple)= 12
#     count(ajshdlfkjahdlkjh)= 1
# 

# In[164]:

# Find the element of words that has minimum edit distance to word
# Return word and the distance.
def min_leven(words, word):
    distances = [(w, leven(w, word)) for w in words]
    return min(distances, key=lambda x: x[1])


# In[168]:

print min_leven(['apple', 'banana', 'chair'], 'bannana')


# Out[168]:

#     ('banana', 1)
# 

# In[143]:

# Too slow!
# print min_leven(word_counts.keys(), 'accross')


# # Faster but less precise
# (See <http://norvig.com/spell-correct.html>)
# 
# 70-80% of misspellings are have edit distance of 1
# 
# **Idea:** Efficiently generate all terms that are edit distance of 1 from query term. 
# 
# 

# In[171]:

# Return all single edits to word
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def edits(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]                       # cat-> ca
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]  # cat -> act
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b] # cat -> car
   inserts    = [a + c + b     for a, b in splits for c in alphabet]      # cat -> cats
   return set(deletes + transposes + replaces + inserts)                  # union all edits

print len(edits('cat')), 'edits for cat:', edits('cat')


# Out[171]:

#     182 edits for cat: set(['caqt', 'ucat', 'cdt', 'ctat', 'ciat', 'vcat', 'cvat', 'ycat', 'caht', 'cut', 'jat', 'caty', 'clt', 'hat', 'cyat', 'capt', 'icat', 'zcat', 'fat', 'dat', 'cet', 'caot', 'catz', 'hcat', 'bat', 'crt', 'cayt', 'cakt', 'clat', 'cmt', 'cvt', 'ceat', 'cwat', 'cjat', 'cnat', 'acat', 'cft', 'cabt', 'cnt', 'cajt', 'aat', 'cwt', 'cast', 'czat', 'csat', 'cqat', 'cit', 'cart', 'jcat', 'cfat', 'cazt', 'pcat', 'catd', 'caat', 'cgt', 'ctt', 'cati', 'cait', 'cot', 'cawt', 'xcat', 'cta', 'act', 'ncat', 'cxt', 'ckat', 'calt', 'ca', 'dcat', 'cadt', 'zat', 'cato', 'ct', 'crat', 'cata', 'catb', 'catc', 'tcat', 'cate', 'catf', 'catg', 'cath', 'yat', 'catj', 'catk', 'xat', 'catm', 'catn', 'catl', 'catp', 'ocat', 'catr', 'cats', 'cht', 'catu', 'catv', 'catw', 'catx', 'iat', 'bcat', 'wat', 'catq', 'vat', 'cqt', 'cact', 'cyt', 'rcat', 'gat', 'cant', 'cgat', 'mcat', 'eat', 'kcat', 'caz', 'cay', 'cax', 'cas', 'car', 'caq', 'cap', 'caw', 'cav', 'cau', 'cat', 'cak', 'caj', 'cai', 'cah', 'cao', 'can', 'cam', 'cal', 'cac', 'cab', 'caa', 'cag', 'caf', 'cae', 'cad', 'tat', 'chat', 'fcat', 'caft', 'lcat', 'uat', 'czt', 'rat', 'at', 'cbt', 'catt', 'scat', 'sat', 'qat', 'qcat', 'pat', 'wcat', 'cuat', 'oat', 'nat', 'cst', 'cavt', 'cjt', 'mat', 'cxat', 'caet', 'cmat', 'ccat', 'cagt', 'cpat', 'kat', 'lat', 'gcat', 'caxt', 'cdat', 'coat', 'cct', 'camt', 'ckt', 'caut', 'cpt', 'cbat', 'ecat'])
# 

# How many edits? *n* deletions, *n-1* transpositions, *26n* substitutions, and *26(n+1)* insertions, for a total of *54n+25.*

# In[172]:

get_ipython().magic(u'pylab inline')
plot([54 * x + 25 for x in range(20)])


# Out[172]:

#     Populating the interactive namespace from numpy and matplotlib
# 

#     [<matplotlib.lines.Line2D at 0x111ce59d0>]

# image file:

# In[174]:

# Return the subset of words that is in word_counts.
def known(words):
    return set(w for w in words if w in word_counts)

print known(['apple', 'zzzzasdfasdfz'])


# Out[174]:

#     set(['apple'])
# 

# In[175]:

def correct(word):
    candidates = known([word]) or known(edits(word)) or [word] # 'or' returns whichever is the first non-empty value
    return max(candidates, key=word_counts.get)


# In[177]:

print correct('apple')   # apple is in word_counts: known([word])
print correct('accross') # accross is not in word_counts, but across is: known(edits(word))
print correct('zebraa')  # zebra is not in word_counts: [word]


# Out[177]:

#     apple
#     across
#     zebraa
# 

# # How to use spelling correction?
# 
# - Make suggestions ("Did you mean?")
# - Add corrected terms to query
#   - only if query term is not in dictionary
#   - only if number of matches < N
