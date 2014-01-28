
# # CS 429: Information Retrieval
# 
# <br>
# 
# ## Lecture 5: Scalable Indexing
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
# - Efficient retrieval of postings lists
# - Wildcard queries
# - Spelling correction
# 
# Today: 
# 
# - How do we build an index that does not fit into memory? 

# - Disk seek time basics
#   - How long to read X bytes? Depends on if contiguous
# - Indexing steps:
#   - term-> term_id
#   - doc-> term-doc_id pairs
#   - sort by terms, then by docids
#   
# - External sorting (Single machine)
#   - minimize random disk seeks
#   
#   - Block sort-based indexing (BSBI)
#     - split documents
#     - sort term-docid pairs in memory, writing result to disk
#     - merge results
#     - ["the dog jumped", "the cat jumped"] -> (the, 0), (dog, 0), (jumped, 0), (the, 1), (cat, 1), (jumped, 1) -> (cat, [1]), (dog, [0]), (jumped, [0, 1]), (the, [0, 1])
#     
#   - Single-pass in-memory indexing (SPIMI)
#     - What if can't fit map from term->index in memory?
#     - separete dictionary for each block
#     - create postings lists on the fly, rather than print all postings then sort.
#     - sort postings lists, rather than individual postings
#     - ["the dog jumped", "the cat jumped"] -> (dog, [0]), (jumped, [0]), (the, [0]), ; (cat, [1]), (jumped, [1]), (the, [1]) -> (cat, [1]), (dog, [0]), (jumped, [0, 1]), (the, [0, 1])
#     
# - Distributed indexing
#   - MapReduce
#     - split documents (~100MB)
#     - (assume shared vocabulary for now)
#     - Map phase:
#       - generate key/value pairs for each document
#       - write to local intermediate files (segment files) (split files by term, e.g., a-g,g-p,q-z)
#     - Reduce phase:
#       - Inverter: collects all segment files (e.g., a-g from all mappers), reads, sorts, and merges.
#     

# # Building an index
# 
# - Up to now, we've assumed everything fits in memory.
# - We'll discuss three ways to scale
#   1. Block sort-based indexing (**BSBI**)
#   2. Single-pass in-memory indexing (**SPIMI**)
#   3. MapReduce

# How long does it take to read 100MB from disk?

# - **Seek time** (to locate data)
# - **Transfer rate** (to copy from disk into memory)
# - Contiguous or non-contiguous?

# # Block sort-based indexing (BSBI)
# 
# Assume a single machine.
# 
# 1. Split documents into **blocks**
# 2. For each block:
#   1. Parse each block into (word_id, doc_id) pairs
#   2. Sort pairs and create separate postings lists for each block.
#   3. Write postings lists to disk
# 3. Merge the postings lists file for each block
# 
# ![bsbi](files/bsbi.png)
# 
# (source: [MRS](http://nlp.stanford.edu/IR-book/pdf/04const.pdf))

# In[66]:

# BSBI: Create one postings list per block of documents.
from collections import defaultdict
from itertools import groupby

block1 = [(0, ["the", "dog", "jumped"]),
          (1, ["the", "cat", "jumped"])]
block2 = [(2, ["a", "dog", "ran"]),
          (3, ["the", "zebra", "jumped"])]
blocks = [block1, block2]

vocab = defaultdict(lambda: len(vocab))
for block_id, block in enumerate(blocks):
    # A. Collect all individual postings: (word_id, doc_id) pairs.
    postings = []
    for doc_id, doc in block:
        for word in doc:
            postings.append((vocab[word], doc_id))
    print 'block', block_id, 'postings=', postings
    print 'vocab=', vocab.items()
    
    # B. Sort postings and create postings lists.
    postings = sorted(postings, key=lambda x: x[0])
    print 'block', block_id, 'sorted postings=', postings
    
    # Group postings for same term together.
    postings = groupby(postings, key=lambda x:x[0])
    postings = [(word_id, [g[1] for g in group]) for word_id, group in postings]
    print 'block', block_id, 'grouped postings=', postings
    
    # C. Write to disk
    f = open('bsbi_block' + str(block_id) + '.txt', 'wt')
    f.write('\n'.join(['%s' % str(p) for p in postings]))
    f.close()
    print
    
# Then, merge blocks in linear time.


# Out[66]:

#     block 0 postings= [(0, 0), (1, 0), (2, 0), (0, 1), (3, 1), (2, 1)]
#     vocab= [('jumped', 2), ('the', 0), ('dog', 1), ('cat', 3)]
#     block 0 sorted postings= [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (3, 1)]
#     block 0 grouped postings= [(0, [0, 1]), (1, [0]), (2, [0, 1]), (3, [1])]
#     
#     block 1 postings= [(4, 2), (1, 2), (5, 2), (0, 3), (6, 3), (2, 3)]
#     vocab= [('a', 4), ('ran', 5), ('jumped', 2), ('dog', 1), ('cat', 3), ('zebra', 6), ('the', 0)]
#     block 1 sorted postings= [(0, 3), (1, 2), (2, 3), (4, 2), (5, 2), (6, 3)]
#     block 1 grouped postings= [(0, [3]), (1, [2]), (2, [3]), (4, [2]), (5, [2]), (6, [3])]
#     
# 

