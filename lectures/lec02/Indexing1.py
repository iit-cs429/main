
# # CS 429: Information Retrieval
# 
# <br>
# ## Lecture 2: Indexing
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology 
# ### Spring 2014
# 
# ---
# 

# # Indexing Pipeline
# 
# 1. Collect documents
# 2. Tokenize
# 3. Normalize
# 4. Index

# # Indexing Pipeline
# 
# document $\xrightarrow{tokenize}$ (tokens, types) $\xrightarrow{normalize}$ terms $\xrightarrow{index}$ inverted index

# In[111]:

# 1. Collect documents.
document = "he didn't know where he worked."

# 2. Tokenize
tokens = ["he", "didn't", "know", "where", "he", "worked"] # split; remove punctuation
types = ["he", "didn't", "know", "where", "worked"] # unique tokens.

# 3. Normalize
# remove common words like 'where'; collapse word forms like worked -> work
terms = ["he", "didnt", "know", "work"]

# 4. Index
index = {'he': [0],
         'didnt': [0],
         'know' : [0],
         'work' : [0]}


# **e·quiv·a·lence class** (/i'kwivələns klas/) *n.*
# 
# 1. A subset whose elements are equivalent according to some relation $\sim$ .
# 
#     $S' \subseteq S \hspace{.2cm}$ s.t. $\hspace{.2cm}x_i \sim x_j \hspace{.1cm} \forall x_i, x_j \in S'$
#     
#     E.g., consider the set \{dog, cat, spider\} and the relation "has same number of legs". Then there are two equivalence classes: \{dog, cat\} and \{spider\}.

# **to·ken** (/tōkən/) *n*.
# 
# 1. A sequence of characters in a document that form a meaningful unit.
# 2. The output of a *tokenizer*.

# **type** (/tīp/) *n.*
# 
# 1. An equivalence class of *tokens* under the string equality relation.
# 2. By analogy to OO-programming, class:object :: type:token
# 
#     *e.g., "to be or not to be"* $\xrightarrow{tokenize}$ *tokens={to, be, or, not, to be}* $\hspace{.2cm}$  *types={to, be, or, not}*
#     
#     The type 'to' is an equivalence class containing the first and fifth tokens of the document.
# 

# **term** (/tərm/) *n.*
# 
# 1. An equivalence class of *types* under the relation "have the same normalized form."
# 2. The keys in the inverted index.
# 
#     e.g., types={John, john, aren't, arent} $\xrightarrow{normalize}$ terms={john, arent}.
# 
#     The term "john" is an equivalence class containing types {John, john}.
#     
#     The term "arent" is an equivalence class containing types {arent, aren't}.
#     
#     

# # Tokenization
# 
# **to·ken·i·za·tion** (/ˈtōkən izā-shən/) *n.*
# 
# 1. The process of splitting a document into tokens.
# 
#     *Simplest approach*: split on whitespace.
# 

# In[112]:

print document.split()


# Out[112]:

#     ['he', "didn't", 'know', 'where', 'he', 'worked.']
# 

# # Tokenization: Compound Nouns
# 
# - *San Francisco*;  *New York University* vs *York University*
# - Solved somewhat by *phrase indexing* (next class)

# # Tokenization: Segmentation
# 
# - *Lebensversicherungsgesellschaftsangestellter*
#   - "life insurance company employee"
# - 我不能说中国话
# - *\#androidgames*
# 

# - Statistical classification algorithms can be used to split (Part III of course). 
# - Simpler: index character subsequences (*n-grams*).
#   - E.g., *\#androidgames* $\rightarrow$ {*#andr, andro, ndroi, droid, roidg, ..., games*}

# # Tokenization: Punctuation
# 
# - Remove all punctuation? 

#   - "didn't", "www.google.com"
#   - [CAR](https://www.google.com/search?q=CAR) vs [C.A.R](https://www.google.com/search?q=C.A.R.).
#   - [O'Neill vs ONeill vs O Neill](https://www.google.com/#q=oneill+-o'neill&safe=active)

# # Tokenization: Regular Expressions

