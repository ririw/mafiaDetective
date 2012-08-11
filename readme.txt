= Current status =
I'm pretty sure this _way_ overfits. 

= What is this =
This is a set of scripts that I am using to try to infer the alignment of some people in a mafia game. It attempts to use machine learning on their post's text along with supervised learning.


= What game is that? =
The game is hosted at epicmafiagame.wordpress.com

In theory the scripts could be used on any mafia game.

= How do I use it? =
1) Run "scraping.py" with python. This will download all posts in the game and all authors.
2) Update the database to tag known mafia:

   $ sqlite3 mafia.db

   >>update authors set isMafia=0 where name not in ('known', 'mafia', 'names');update authors set isMafia=1 where name in ('known', 'mafia', names');

2) Run "mine.py" - you need the python nltk library and the pyYAML library 
3) Download and install the orange machine learning program.
4) Open "investigate.vcs.ows" in orange.

= My results are stupid =
1) Machine learning is tricky
2) Are you 100% sure about who is and isn't mafia?

= Possible improvements =
* Accusation graphs
* Mention graphs
* Sentiment analysis on words
* When the game ends I'll add a full and correct "mafia.db" to the repo. Until then you need your own information!
* Using known mafia's posts to find unknown mafia.
