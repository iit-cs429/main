
# # CS 429: Information Retrieval
# 
# <br>
# 
# ## Lecture 8: Scalable scoring and system integration
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
#  - tf-idf weights for each document
#  - Vector Space Model
#  - Cosine Similarity
# 
# Today:
# 
#  - How to efficiently retrieve top ranked documents
#  - Full search pipeline
#  - Grab bag

# **tf-idf weight:**
# 
# - $w_{t,d} = (1 + \log tf_{t,d}) \times \log (\frac{N}{df_t})$
# 
# **cosine similarity:**
# 
# $sim(a, b) = \frac{a \cdot b}{||a||\hbox{ } ||b||}$
# 
# - $a \cdot b$ is dot product: $\sum_i a_i \times b_i$
# 
# 
# - $||a||$ is norm: $\sqrt{\sum_i a_i^2}$
# 
# **search:**
# 
# - convert each query and document into *tf-idf* vectors $q$ and $d$
# - sort documents by $sim(q, d)$
# 
# 

# In[ ]:

# Score documents by cosine similarity
from collections import defaultdict

# tf-idf weighted query
query = {'the': 0.01, 'zygote': 14.2}

# index is list of (doc_id, tf-idf weight) pairs
index = {'the': [(0, 44), (1, 100)],
         'zygote': [(0, 100), (1, 44)]}

# document lengths, for normalization
doc_lengths = {0: 12, 1: 12}

def cosine(query, index, doc_lengths):
  scores = defaultdict(lambda: 0)
  # For each search term
  for query_term, query_weight in query.items():
      # For each matching doc
      for doc_id, doc_weight in index[query_term]:
          scores[doc_id] += query_weight * doc_weight  # part of dot product

  # normalize by doc length (why not also by query length?)
  for doc_id in scores:
    scores[doc_id] /= doc_lengths[doc_id]
  return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
results = cosine(query, index, doc_lengths)
print results


# What is runtime?

# $O(QN)$ where $Q$ is number of query terms and $N$ is number of documents containing each query term.

# # Faster Cosine Search
# 
# If only retrieving top $k$, how can we do better than 
# 

# In[ ]:

sorted(scores.items(), key=lambda x: x[1], reverse=True)


# No need to sort all scores: use priority queue of size $k$
# 
# - $O(2J)$ to construct heap, where $J$ is number of docs with non-zero score
# - $O(k \log J)$ to find top $k$

# # Approximate $k$-best
# 
# - How can we find *almost* the top $k$ documents?

# - **Idea:**
#   - Find a set $A$ of *contenders* $K < |A| << N$
#   - Only compute cosine similarity between query and $A$
#   
# We'll consider a number of approaches.

# # Only use high $idf$ terms
# 
# - Similar to pruning stop words
# - Since low $idf$ terms occur in many documents, this prunes a lot
# - What's the downside?
# 
# 

# # Soft conjunction
# 
# - If query has 4 terms
#   - Retrieve all docs that match at least 3 terms
#   - Compute cosine similarity for this subset
# - How to find matches efficiently?

# # Champion lists
# 
# At index time:
# 
# - For each term $t$
#   - compute $r$ documents that have highest weight for $t$ ("champion lists")
#   
# At query time:
# 
# - Take union of champion lists of all query terms
# - Sort them by cosine similarity

# - How can we use an inverted index for a champion lists?

# # Static quality scores
# 
# - Assign a score $g(d)$ to each document at index time indicating how good it is
# - Based on what?

# - List of known good pages (Wikipedia, CNN, ...)
# - Pages with many in-links, bookmarks
# - PageRank
# - Is it spam?

# # Static quality scores
# 
# - How to combine static score with cosine score?
#   - **addition**: `netscore`$(q,d) = g(d) + sim(q,d)$
#   
# - How to efficiently find top $k$ by `netscore`?

# - One speedup: Order postings lists by $g(d)$
#   - Thus, we'll find top documents earlier
#   - Good if have small time budget

# # Impact ordering
# 
# - Sort postings list in decreasing order of $tfidf$

# In[31]:

index = {'the': [(0, 44), (1, 100)],
         'zygote': [(0, 100), (1, 44)]}

# becomes

index = {'the': [(1, 100), (0, 44)],
         'zygote': [(0, 100), (1, 44)]}


# How does this affect our algorithm to merge postings lists?

# We'll instead use our initial algorithm that accumulates scores one term at a time.
# 
# - Approximations:
#   - **Early termination**: stop traversing postings after $r$ docs or when weight drops below a threshold
#   - **$idf$ ordered search terms**: Sort query terms by $idf$ and process in order. Stop if score doesn't change much with additional term.

# # Cluster pruning
# 
# ![cluster](files/cluster.png)
# 
# - pick $\sqrt(N)$ docs at random (**leaders**)
# - assign all other docs to nearest leader
# - **follower**: doc attached to a leader
# - for query Q
#   - find nearest leader
#   - find K-best followers
#   - rank by cosine similarity
# 

# Improvements?
# 
# - Select $b > 1$ leaders; attach each follower to $c > 1$ leaders
# - when will cluster pruning fail?

# # Tiered indices
# 
# ![tier](files/tier.png)

# # Field and Zone Search
# 
# - *Field:* year, name, etc (limited values)
# - *Zone:* subsection of document (abstract, footer)
# 
# How to search these efficiently?
# 

# In[ ]:

index = {'the': [(0, 44), (1, 100)],
         'zygote': [(0, 100), (1, 44)],
         'the-title': [(0, 44), (1, 100)],
         'zygote-title': [(0, 100), (1, 44)],
         'the-abstract': [(0, 44), (1, 100)],
         'zygote-abstract': [(0, 100), (1, 44)],
         }


# # Query term proximity
# 
# - If query is: *dog catcher van*, how can we prefer documents where the three words occur in proximity?

# # Query parser
# 
# - Consider phrase query "pitchfork music festival"
# - Submit various queries until get at least $k$ results
#  - "pitchfork music festival"
#  - "pitchform music" AND "music festival"
#  - pitchform AND music AND festival
#  - ...

# # All together now...
# 
# ![system](files/system.png)
