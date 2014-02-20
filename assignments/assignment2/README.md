## Assignment 2: Ranking (50 points)

0. Unzip `documents.txt.zip` into `documents.txt`.
1. Complete the methods in [searcher.py](searcher.py). You will:
  1. Create an index containing tf-idf values.
  2. Rank documents based on cosine similarity between query and document tf-idf vectors.
  3. Create a champion list, optionally searching that instead of the traditional index.
2. Complete the [ShortAnswer](ShortAnswer.md) questions.
3. **Bonus (5 points):** Implement the "Fast but imprecise" spelling corrector
I presented at the end of
[Lecture 4](https://github.com/iit-cs429/main/blob/master/lectures/lec04). Use
the terms in [documents.txt](documents.txt) to compute word counts, used by
the spelling corrector to pick the most likely correction. For each query,
correct all terms if needed and submit the transformed query (i.e., no need to
ask the user if it's okay to change the query). **Note:** you may need to
modify the `Index.__init__()` method to complete this.

In addition to the doctests, the expected output of `python searcher.py` is in [Log.txt](Log.txt).

To view the web interface, you'll need to install
[Flask](http://flask.pocoo.org/docs/installation). Then you can run `python
run.py` to launch the Flask server, which will respond to requests on
localhost (typically `http://127.0.0.1:5000/`).

The data in `documents.txt` contains snippets from the Wikipedia pages in the "Wiki Small" collection [here](http://www.search-engines-book.com/collections/).

**Update 2/20:** There is some ambiguity in how to compute inverse document frequency for the query_to_vector method. The result in `[Log.txt](Log.txt)` uses simply `1 / df(term)`. The result in `[Log2.txt](Log2.txt)` uses `log(N / df(term))`, where `N` is the number of documents, and `df(term)` is the number of unique documents in which a term appears. I will accept either answer.
