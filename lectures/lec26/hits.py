
# # CS 429: Information Retrieval
# <br>
# 
# ## Lecture 26: HITS
# 
# <br>
# 
# ### Dr. Aron Culotta
# ### Illinois Institute of Technology
# ### Spring 2014

# The **Hubs and Authorities** algorithm is a simple procedure to assign each page two scores:
# 
# - **hub score:** how likely is this page to be a directory?
# - **authority score:** how likely is this page to be a trustworthy resource on a topic?

# Let $F_u$ be *forward* links (going out from $u$).
# 
# Let $B_u$ be *back* links (going in to $u$).
# 
# $ \begin{align}
# h(u) = \sum_{v \in F_u} a(v)\\
# a(u) = \sum_{v \in B_u} h(v)\\
# \end{align}$
# 
# In words:
# 
# - The hub score for $u$ is the sum of the authority scores for all pages linked from $u$.
# - The authority score for $u$ is the sum of the hub scores for all pages linking to $u$.

# As for PageRank, we can compute these iteratively until convergence:
# 
# 1. Initialize all hub/authority scores to 1.0
# 2. Loop until convergence
#   1. update authority scores
#   2. update hub scores

# Let's try this out on some real data:

# In[160]:

# Get some search results.
from google import search
urls = set([u for u in search('football teams', stop=20)])
print 'top', len(urls), 'results:\n', '\n'.join(urls)


# Out[160]:

#     top 32 results:
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA
#     http://www.azcardinals.com/
#     http://www.usatoday.com/story/sports/nfl/2014/04/20/offseason-program-first-phase-begins/7946325/
#     http://www.goducks.com/SportSelect.dbml?SPID=233
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL
#     http://www.cbssports.com/collegefootball/teams
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/
#     http://www.nfl.com/teams/denverbroncos/profile?team=DEN
#     http://sports.yahoo.com/ncaa/football/teams
#     http://highschoolsports.nj.com/football/teams/
#     http://espn.go.com/nfl/teams
#     http://www.king5.com/sports/football-Offseason-activities-OTA-255999771.html
#     http://www.willamette.edu/athletics/football/
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/
#     http://www.cbssports.com/nfl/teams
#     http://www.freevector.com/canadian-football-teams/
#     http://www.forbes.com/nfl-valuations/
#     http://www.nfl.com/teams/newenglandpatriots/profile?team=NE
#     http://www.sodahead.com/entertainment/are-you-a-red-skins-fan-or-other/question-3688699/
#     http://www.sporcle.com/games/printzj/ncaahelmet1
#     http://www.sbnation.com/college-football/2014/3/31/5546726/professional-wrestlers-as-college-football-teams
#     http://en.wikipedia.org/wiki/National_Football_League
#     http://nfltix.net/nfl-football-prismatic-stickers-complete-set-of-32-teams-decals/
#     http://www.maxpreps.com/news/lRfk29Nphkue38lH0WvW0A/maxpreps-2013-all-american-football-teams.htm
#     http://www.nfl.com/teams
#     http://en.wikipedia.org/wiki/Football_team
#     http://www.puma.com/football/teams
#     http://msn.foxsports.com/nfl/teams
#     http://en.wikipedia.org/wiki/Category:American_football_teams
#     http://sportsillustrated.cnn.com/football/nfl/teams/
#     http://blogs.ajc.com/georgia-high-school-sports/2013/12/27/ajc-all-state-football-teams-2013/?cxntfid=blogs_georgia_high_school_sports
#     http://www.pro-football-reference.com/teams/
# 

# In[161]:

# Download links for each url. Store inlinks/outlinks for each page in original set.
from collections import defaultdict
import requests
from BeautifulSoup import BeautifulSoup
inlinks = defaultdict(lambda: set())   # url -> set of inlinks
outlinks = defaultdict(lambda: set())  # url -> set of outlinks 
for url in urls:
    soup = BeautifulSoup(requests.get(url).text)
    # Exclude self links and restrict to links in original search results.
    links = set([a['href'] for a in soup.findAll('a') if a.get('href')
                 and a['href'] in urls and a['href'] != url])
    outlinks[url] = links
    for link in links:
        inlinks[link].add(url)


# In[192]:

# Print outlinks.
for url in outlinks:
    if len(outlinks[url]) > 0:
        print '\n', url, '->\n', '\n'.join(outlinks[url])


# Out[192]:

