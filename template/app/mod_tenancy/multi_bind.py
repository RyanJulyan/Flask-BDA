
from app import app, db

class MultiBindSQLAlchemy(object):
    def __init__(self, bind_key):
        self.bind = db.get_engine(app, bind_key)
    def execute(self, query, params=None):
        return db.session.execute(query, params, bind=self.bind)


################################################################################
#### Add the following to a controller to be able to use different bindings ####
################################################################################

# from app.mod_tenancy.multi_bind import MultiBindSQLAlchemy

# ....

# db.first = MultiBindSQLAlchemy('first')
# db.first.execute(...)

# db.second = MultiBindSQLAlchemy('second')
# db.second.execute(...)

