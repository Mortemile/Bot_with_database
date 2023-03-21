import sqlite3


class SQLighter:

    def __init__(self, database):
        """Connect to db"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Get all subscribers"""
        with self.connection:  # Execute SQL statement
            return self.cursor.execute("SELECT * FROM `subs` WHERE `subscription` = ?", (status,)).fetchall()
        # Return all rows of a query result as a list. Return an empty list if no rows are available

    def subscriber_exists(self, user_id):
        """Check user"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subs` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=False):
        """Add a new subscriber"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subs` (`user_id`, `subscription`) VALUES(?,?)",
                                       (user_id, status))

    def update_subscription(self, user_id, status):
        """Subscription status update"""
        with self.connection:
            return self.cursor.execute("UPDATE `subs` SET `subscription` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        """Close connection"""
        self.connection.close()
