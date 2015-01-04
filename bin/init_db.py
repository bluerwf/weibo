#! /usr/bin/env python

import os
os.path.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ann import db

tb = db.AccountDB('/Users/lafengnan/codes/Github/weibo/weibo.db') 
tb.create_table()
