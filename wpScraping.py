import httplib
import urllib
import json
import logging

def scrapeGame(db, wpID):
   gameConnection = httplib.HTTPSConnection('public-api.wordpress.com')
   gameConnection.request('GET', '/rest/v1/sites/%d/posts/' % wpID)
   postsConn = gameConnection.getresponse()
   #postsJSON = postsConn.read()
   postsJSON = json.loads(postsConn.read())
   postIDs = []
   posts = {}
   for post in postsJSON['posts']:
      postIDs.append(post['ID'])
      posts[post['ID']] = post['title']
   logging.info("Got posts %s" % postIDs)
   comments = []
   for postID in postIDs:
      gameConnection.request(
            'GET', 
            '/rest/v1/sites/%d/posts/%d/replies?number=100' % (wpID, postID))
      logging.info("Getting replies to post %d:%s" % (postID, posts[postID]))
      commentsConn = gameConnection.getresponse()
      commentsJSON = json.loads(commentsConn.read())
      totalComments = commentsJSON['found']
      commentsRead = 100
      while totalComments > 0:
         newComments = map(lambda c: 
                  (c['ID'], c['author']['name'], c['content']), 
                  commentsJSON['comments'])
         comments.extend(newComments)

         gameConnection.request(
               'GET', 
               '/rest/v1/sites/%d/posts/%d/replies?offset=%d&number=100' % (wpID, postID, commentsRead))
         logging.info("Getting replies to post %d with offset %d" % 
               (postID, commentsRead))
         commentsConn = gameConnection.getresponse()
         commentsJSON = json.loads(commentsConn.read())
         totalComments -= len(newComments)
         commentsRead += len(newComments)
   names = {}
   c = db.cursor()
   for author in c.execute('''select name,id from authors'''):
      names[author[0]] = author[1]
   c.close()
   db.commit()

   for comment in comments:
      cID = comment[0]
      name = comment[1]
      text = comment[2]
      if name not in names:
         c = db.cursor()
         c.execute('''insert into authors values (null,?,'u',2)''', (name,))
         c.close()
         db.commit()
         c = db.cursor()
         for ids in c.execute('''select * from authors where name=?''', (name,)):
            names[name] = ids[0]
         c.close()
         db.commit()
      c = db.cursor()
      c.execute('''insert into posts values (?,?,?)''', (cID, text, names[name]))
      c.close()
      db.commit()