#     
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA ->
#     http://www.azcardinals.com/
#     
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL ->
#     http://www.azcardinals.com/
#     
#     http://www.cbssports.com/collegefootball/teams ->
#     http://www.cbssports.com/nfl/teams
#     
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/ ->
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/
#     
#     http://www.nfl.com/teams/denverbroncos/profile?team=DEN ->
#     http://www.azcardinals.com/
#     
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/ ->
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/
#     
#     http://www.cbssports.com/nfl/teams ->
#     http://www.cbssports.com/collegefootball/teams
#     
#     http://www.nfl.com/teams/newenglandpatriots/profile?team=NE ->
#     http://www.azcardinals.com/
#     
#     http://www.nfl.com/teams ->
#     http://www.azcardinals.com/
# 

# In[193]:

# Print inlinks
for url in inlinks:
    if len(inlinks[url]) > 0:
        print '\n', url, '<-\n', '\n'.join(inlinks[url])


# Out[193]:

#     
#     http://www.cbssports.com/collegefootball/teams <-
#     http://www.cbssports.com/nfl/teams
#     
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/ <-
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/
#     
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/ <-
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/
#     
#     http://www.cbssports.com/nfl/teams <-
#     http://www.cbssports.com/collegefootball/teams
#     
#     http://www.azcardinals.com/ <-
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL
#     http://www.nfl.com/teams
#     http://www.nfl.com/teams/newenglandpatriots/profile?team=NE
#     http://www.nfl.com/teams/denverbroncos/profile?team=DEN
# 

# In[237]:

# Initialize hubs and authorities scores and print.
hubs = dict([(u, 1.0) for u in urls])
authorities = dict([(u, 1.0) for u in urls])
def print_top(hubs, authorities):
    print 'Top hubs\n', '\n'.join('%s %.6f' % (u[0], u[1]) for u in sorted(hubs.items(), key=lambda x: x[1], reverse=True)[:5])
    print 'Top authorities\n', '\n'.join('%s %.6f' % (u[0], u[1]) for u in sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:5])

print_top(hubs, authorities)


# Out[237]:

#     Top hubs
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA 1.000000
#     http://www.azcardinals.com/ 1.000000
#     http://www.usatoday.com/story/sports/nfl/2014/04/20/offseason-program-first-phase-begins/7946325/ 1.000000
#     http://www.king5.com/sports/football-Offseason-activities-OTA-255999771.html 1.000000
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL 1.000000
#     Top authorities
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA 1.000000
#     http://www.azcardinals.com/ 1.000000
#     http://www.usatoday.com/story/sports/nfl/2014/04/20/offseason-program-first-phase-begins/7946325/ 1.000000
#     http://www.king5.com/sports/football-Offseason-activities-OTA-255999771.html 1.000000
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL 1.000000
# 

# In[238]:

# Update hub and authority scores.
import math

def update(hubs, authorities, inlinks, outlinks):
    for u in authorities:
        authorities[u] += sum([hubs[inlink] for inlink in inlinks[u]])
    normalize(authorities)
    for u in hubs:
        hubs[u] += sum([authorities[outlink] for outlink in outlinks[u]])
    normalize(hubs)

def normalize(d):
    norm = math.sqrt(sum([v * v for v in d.values()]))
    for k in d:
        d[k] /= norm


# In[239]:

update(hubs, authorities, inlinks, outlinks)
print_top(hubs, authorities)


# Out[239]:

#     Top hubs
#     http://www.nfl.com/teams/seattleseahawks/profile?team=SEA 0.255349
#     http://www.nfl.com/teams/baltimoreravens/profile?team=BAL 0.255349
#     http://www.nfl.com/teams/denverbroncos/profile?team=DEN 0.255349
#     http://www.nfl.com/teams/newenglandpatriots/profile?team=NE 0.255349
#     http://www.nfl.com/teams 0.255349
#     Top authorities
#     http://www.azcardinals.com/ 0.675053
#     http://www.cbssports.com/collegefootball/teams 0.225018
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-2-facebook-myspace/ 0.225018
#     http://www.friendstagger.com/tag-your-friends-as-nfl-football-teams-facebook-myspace/ 0.225018
#     http://www.cbssports.com/nfl/teams 0.225018
# 

# ## Expanding the set of urls
# 
# - For a given query, begin with the *root* set of the top $k$ matching documents.
# - Expand the set to include all forward and backward links from the root.
# 
# When would this help?
# 
