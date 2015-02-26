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
  
4. Enter the results in the table in [Results.md](Results.md) in your private repository.

5. For RSV, compute a precision/recall curve and plot it using [matplotlib](http://matplotlib.org/). Save it to a file called `pr.png`; commit that file to your private repository.


Other clarifications:

- You can use the same tokenizer/stemmer as the previous assignment.
- You should report the average evaluation measures over all queries.
- You should ignore query terms that do not appear in any document.
- Compute precision/recall/F1 using only the top 20 results
- When computing MAP, if a relevant document is not in the top 20, assume 0% precision for those relevant documents.
- Note that IDs are assigned to queries and documents according to their position in the file, starting at ID 1. Thus, in TIME.REL, the line "1 268" indicates that the first query in TIME.QUE is relevant to the 268th document in TIME.ALL.









