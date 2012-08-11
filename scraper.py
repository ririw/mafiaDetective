import sqlite3
import httplib
import logging
logging.basicConfig(filename='fetcher.log',level=logging.INFO)
logger = logging.root
logger.addHandler(logging.StreamHandler())

from mafiaStooges import *
import wpScraping

db = sqlite3.connect('./mafia.db')
init_tables(db)
wpID = 38033256

wpScraping.scrapeGame(db, wpID)
