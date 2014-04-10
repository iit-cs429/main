
# # CS 429: Information Retrieval
# <br>
# 
# ## Lecture 23: Clustering Words
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology
# ### Spring 2014

# # Motivation
# 
# Often, we want to know which features appear together.
# 
# - If you liked *Twilight* you might like *Nosferatu*.
# - "happy" is a synonym of "glad."

# We'll use k-means to cluster together related words from Twitter.
# 
# **Caution:** This uses live Twitter data, which often contains profanity.

# In[21]:

# Get some tweets containing the word 'i'.

import os
from TwitterAPI import TwitterAPI

# Read Twitter credentials from environmental variables.
api = TwitterAPI(os.environ.get('TW_CONSUMER_KEY'),
                 os.environ.get('TW_CONSUMER_SECRET'),
                 os.environ.get('TW_ACCESS_TOKEN'),
                 os.environ.get('TW_ACCESS_TOKEN_SECRET'))

# Collect tweets until we hit rate limit.
tweets = []
while True: 
    r = api.request('search/tweets', {'q':'i',
                                      'language':'en',
                                      'count':'100'})
    if r.status_code != 200: # error
        break
    else:
        for item in r.get_iterator():
            tweets.append(item)


# In[416]:

print len(tweets)


# Out[416]:

#     17300
# 

# In[417]:

# Each tweet is a Python dict.
print 'text', tweets[10]['text']
print 'description:', tweets[10]['user']['description']
print 'name:', tweets[10]['user']['name']
print 'location:', tweets[10]['user']['location']


# Out[417]:

#     text "You are amazing." - Silas says to Sam. I have to agree. #GH
#     description: I am a former editor.  A soon to be grad student and educator.  I currently have a book about my life in editing mode.
#     name: Sean Greeley
#     location: Oakland Gardens, New York
# 

# In[418]:

# Tokenize each tweet text.
import re
tokens = []
for tweet in tweets:
    text = tweet['text'].lower()
    text = re.sub('@\S+', ' ', text)  # Remove mentions.
    text = re.sub('http\S+', ' ', text)  # Remove urls.
    tokens.append(re.findall('[A-Za-z]+', text)) # Retain words.
print tokens[1]


# Out[418]:

#     [u'i', u'm', u'strangely', u'ok', u'with', u'being', u'known', u'as', u'a', u'day', u'drinker']
# 

# In[419]:

# Count words.
from collections import Counter

word_counts = Counter()
for tweet in tokens:
    word_counts.update(tweet)


# In[420]:

# Inspect word counts.
import math

print len(word_counts), 'unique terms'
sorted_counts = sorted(word_counts.items(),
                       key=lambda x: x[1],
                       reverse=True)
print '\n'.join('%s\t%d' % (w, c) for w, c in sorted_counts[:10])


# Out[420]:

#     18713 unique terms
#     i	21239
#     rt	5812
#     to	5137
#     you	4381
#     the	4192
#     a	4121
#     m	3303
#     my	3070
#     and	2891
#     me	2768
# 

# In[421]:

# Retain in vocabulary words occurring more than twice.
vocab = set([w for w, c in word_counts.iteritems() if c > 2])
print '%d words occur at least three times.' % len(vocab)


# Out[421]:

#     4915 words occur at least three times.
# 

# In[422]:

# Prune tokens.
newtoks = []
for i, tweet in enumerate(tokens):
    newtok = [token for token in tweet if token in vocab]
    if len(newtok) > 0:
        newtoks.append(newtok)
tokens = newtoks


# In[423]:

# A sample pruned tweet.
print tokens[1]


# Out[423]:

#     [u'i', u'm', u'ok', u'with', u'being', u'known', u'as', u'a', u'day']
# 

# In[426]:

# For each term, create a context vector, indicating how often
# each word occurs to the left or right of it.
from collections import defaultdict

# dict from term to context vector.
contexts = defaultdict(lambda: Counter())
window = 2
for tweet in tokens:
    for i, token in enumerate(tweet):
        features = []
        for j in range(np.amax([0, i-window]), i):
            features.append(tweet[j] + "@" + str(j-i))
        for j in range(i+1, min(i + window, len(tweet))):
            features.append(tweet[j] + "@" + str(j-i))
        contexts[token].update(features)
        # Optionally: ignore word order
        # contexts[token].update(tweet[:i] + tweet[i+1:])