# symbol | meaning
# ------ | -------
# \b	| Word boundary (zero width)
# \d	| Any decimal digit (equivalent to [0-9])
# \D	| Any non-digit character (equivalent to [^0-9])
# \s	| Any whitespace character (equivalent to [ \t\n\r\f\v]
# \S	| Any non-whitespace character (equivalent to [^ \t\n\r\f\v])
# \w	| Any alphanumeric character (equivalent to [a-zA-Z0-9_])
# \W	| Any non-alphanumeric character (equivalent to [^a-zA-Z0-9_])
# \t	| The tab character
# \n	| The newline character
# 
# (source: <http://nltk.org/book/ch03.html>)

# In[2]:

import re  # Regular expression module
print re.split('x', 'axbxc')


# Out[2]:

#     ['a', 'b', 'c']
# 

# In[25]:

print re.split('\+\+', 'hi+++there')


# Out[25]:

#     ['hi', '+there']
# 

# In[38]:

print re.split('([\W\s]|t)', "what's up?")


# Out[38]:

#     ['wha', 't', '', "'", 's', ' ', 'up', '?', '']
# 

# In[29]:

text = "A first-class ticket to the U.S.A. isn't expensive?"
print re.split(' ', text)


# Out[29]:

#     ['A', 'first-class', 'ticket', 'to', 'the', 'U.S.A.', "isn't", 'expensive?']
# 

# How to remove punctuation?

# In[159]:

print re.split('\W+', text)           # \W=not a word character; +=1 or more


# Out[159]:

#     ['A', 'first', 'class', 'ticket', 'to', 'the', 'U', 'S', 'A', 'isn', 't', 'expensive', '']
# 

# In[160]:

print re.findall('\w+', text)         # \w=a word character [a-zA-Z0-9_]


# Out[160]:

#     ['A', 'first', 'class', 'ticket', 'to', 'the', 'U', 'S', 'A', 'isn', 't', 'expensive']
# 

# In[161]:

# group punctuation with following letters
print re.findall('\w+|\S\w*', text)  # \S=not a space; |=OR


# Out[161]:

#     ['A', 'first', '-class', 'ticket', 'to', 'the', 'U', '.S', '.A', '.', 'isn', "'t", 'expensive', '?']
# 

# How to keep hyphenated words and contractions together?

# In[43]:

print re.findall("\w+(?:[-']\w+)*|[-.(]+|\S\w*", text)
# (?: specifies what to match, not what to capture


# Out[43]:

#     ['A', 'first-class', 'ticket', 'to', 'the', 'U', '.', 'S', '.', 'A', '.', "isn't", 'expensive', '?']
# 

# In[44]:

print re.findall("(?:[A-Z]\.)+|\w+(?:[-']\w+)*|[-.(]+|\S\w*", text)


# Out[44]:

#     ['A', 'first-class', 'ticket', 'to', 'the', 'U.S.A.', "isn't", 'expensive', '?']
# 

# # Normalization
# 
# **nor·mal·iz·a·tion** (/ˈnôrməˌlizā-shən/) *n.*
# 
# 1. The process of clustering *types* into *terms*.
# 
#     Issues include: removing common words, special characters, casing, morphology

# # Normalization: Stop words
# 
# - Exclude common words
#   - *the*, *a*, *be*
# - Why?

#   - save space (length of postings list is huge!)
#   - no semantic content (?!)

# *"[to be or not to be](https://www.google.com/search?q=to+be+or+not+to+be&oq=to+be+or+not+to+be)"* is all stop words!

# # Accents/Diacritics
# 
# - naive vs. naïve
# - pena (sorrow) vs peña (cliff)

# - What will users enter?

# # Case
# 
# - Typically, just convert everything to lowercase.
# - E.g., search Google for [CAT -cat](https://www.google.com/search?q=CAT+-cat).

# # Stemming / Lemmatizing
# 
# **mor·phol·o·gy** (/môrˈfäləjē/) *n.*
# 
# 1. (*Linguistics*) The study of the rules governing how words may take different forms in a language.
# 
# *E.g.* 
# 
# - Pluralization: *dog* $\xrightarrow{pluralize}$ *dogs* ; *goose* $\xrightarrow{pluralize}$ *geese*
# 
# 
# - Tense: *play* $\xrightarrow{past.tense}$ *played* ; *go* $\xrightarrow{past.tense}$ *went*