# # Merging posting list blocks
# 
# Since each block is sorted by term, can do a single linear pass through each block.
# 
# - Open all postings files simulataneously.
# - Read small buffer from each.
# - Equivalent to a union of postings lists for same term.

# # BSBI
# 
# Space requirements?

# - Number of tokens in each block ($T$)
# - Number of unique terms in vocabulary ($V$)

# Time requirements?

# - Sorting (word_id, doc_id) pairs in each block.
# - $O(T log T)$

# # Single-pass in-memory indexing (SPIMI)
# 
# - separate dictionary for each block
# - create postings lists on the fly, rather than collecting all postings then sorting.
# - sort postings lists, rather than individual postings
#     - ["the dog jumped", "the cat jumped"] -> (dog, [0]), (jumped, [0]), (the, [0]), ; (cat, [1]), (jumped, [1]), (the, [1]) -> (cat, [1]), (dog, [0]), (jumped, [0, 1]), (the, [0, 1]

# In[67]:

# SPIMI: Create one postings list per block of documents.
from collections import defaultdict
from itertools import groupby

block1 = [(0, ["the", "dog", "jumped"]),
          (1, ["the", "cat", "jumped"])]
block2 = [(2, ["a", "dog", "ran"]),
          (3, ["the", "zebra", "jumped"])]
blocks = [block1, block2]

for block_id, block in enumerate(blocks):
    # Note that there is a new vocab for each block!
    vocab = defaultdict(lambda: len(vocab))  # maps from term -> term_id
    index = defaultdict(lambda: [])          # from term_id -> postings list

    for doc_id, doc in block:
        # append doc_id to the postings list of each term
        for word in doc:
            index[vocab[word]].append(doc_id)
    
    
    # B. Sort terms
    sorted_terms = sorted(vocab.keys())
    print 'Block', block_id, [t + ' ' + str(index[vocab[t]]) for t in sorted_terms]
    
    # C. Write to disk
    f = open('spimi_block' + str(block_id) + '.txt', 'wt')
    f.write('\n'.join(['%d, %s' % (vocab[t], str(index[vocab[t]])) for t in sorted_terms]))
    f.close()
    print
    
# Then, merge blocks in linear time.


# Out[67]:

#     Block 0 ['cat [1]', 'dog [0]', 'jumped [0, 1]', 'the [0, 1]']
#     
#     Block 1 ['a [2]', 'dog [2]', 'jumped [3]', 'ran [2]', 'the [3]', 'zebra [3]']
#     
# 

# # SPIMI
# 
# Space requirements?

# - Number of tokens in each block ($T$)
# - Number of unique terms in vocabulary *in each block* ($V_b << V$)

# Time requirements?

# - Sorting unique terms in each block 
# - $O(V log V)$
#   - (compare to $O(T log T)$ for BSBI

# # MapReduce
# 
# - What if we had 100K servers?
# - **MapReduce:**
#   - A distributed programming framework
#   - Breaks large data into smaller data, called **splits**
# - Two phases:
#   - **Map:**
#     - Input: one split
#     - Output: (key, value) pairs
#   - **Reduce:**
#     - Input: (key, list of mapped values)
#     - Output: list of output values

# # MapReduce Counting Example
# 
# ```
# map(key, value):
#   for each word in value:
#     output word, 1
#        
# reduce(key, values):
#   output key, sum(values)
# ```
# 
# Framework takes care of grouping keys together to call `reduce` appropriately.
# 
# 

# # MapReduce Counting Example
# 
# - Split 1: "Twinkle, twinkle little star"
# - Split 2: "Little by little"
# 
# #### Map
# 
# "Twinkle, twinkle little star" $\rightarrow$ **Mapper 1**  $\rightarrow$ (twinkle, 1), (twinkle, 1), (little, 1), (star, 1)
# 
# "Little by little" $\rightarrow$ **Mapper 2** $\rightarrow$ (little, 1), (by, 1), (little, 1)
# 
# #### Reduce
# 
# (twinkle, 1), (twinkle, 1) $\rightarrow$ **Reducer 1** $\rightarrow$ (twinkle, 2)
# 
# (little, 1), (little, 1), (little, 1) $\rightarrow$ **Reducer 2** $\rightarrow$ (little, 3)
# 
# ...

# # Indexing with MapReduce
# 
# - **Map**: Read a document and output (term, doc_id) pairs.
# - **Reduce**: Read a list of doc_ids for a term and output a postings list.
# 
# 
# "Twinkle, twinkle little star" $\rightarrow$ **Mapper 1**  $\rightarrow$ (twinkle, 0), (little, 0), (star, 0)
# 
# "Little by little" $\rightarrow$ **Mapper 2** $\rightarrow$ (little, 1), (by, 1)
# 
# #### Reduce
# 
# (little, 0), (little, 1) $\rightarrow$ **Reducer 1** $\rightarrow$ (little, [0, 1])
# 
# ...

# In[76]:

import re
from mrjob.job import MRJob  # install with `pip install mrjob`

class MRIndexer(MRJob):
        
    def mapper(self, _, line):
        # Emit word, doc_id pairs from lines that look like:
        # doc_id [document tokens]
        words = re.findall('\w+', line.lower())
        doc_id = int(words[0])
        for word in set(words[1:]):
            yield word, doc_id

    def reducer(self, key, values):
        # key is a term, values is an (unsorted) list of doc_ids
        yield key, sorted(values)

# Run python mr.py to execute this example.