# In[428]:

print contexts['you'].items()[:5]


# Out[428]:

#     [(u'talk@-2', 13), (u'touch@-2', 1), (u'please@1', 32), (u'man@-1', 1), (u'date@-1', 2)]
# 

# In[429]:

# Compute the number of different contexts each term appears in.
tweet_freq = Counter()
for context in contexts.itervalues():
    for term in context:
        tweet_freq[term] += 1.
print tweet_freq.items()[:5]


# Out[429]:

#     [(u'please@1', 90.0), (u'history@-1', 7.0), (u'sum@1', 11.0), (u'date@-2', 22.0), (u'history@-2', 8.0)]
# 

# In[430]:

# Transform each context vector to be term freq / tweet frequency. 
# Also then normalize by length.
for term, context in contexts.iteritems():
    for term2, frequency in context.iteritems():
        context[term2] = frequency / (1. + math.log(tweet_freq[term2]))
    length = math.sqrt(sum([v*v for v in context.itervalues()]))
    for term2, frequency in context.iteritems():
        context[term2] = 1. * frequency / length
    
print contexts['being'].items()[:5]


# Out[430]:

#     [(u'comes@-2', 0.021457572258183157), (u'or@1', 0.013519637819578057), (u'as@-1', 0.030798751481017773), (u'time@-1', 0.030514456587444547), (u'wow@1', 0.02101070082357469)]
# 

# At this point we have ~5k dictionaries, one per term, indicating the terms that co-occur (weighted by inverse tweet frequency).
# 
# Next, we have to cluster these vectors. To do this, we'll need to be able to compute the euclidean distance between two vectors.

# In[431]:

def distance(c1, c2):
    if len(c1.keys()) == 0 or len(c2.keys()) == 0:
        return 1e9
    keys = set(c1.keys()) | set(c2.keys())
    distance = 0.
    for k in keys:
        distance += (c1[k] - c2[k]) ** 2
    return math.sqrt(distance)

print distance({'hi':10, 'bye': 5}, {'hi': 9, 'bye': 4})
print distance({'hi':10, 'bye': 5}, {'hi': 8, 'bye': 4})


# Out[431]:

#     1.41421356237
#     2.2360679775
# 

# In[432]:

def find_closest(term, n=5):
    terms = np.array(contexts.keys())
    context = contexts[term]
    distances = []
    for term2, context2 in contexts.iteritems():
        distances.append(distance(context, context2))
    return terms[np.argsort(distances)][:n]

print find_closest('sad', n=10)


# Out[432]:

#     [u'sad' u'sleepy' u'excited' u'glad' u'sorry' u'scared' u'lazy' u'bad'
#      u'hungry' u'nervous']
# 

# In[436]:

nz_contexts = [t for t, context in contexts.items()
               if len(context) > 1]
contexts = dict([(term, contexts[term]) for term in nz_contexts])
print len(nz_contexts), 'nonzero contexts'


# Out[436]:

#     4910 nonzero contexts
# 

# In[437]:

# Transform context dicts to a sparse vector
# for sklearn.
from sklearn.feature_extraction import DictVectorizer

vec = DictVectorizer()
X = vec.fit_transform(contexts.values())
names = np.array(vec.get_feature_names())
print names[:10]
print X[0]


# Out[437]:

#     [u'a@-1' u'a@-2' u'a@1' u'aap@-1' u'aap@-2' u'aap@1' u'aapl@-1' u'aapl@-2'
#      u'aapl@1' u'aaron@-1']
#       (0, 4941)	0.237473316099
#       (0, 7742)	0.374375711285
#       (0, 6262)	0.146969238152
#       (0, 2252)	0.374375711285
#       (0, 13400)	0.166342996686
#       (0, 10740)	0.143485404568
#       (0, 8758)	0.163703930656
#       (0, 7285)	0.339401454089
#       (0, 2191)	0.229437338908
#       (0, 8608)	0.61729242976
#       (0, 1)	0.133230276709
# 

# In[438]:

# Let's cluster!
from sklearn.cluster import KMeans
num_clusters = 50
kmeans = KMeans(num_clusters)
kmeans.fit(X)


# Out[438]:

#     KMeans(copy_x=True, init='k-means++', max_iter=300, n_clusters=50, n_init=10,
#         n_jobs=1, precompute_distances=True, random_state=None, tol=0.0001,
#         verbose=0)

