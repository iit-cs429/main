Edit this file and push to your private repository to provide answers to the following questions.

1. In `searcher.py`, why do we keep an inverted index instead of simply a list
of document vectors (e.g., dicts)? What is the difference in time and space
complexity between the two approaches?

    The first thing that is possible to say is that none all documents can present the query terms. Furthermore, the size of an inverted index can be considerably smaller as it only stores unique terms and its occurence. This can be helpful in a large scale situation. Considering an implementation such as an hashmap, the inverted index would take O(1) for lookup for the term. If the the top higuest documents need to be computed, an heap can be used and then the time the show the results would be O(log(t)), where t is the number of documents that have the term. If we use a list of documents, as it is necessary to see if the term occurs in each document, it would take O(nd), where n is the number of documents that I have in my collection and d is the document length (because for each document it is necessary to check if the word occurs or no). However, in this situation, it is also possible to rank the documents in O(log(t)).
    
    Considering the space, if each term occurs at least in one collection, an inverted index would be O(n) for store, where n is the total number of different elements in the collection, as it element points the doc_id that it occurs. In the other case, the list of vectors would be O(N), where N is the total number of words in the collection (because terms can be repeated in this situation and it is necessary to store all of them as a consequence that we will be analyze each document sparately).

2. Consider the query `chinese` with and without using champion lists.  Why is
the top result without champion lists absent from the list that uses champion
lists? How can you alter the algorithm to fix this?

    This happens because when the threshold r for the champions list is defined as it is constructed at the time of index construction, the number chosen can be smaller than the top K results. This will imply that the subset selected A from the champions lists may be smaller than the number of D documents, influencing the cosine similarity calculations. In the example of the `searcher.py`, the search engine wants to show the 100 most relevant results whereas the champions lists just stores the top 10. A simple approach to solve this issue is just to set the threshold number as high as the number of the most relevant results that we want to compute.

3. Describe in detail the data structures you would use to implement the
Cluster Pruning approach, as well as how you would use them at query time.

    Given the number of documents N, the Data Structure used would be a list of lists. Each sqrt(N) leaders randomnly selected would be one of the indices of the first list and each of its followers would be the elements of each sublist. Each element of the lists would have the follwing structure : (doc_id : [list_of_terms], score). The clusters can be constructed by computing the cosine similarity between the leader and the followers. To pick the nearest document for each Leader, it is possible to use a data structure such as a heap. In this case the first N/sqrt(N) = **sqrt(N)** elements will the followers of each leader.
   
   Considering the query q, the query time can be described as the following: first, find the nearest leader L to q using cosine silarity.  Pick the element with the highest cosine similarity (in other words, the nearest one) and access its sublist, containing L and its followers. Again, compute the cosine simlarities between the elements, finding the nearest ones (for this case, again, it is possible to use a heap to rank them and return the top K documents).
