Edit this file in your private repository to provide answers to the following questions.

1. Consider merging the following two lists, where the first list has skip pointers.
![skips](skips.png)
  1. How often is a skip pointer followed (i.e., p1 is advanced to skip(p1))?

    **Insert your answer here.**

  2. How many postings comparisons will be made by this algorithm while intersecting the two lists?

    **Insert your answer here.** 
  
  3. How many postings comparisons would be made if the postings lists are intersected without the use of skip pointers?

    **Insert your answer here.**

2. Compute the Levenshtein edit distance between *paris* and *alice*. Fill in the 5 × 5 table below of
distances between all preﬁxes as computed by the algorithm in Figure 3.5 in [MRS](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf). Cell (*i*, *j*) should store the minimum edit distance between the first *i* characters of *alice* and the first *j* characters of *paris* (as in the bottom right number of each cell in Figure 3.6).

  |       |   | p | a | r | i | s |
  |-------|---|---|---|---|---|---|
  |       | 0 | 1 | 2 | 3 | 4 | 5 |
  | **a** | 1 |   |   |   |   |   |
  | **l** | 2 |   |   |   |   |   |
  | **i** | 3 |   |   |   |   |   |
  | **c** | 4 |   |   |   |   |   |
  | **e** | 5 |   |   |   |   |   |

3. (Inspired by [H Schütze](http://www.cis.uni-muenchen.de/~hs/teach/13s/ir/).)We define a *hapax legomenon* as a term that occurs exactly once in a collection. We want to estimate the number of hapax legomena using Heaps’ law and Zipf’s law.
    1. How many unique terms does a web collection of 400,000,000 web pages containing 400 tokens on average have? Use the Heaps parameters k = 100 and b = 0.5.
    2. Use Zipf’s law to estimate the proportion of the term vocabulary of the collection that consists of hapax legomena. You may want to use the approximation 1/1 + 1/2 + ... + 1/*n* = ln *n*
    3. Do you think that the estimate you get is correct? Why or why not?

  **Insert your answer here.**
