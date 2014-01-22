
# # CS 429: Information Retrieval
# 
# <br>
# ## Lecture 3: Indexing II
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology 
# ### Spring 2014
# 
# ---
# 

# # Recall Inverted Index
# 
# ![diagrams-0](files/diagrams-0.png)
# 
# Runtime: $O(x + y)$, for postings lists of size $x$ and $y$

# # Skip Lists
# 
# ![diagrams-1](files/diagrams-1.png)

# Worst-case runtime? 

# $O(x + y)$

# Best-case runtime?

# $O(k)$, for $k$ matching documents

# # Merging Skip Lists

# In[1]:

# tuple (x,y,z): x=doc_id, y=skip index, z=skip value
index = {'cat': [(2, 3, 16), 4, 8, (16, 6, 28), 19, 23, 28, 43],
         'dog': [(1, 3, 5), 2, 3, (5, 6, 51), 8, 41, 51, 60, 71]}


# In[2]:

# Print postings list containing skip pointers.
def print_skip_list(docs):
    idx = 0
    while idx < len(docs):
        print docs[idx]
        if type(docs[idx]) is tuple: # skip
            idx = docs[idx][1]
        else:
            idx += 1


# In[3]:

print_skip_list(index['cat'])


# Out[3]:

#     (2, 3, 16)
#     (16, 6, 28)
#     28
#     43
# 

# In[4]:

print_skip_list(index['dog'])


# Out[4]:

#     (1, 3, 5)
#     (5, 6, 51)
#     51
#     60
#     71
# 

# ![skip_merge](files/skip_merge.png)

# # Where to insert skip pointers?
# 
# Tradeoff:
# 
# - More pointers mean more opportunities to skip 
# - Fewer pointers means less time wasted comparing to skip values.
# - Heuristic: $\sqrt{n}$ evenly-spaced pointers, for list of size $n$.
# 
# ![diagrams-2](files/diagrams-2.png)

# # Adding to an index with skip pointers
# 
# What happens when we have to add a document to a postings list?
# 
# 

# If postings list is a ...
# 
# - linked list
# - dynamic array (e.g., ArrayList)

# # Phrase queries
# 
# "cat dog" **vs** cat AND dog
# 
# 

# ![catdog](files/CatDog.jpeg) <img src="files/cat_and_dog.jpg" width=40%/>

# # Phrase Indexing
# 
# Two approaches
# 
# 1. **Biword Index**
# 2. **Positional Index**

# # Biword index
# 
# "The cat dog jumped."
# 
# ![diagrams-3](files/diagrams-3.png)

# # Finding phrases

# In[5]:

docs = [l.strip() for l in open("documents.txt", 'rt').readlines()]
print 'read', len(docs), 'docs'


# Out[5]:

#     read 62 docs
# 

# In[6]:

def ngrams(n, docs):
    terms = set()
    for d in docs:
        toks = d.split()
        for i in range(len(toks) - n + 1):
            terms.add('_'.join(toks[i:i+n]))
    return terms


# In[7]:

print ngrams(1, ['a b c'])
print ngrams(2, ['a b c'])
print ngrams(3, ['a b c'])
print ngrams(4, ['a b c'])


# Out[7]:

#     set(['a', 'c', 'b'])
#     set(['b_c', 'a_b'])
#     set(['a_b_c'])
#     set([])
# 

# In[8]:

max_n = 10
sizes = [len(ngrams(i, docs)) for i in range(1, max_n)]
print 'number of terms=', zip(range(1, max_n), sizes)


# Out[8]:

#     number of terms= [(1, 380), (2, 585), (3, 599), (4, 567), (5, 511), (6, 452), (7, 391), (8, 330), (9, 272), (10, 221), (11, 172), (12, 129), (13, 90), (14, 61), (15, 40), (16, 28), (17, 22), (18, 17), (19, 14), (20, 11), (21, 10), (22, 9), (23, 8), (24, 7), (25, 6), (26, 5), (27, 4), (28, 3), (29, 2), (30, 1), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0), (41, 0), (42, 0), (43, 0), (44, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0), (51, 0), (52, 0), (53, 0), (54, 0), (55, 0), (56, 0), (57, 0), (58, 0), (59, 0), (60, 0), (61, 0), (62, 0), (63, 0), (64, 0), (65, 0), (66, 0), (67, 0), (68, 0), (69, 0), (70, 0), (71, 0), (72, 0), (73, 0), (74, 0), (75, 0), (76, 0), (77, 0), (78, 0), (79, 0), (80, 0), (81, 0), (82, 0), (83, 0), (84, 0), (85, 0), (86, 0), (87, 0), (88, 0), (89, 0), (90, 0), (91, 0), (92, 0), (93, 0), (94, 0), (95, 0), (96, 0), (97, 0), (98, 0), (99, 0)]
# 

# In[9]:

get_ipython().magic(u'pylab inline')
# 1-grams, 1-grams + 2-grams, ...
x = [sum(sizes[:i]) for i in range(1,max_n)]
print x
plot(x)


# Out[9]:

#     Populating the interactive namespace from numpy and matplotlib
#     [380, 965, 1564, 2131, 2642, 3094, 3485, 3815, 4087, 4308, 4480, 4609, 4699, 4760, 4800, 4828, 4850, 4867, 4881, 4892, 4902, 4911, 4919, 4926, 4932, 4937, 4941, 4944, 4946, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947, 4947]
# 

#     [<matplotlib.lines.Line2D at 0x10da61110>]

# image file:

# # Limits of phrase indices
# 
# If we index 5-grams, how can we search for the phrase "to be or not to be"?

# - AND of 5-grams "to be or not to" AND "be or not to be"
# - Very small possibility of a false match

# What if we index 2-grams and we search for the phrase "new york university"
# 
# - "new york" AND "york university"
# - greater possibility of false match

# # Positional Index
# 
# - Store position of term in original document.
# - *term*: [(doc_id1, [pos1, pos2, ...]), (doc_id2, [pos1, pos2, ...]), ...]

# In[10]:

doc0 = "The cat dog jumped over the dog."
doc1 = "The dog jumped."
index = {
         'the': [(0, [0, 5]), (1, [0])],
         'cat': [(0, [1])],
         'dog': [(0, [2, 6]), (1, 1)],
         'jumped': [(0, [3]), (1, [2])]
         }


# # Positional Index

# - Additional space needed?

# - One `int` for each time a term occurs in a document.
# - Biggest impact on long documents.
# - E.g., consider a term that occurs once every thousand words:
# 
# |document length | # postings | # positional postings|
# |----------------|------------|----------------------|
# |1000            |  1         | 1                    |
# |100,000         |  1         | 100                  |
# 

# # Merging positional postings lists
# 
# How can we efficiently merge positional postings lists to find phrases?

# In[11]:

index = {'cat': [(0, [1])],
         'dog': [(0, [2, 6]),
                 (1, [1])]}
# [ (doc_id1, [pos1, pos2, ...]),
#   (doc_id2, [pos1, pos2, ...]), ...
# ]

# Search for "cat dog"
# This is inefficient! See Figure 2.12 (from book) and next assignment for more.
for cat_doc in index['cat']:
    for dog_doc in index['dog']:
        if cat_doc[0] == dog_doc[0]:  # In same document
            print 'both appear in ', cat_doc[0]
            for cat_pos in cat_doc[1]:
                for dog_pos in dog_doc[1]:
                    if cat_pos == dog_pos - 1: # dog comes right after cat.
                        print 'found "cat dog" at positions', cat_pos, dog_pos


# Out[11]:

#     both appear in  0
#     found "cat dog" at positions 1 2
# 

# # Combining Biword Index and Positional Index
# 
# - Store only phrases that are
#   - Commonly queried
#   - Individual words are common
# - *Britney Spears* vs. *The Who*

# ![diagrams-4](files/diagrams-4.png)
# 
# 1. How often is a skip pointer followed (i.e., p1 is advanced to skip(p1))?
# 2. How many postings comparisons will be made by this algorithm while intersecting the two lists?
# 3. How many postings comparisons would be made if the postings lists are intersected without the use of skip pointers?
