import auth
import db

class Accounts:

    def is_account_owner(self, account_no):
        user_id = auth.Authentication.get_logged_user()

        db.cur.execute(
            """
            SELECT 1
            FROM accounts
            WHERE account_no = %s AND user_id = %s
            """,
            (account_no, user_id)
        )

        return db.cur.fetchone() is not None
