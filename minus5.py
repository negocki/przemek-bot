import sqlite3


class Minus5:
    def __init__(self, conn):
        self.conn = conn
        self.curs = self.conn.cursor()
        # First time setup
        self.curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='minus5'")
        # if table 'minus5' doesn't exist:
        if len(self.curs.fetchall()) == 0:
            self.curs.execute("CREATE TABLE minus5 (user_id text, count int)")
            self.conn.commit()

    def _add_user(self, user_id):
        self.curs.execute("INSERT INTO minus5 (user_id, count) VALUES (?, 0)", (user_id,))
        self.conn.commit()

    def _remove_user(self, user_id):
        self.curs.execute("DELETE FROM minus5 WHERE user_id=?", (user_id,))
        self.conn.commit()

    def _is_user_in_database(self, user_id):
        self.curs.execute("SELECT * FROM minus5 WHERE user_id=?", (user_id,))
        if len(self.curs.fetchall()) < 1:
            return False
        else:
            return True

    def recalculate_stats(self, stats_dict):
        self.curs.execute("DELETE FROM minus5")  # delete all records
        for user_id, count in stats_dict.items():
            self._add_user(user_id)
            self.curs.execute("UPDATE minus5 SET count=? WHERE user_id=?", (count, user_id))
        self.conn.commit()

    def get_stats(self, user=None):
        if user == None:
            self.curs.execute("SELECT user_id, count FROM minus5")
            return self.curs.fetchall()
        else:
            self.curs.execute("SELECT user_id, count FROM minus5 WHERE user_id=?", (user.id,))
            return self.curs.fetchone()

    def increment_user(self, user):
        if not self._is_user_in_database(user.id):
            self._add_user(user.id)
        self.curs.execute("UPDATE minus5 SET count=count+1 WHERE user_id=?", (user.id,))
        self.conn.commit()

    def decrement_user(self, user):
        self.curs.execute("UPDATE minus5 SET count=count-1 WHERE user_id=?", (user.id,))
        self.conn.commit()