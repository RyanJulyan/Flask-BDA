
# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Import aggregated functionality 
from sqlalchemy_utils import aggregated


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), index=True)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    # @aggregated('calendar_definitions_count', db.Column(db.Integer))
    # def calendar_definitions_count(self):
    #     return db.func.count('1')


# Define a Calendar_definitions model
class Calendar_definitions(Base):
    __tablename__ = 'calendar_definitions'
    # start new field definitions
    name = db.Column(db.String(256), nullable=False, default="Standard Calendar", unique=True, index=True)
    start = db.Column(db.String(10), nullable=True, default=None, unique=False, index=False)
    end = db.Column(db.String(10), nullable=True, default=None, unique=False, index=False)
    range_history_periods = db.Column(db.Integer, nullable=False, default=104, unique=False, index=False)
    range_future_periods = db.Column(db.Integer, nullable=False, default=104, unique=False, index=False)
    freq_period_start_day = db.Column(db.String(4), nullable=False, default="-SUN", unique=False, index=False)
    freq_normalize = db.Column(db.Boolean, nullable=False, default=True, unique=False, index=False)
    freq_closed = db.Column(db.String(4), nullable=False, default="left", unique=False, index=False)    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, name, start, end, range_history_periods, range_future_periods, freq_period_start_day, freq_normalize, freq_closed):  # ,example_field):
        # start new instance fields
        self.name = name
        self.start = start
        self.end = end
        self.range_history_periods = range_history_periods
        self.range_future_periods = range_future_periods
        self.freq_period_start_day = freq_period_start_day
        self.freq_normalize = freq_normalize
        self.freq_closed = freq_closed
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Calendar_definitions %r>' % (self.id)
