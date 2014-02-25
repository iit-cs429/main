## Assignment 3: Ranking II

1. Download the [TIME](http://ir.dcs.gla.ac.uk/resources/test_collections/time/) dataset. 
  - This contains relevance judgements for 83 queries on a collection of 423 documents.
  - Do **not** store this data in github. Create a subdirectory here called `time`; unzip the contents there. You can then tell git to ignore this subdirectory by creating a text file here called `.gitignore` with the contents `time/`.
  - Your code should use relative, not absolute paths. That is, your code can assume there is a subdirectory here called `time`.

2.  Compare the following:
  1. **Cosine similarity:** Convert each query and document to tf-idf and sort the documents according to the cosine similarity between query and document.
  2. **RSV:** See the definition on the last slide of [lecture 12](https://github.com/iit-cs429/main/tree/master/lectures/lec12).
  3. **BM25:** See the definition on the last slide of [lecture 12](https://github.com/iit-cs429/main/tree/master/lectures/lec12).
    1. Consider 2 values for k (1, 2) and 2 values for b (.5, 1) (so, 4 different settings in total). 

3. For each system, compute the following evaluation metrics:
  - Precision
  - Recall
  - F1
  - Mean Average Precision (MAP)
  
4. Enter the results in the table in [Results.md](Results.md).

5. For RSV, compute a precision/recall curve and plot it using [matplotlib](http://matplotlib.org/). Save it to a file called `pr.png`.





