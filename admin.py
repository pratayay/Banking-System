import db

class Admin:

    def close_account(self, ac_no):
        db.cur.execute(
            "UPDATE accounts SET status='Closed' WHERE account_no=%s",
            (ac_no,)
        )
        db.con.commit()

    def freeze_account(self, ac_no):
        db.cur.execute(
            "UPDATE accounts SET status='Frozen' WHERE account_no=%s",
            (ac_no,)
        )
        db.con.commit()

    def activate_account(self, ac_no):
        db.cur.execute(
            "UPDATE accounts SET status='Active' WHERE account_no=%s",
            (ac_no,)
        )
        db.con.commit()
