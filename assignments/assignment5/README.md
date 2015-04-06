## Assignment 5: Clustering

In this assignment, you will implement k-means clustering to cluster together a sample of user descriptions from Twitter. (Once again, I apologize for any offensive text you may be subjected to.) These are a somewhat random sample of 10,000 user profiles. They have already been tokenized.

1. Download the data from <http://cs.iit.edu/~culotta/cs429/profiles.txt> to your working directory. (Make sure it is also in .gitignore).
2. Implement the functions as indicated in `cluster.py`
  - `cluster`
  - `compute_means`
  - `compute_clusters`
  - `distance`
  - `error`
  - `print_top_docs`
  - `prune_terms`
3. You can use `test.txt` to help debugging -- there should be 3 clear clusters (a, b, c).
4. Your output should match that in [Log.txt](Log.txt).
