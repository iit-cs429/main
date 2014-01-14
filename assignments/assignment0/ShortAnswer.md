Edit this file in your private repository to provide answers to the following questions (from MRS).

1. Extend the postings merge algorithm to arbitrary Boolean query formulas. What is
its time complexity? For instance, consider:

  `(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)`

  Can we always merge in linear time? Linear in what? Can we do better than this?

  **Insert your answer here.**

2. If the query is:

  `friends AND romans AND (NOT countrymen)`

  How could we use the frequency of countrymen in evaluating the best query evaluation order? In particular, propose a way of handling negation in determining the order of query processing.
  
  **Insert your answer here.**
  
3. For a conjunctive query, is processing postings lists in order of size guaranteed to be
optimal? Explain why it is, or give an example where it isn’t.

  **Insert your answer here.**
