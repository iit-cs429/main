## Assignment 4: Classification

In this assignment, you'll implement a Naive Bayes classifier for spam filtering.

Complete the classify.py method by following Figure 13.2 from your text (using add-one smoothing). I recommend reading Example 13.1 to test your understanding of this computation.

You should download the data [here](http://cs.iit.edu/~culotta/cs429/lingspam.zip), which is a slightly modified version of the [LingSpam](http://csmining.org/index.php/ling-spam-datasets.html) spam dataset. This contains a set of emails categorized as spam or not, with headers removed.

Unzip the data in the same folder as `classify.py`. This will create train and test folders.

The output of running `python classify.py` should match that in [Log.txt](Log.txt).