# In[439]:

# Let's print out the top features for each mean vector.
# This is swamped by common terms
for i in range(num_clusters):
    print i, ' '.join(names[np.argsort(kmeans.cluster_centers_[i])[::-1][:5]])


# Out[439]:

#     0 i@-2 i@-1 just@-1 ve@-1 a@1
#     1 the@-1 i@1 in@-2 to@-2 and@1
#     2 like@1 it@-1 elephant@-2 to@-1 starting@-2
#     3 be@-1 to@-2 i@-2 t@-2 being@-1
#     4 a@-1 i@1 my@-1 the@-1 a@-2
#     5 you@1 i@-2 i@-1 i@1 me@1
#     6 t@-1 can@-2 don@-2 i@-1 to@-1
#     7 i@-2 m@-1 m@-2 i@1 be@-1
#     8 my@-2 my@-1 i@1 the@-2 a@-1
#     9 an@-1 i@1 with@1 a@-2 for@-2
#     10 she@-1 it@-1 her@-2 he@-1 door@-2
#     11 your@-1 my@-1 in@-2 the@-1 i@1
#     12 up@1 i@-2 i@-1 a@-1 to@-1
#     13 the@-1 the@-2 in@-2 i@1 of@-2
#     14 and@-1 is@-1 he@-1 for@-1 the@1
#     15 a@-2 a@-1 i@1 but@1 and@1
#     16 i@-2 love@-1 m@-1 i@1 i@-1
#     17 proud@-2 to@-1 pleased@-2 i@1 rider@1
#     18 with@1 i@-2 to@1 m@-2 m@-1
#     19 in@-1 i@1 to@-1 for@-1 and@1
#     20 me@1 i@-1 you@1 you@-1 to@-1
#     21 to@-1 the@1 i@1 i@-1 to@1
#     22 lil@-1 gucci@-1 nia@-2 lady@1 essential@-1
#     23 i@-1 i@-2 rt@-2 i@1 a@1
#     24 i@-1 i@-2 a@1 rt@-2 i@1
#     25 of@1 the@-1 a@-1 i@-2 the@-2
#     26 san@-1 santa@-1 at@-2 churrascaria@-1 his@-1
#     27 de@1 de@-1 de@-2 m@-2 at@-1
#     28 to@-2 i@1 see@-1 the@-1 and@1
#     29 i@1 rt@-1 i@-2 the@-2 you@1
#     30 and@1 i@-2 the@-1 the@-2 my@-1
#     31 my@-1 i@1 in@-2 and@1 on@-2
#     32 i@-2 to@-2 i@1 the@1 for@-1
#     33 of@-1 the@-1 i@1 out@-2 i@-2
#     34 fa@1 oy@-2 santiago@-2 cia@-1 tylko@-1
#     35 my@1 the@1 i@-2 i@-1 a@1
#     36 so@-1 m@-2 i@-2 i@1 m@-1
#     37 gain@-2 gain@-1 rts@-2 followtrick@-1 teamfollowback@-1
#     38 from@-1 video@-2 national@-1 day@1 i@1
#     39 on@-1 i@1 on@-2 the@-1 the@-2
#     40 in@1 i@-2 the@-2 get@-1 to@-2
#     41 i@1 rt@-1 the@-1 i@-2 a@-2
#     42 to@1 i@-2 i@-1 m@-1 not@-1
#     43 rt@-1 rt@-2 i@-1 the@-2 i@-2
#     44 a@-1 i@1 and@1 the@-1 of@1
#     45 to@-1 i@-2 i@-1 it@1 my@1
#     46 you@-1 i@1 love@-2 i@-2 you@-2
#     47 t@1 i@-1 you@-1 if@-2 it@-1
#     48 flaherty@1 partnered@-2 rip@-1 pag@-1 affected@-2
#     49 on@1 i@-2 the@-1 a@-1 a@-2
# 

# In[440]:

# .transform will compute the distance from each term to each cluster.
distances = kmeans.transform(X)
print distances[0]


# Out[440]:

