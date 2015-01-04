import os
os.path.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ann import db

def main():
    acc = db.AccountDB("weibo.db")
    if not acc.is_table_existing('account'):
        acc.create_table()
    if not acc.is_user_existing('ann'):
        acc.add_user('ann', '123')


if __name__ == '__main__':
    main()


