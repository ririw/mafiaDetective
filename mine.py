import sqlite3
import nltk
from yaml import load, dump
from yaml import Loader, Dumper
import random

conn = sqlite3.connect('./mafia.db')
data = load(open("language.yaml"), Loader=Loader)
slangSet = set(data['slangdict'].keys())
stopwords = set(data['stopwords'])
townPosts = []
mafiaPosts = []
townCorpus = []
mafiaCorpus = []
c = conn.cursor()
for l in c.execute('''select content,name,isMafia from posts left join authors on posts.author = authors.id'''):
   isMafia = l[2]
   if isMafia == 1:
      tokens = filter(lambda w: w not in stopwords, nltk.word_tokenize(l[0]))
      mafiaCorpus.extend(tokens)
      mafiaPosts.append(tokens)
   else:
      tokens = filter(lambda w: w not in stopwords, nltk.word_tokenize(l[0]))
      townCorpus.extend(tokens)
      townPosts.append(tokens)
c.close()
mafiaWords = nltk.FreqDist(w.lower() for w in mafiaCorpus)
townWords = nltk.FreqDist(w.lower() for w in townCorpus)
allWords = nltk.FreqDist(w.lower() for w in mafiaCorpus + townCorpus)
allTweets = [(t, 't') for t in townPosts] + [(t, 'm') for t in mafiaPosts]
random.shuffle(allTweets)
word_features = allWords.keys()[:1000]
def document_features(document):
   document_words = set(document) 
   features = {}
   for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
   return features
featuresets = [(document_features(d), c) for (d,c) in allTweets]

dumpTarget = open('data.tab', 'w')
headerList = [h for h in featuresets[0][0].keys()]
for header in headerList:
   dumpTarget.write(header.encode('ascii', 'ignore') + "\t")
dumpTarget.write('class\n')
for header in headerList:
   dumpTarget.write("d\t")
dumpTarget.write("d\n")
for header in headerList:
   dumpTarget.write("\t")
dumpTarget.write("class\n")
for featureset in featuresets:
   for header in headerList:
      dumpTarget.write(str(featureset[0][header]) + "\t")
   dumpTarget.write(str(featureset[1]) + "\n")
theslice = len(featuresets)/3
trainSet, testSet = featuresets[theslice:], featuresets[:theslice]
classifier = nltk.NaiveBayesClassifier.train(trainSet)
print(nltk.classify.accuracy(classifier, testSet))
classifier.show_most_informative_features(30)