#     [ 1.13521267  1.1240182   1.10742592  1.08732169  1.03694299  1.04006013
#       1.15302655  1.15812103  1.03107212  1.08102953  1.10724202  1.05408489
#       1.11956906  1.02070019  1.0508641   1.01893944  1.0311229   1.1370101
#       1.05999362  1.010669    1.0954494   1.07168689  1.02534256  1.22808261
#       1.05724649  1.10921475  1.08896775  1.0245512   1.03153311  1.12516247
#       1.02367389  1.10663023  1.09598667  1.05891253  1.04467328  1.07224092
#       1.12788733  1.09460034  1.0410211   1.06544318  1.06445839  1.0165742
#       1.14504997  0.99765603  1.12288503  1.13720466  1.04061974  1.37525835
#       1.07813631  1.06099406]
# 

# In[441]:

# Finally, we'll print the words that are closest
# to the mean of each cluster.
terms = np.array(contexts.keys())
for i in range(num_clusters):
    print i, ' '.join(terms[np.argsort(distances[:,i])[1:10]])


# Out[441]:

#     0 saw got entered checked realized learned heard had made
#     1 world truth worst gym bathroom devil beach masters most
#     2 looks mctc feel titties feels sleeps essays look fly
#     3 bothered loyal honest expressed surprised attending appreciated able trusted
#     4 few little joke couple guy job good stoner boyfriend
#     5 cursing ship meet if invite miss annoying stalk tell
#     6 wait even stand breathe contain stop handle blame care
#     7 hungry guessing melting confused gonna lien getting afraid buried
#     8 yard dream glasses nationalsiblingday teacher liam twin watches brother
#     9 hour option adult indirect egg assignment argument upgrade acc
#     10 stays raps bent moaned screams tasted s takes hurts
#     11 face opinion butt stomach life mouth head heart car
#     12 wake fucked hurry messed ended give woken waking catching
#     13 same beach bathroom worst truth most masters way gym
#     14 hayley jazmyn adjust shake follows adj chase then signing
#     15 mood favor person photo kid pace tool tan buddy
#     16 you getting u probably afraid hungry done some a
#     17 satisfied lasted host boli say work share do play
#     18 partnered content quote done deeply pleased deal agree concerned
#     19 class japan town front depth politics ohio bed cleveland
#     20 excuse tell remind gave make reminds ignore inspired followed
#     21 play eat draw clarify go brush meet sleep spend
#     22 sis punk rob freaky mane doe steve wayne czym
#     23 hate got swear am hope volunteer ll think thought
#     24 got hate am hope swear have volunteer thought just
#     25 amount type sort instead none part rest lots pair
#     26 fransico monica cruz pride rn sons spf ce maria
#     27 deus de banda el centro las gol e hospital
#     28 ourselves playlist bathroom dms moon portland pausing him them
#     29 but ahhh cause yes yep yeah lol and because
#     30 paradise fun prison pencil legend gps brothers yogurt favour
#     31 tl phone wrist hair heart dad car soul own
#     32 u a him not that some getting them afraid
#     33 justice habit india couples college weirdos those duty nowhere
#     34 madre vuruyor nun qu oy sms ada chcecie metropolitana
#     35 stole updated wasting in rearranged change packing washed into
#     36 much sleepy cute hard glad lazy bad far upset
#     37 followtrick onedirection ua tcfollowtrain mm teamfollowback ipadgames retweet vod
#     38 dallas minecraft argentina sos congress throwbackthursday battle mw monsters
#     39 soundcloud yelp youtube sunday speak tumblr saturday holiday instagram
#     40 faith performing stuck checked participate interested masturbate landed involved
#     41 when ahhh cause yes and lol yep yeah because
#     42 trying listen unable listening used addicted going talk able
#     43 do one all lol like shit man and for
#     44 few couple little joke stoner cookie cassette nap chance
#     45 find watch take be do say make put play
#     46 were guys shawty are spinnrtaylorswift inspired happybdayshaymitchellfrombrazil bby join
#     47 ain wouldn didn haven couldn wasn won shouldn hadn
#     48 mr cdnpoli parallels makism autism gising tayo society mplaces
#     49 focus focusing hooked depends working lock focused poop banged
# 

# Clearly, interpreting these results requires a bit of investigation.
# 
# Some patterns do emerge:
#  - Cluster 47 is all contractions
#  - Cluster 29,41 seems to be inerjections/[disfluencies](http://en.wikipedia.org/wiki/Speech_disfluency)
#  - Cluster 39 refers to tech sites.
#  - Cluster 34 has Polish and what looks like Spanish.
# 
# As the number of tweets increases, we expect these clusters to become more coherent.