# **stem** (/stem/) *v.*
# 
# 1. To normalize based on crude morphology heuristics.
# 
#     *E.g. remove all "-s" and "-ed" suffixes*

# **lem·ma·tize** (ˈleməˌtīz/) *v.*
# 
# 1. To create equivalence classes of word types using the morphological rules of a language.
# 
#     *Often relies on **part-of-speech** tagging to select rules*.
# 
#     *E.g. if * bed * is a noun, then do not remove * -ed *suffix.*

# # Simple stemmer
# 
# 

# In[91]:

def stem(word):
    for suffix in ['ies', 's', 'ed', 'ing']: # order matters!
        if word.endswith(suffix):
            return word[:-len(suffix)]


# **What can go wrong?**

# # Stemming Errors
# 
# - **over-stemming**: merge types that should not be merged.
# - **under-stemming**: fail to merge types that should be merged.

# In[46]:

types = ['tied', 'ties', 'tis', 'bed', 'cities']
print '\n'.join([stem(w) for w in types])


# Out[46]:


    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    <ipython-input-46-7154f802d81c> in <module>()
          1 types = ['tied', 'ties', 'tis', 'bed', 'cities']
    ----> 2 print '\n'.join([stem(w) for w in types])
    

    NameError: name 'stem' is not defined


# **How does this affect search?**

# # Porter Stemmer
# 
# - Very commonly used stemmer with a complex set of heuristics.

# In[ ]:

from nltk.stem import PorterStemmer # See nltk.org (`pip install nltk`)
porter = PorterStemmer()
print types
print '\n'.join([porter.stem(x) for x in types])


# Out[]:


    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    <ipython-input-45-15fdbdb8f5d3> in <module>()
          1 from nltk.stem import PorterStemmer # See nltk.org (`pip install nltk`)
          2 porter = PorterStemmer()
    ----> 3 print types
          4 print '\n'.join([porter.stem(x) for x in types])


    NameError: name 'types' is not defined


# In[107]:

types = ['bed', 'kiss',
         'tied', 'tis',
         'universal', 'university',
         'experiment', 'experience',
         'past', 'paste',
         'alumnus', 'alumni',
         'adhere', 'adhesion',
         'create', 'creation']
porter_results = [porter.stem(x) for x in types]
print '\n'.join(porter_results)


# Out[107]:

#     bed
#     kiss
#     tie
#     ti
#     univers
#     univers
#     experi
#     experi
#     past
#     past
#     alumnu
#     alumni
#     adher
#     adhes
#     creat
#     creation
# 

# # WordNet Lemmatizer

# In[106]:

from nltk.stem.wordnet import WordNetLemmatizer
# See description: https://wordnet.princeton.edu/wordnet/man/morphy.7WN.html
lemm = WordNetLemmatizer()
lemm_results = [lemm.lemmatize(x) for x in types]
print 'type, porter, lemmatizer\n'
print '\n'.join([str(t) for t in zip(types, porter_results, lemm_results)])


# Out[106]:

#     type, porter, lemmatizer
#     
#     ('bed', 'bed', 'bed')
#     ('kiss', 'kiss', 'kiss')
#     ('tied', 'tie', 'tied')
#     ('tis', 'ti', 'ti')
#     ('universal', 'univers', 'universal')
#     ('university', 'univers', 'university')
#     ('experiment', 'experi', 'experiment')
#     ('experience', 'experi', 'experience')
#     ('past', 'past', 'past')
#     ('paste', 'past', 'paste')
#     ('alumnus', 'alumnu', 'alumnus')
#     ('alumni', 'alumni', 'alumnus')
#     ('adhere', 'adher', 'adhere')
#     ('adhesion', 'adhes', 'adhesion')
#     ('create', 'creat', 'create')
#     ('creation', 'creation', 'creation')
# 

# # A principled approach?
# 
# Given the many number of ways to preprocess text, how do we know which one is best?

# Approaches:
# 
# - Assume types that appear in similar contexts can be merged.
#   - e.g., *universally* and *universal* appear in similar documents, but not *university*.

# - Learn from user behavior
#   - e.g., users click on very different search results if they search for *universal* vs *university*.
#   
# We'll explore both later in the course.
