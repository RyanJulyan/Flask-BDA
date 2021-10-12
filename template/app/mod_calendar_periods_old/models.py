
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

    # @aggregated('calendar_periods_count', db.Column(db.Integer))
    # def calendar_periods_count(self):
    #     return db.func.count('1')


# Define a Calendar_periods model
class Calendar_periods(Base):
    __tablename__ = 'calendar_periods'
    # start new field definitions
    day = db.Column(db.Integer, nullable=False, default=False, unique=False, index=False)
    end_date = db.Column(db.DateTime, nullable=False, default=False, unique=False, index=True)
    month = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    month_index = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    quarter = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    quarter_index = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    start_date = db.Column(db.DateTime, nullable=False, default=False, unique=False, index=True)
    week = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    week_day = db.Column(db.String(50), nullable=False, default=False, unique=False, index=False)
    week_index = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)
    year = db.Column(db.Integer, nullable=False, default=False, unique=False, index=True)    # this line should be removed and replaced with the columns variable
    # end new field definitions
    # example_field = db.Column(db.String(256), nullable=False,default=False, unique=False)

    # New instance instantiation procedure
    def __init__(self, day, end_date, month, month_index, quarter, quarter_index, start_date, week, week_day, week_index, year):  # ,example_field):
        # start new instance fields
        self.day = day
        self.end_date = end_date
        self.month = month
        self.month_index = month_index
        self.quarter = quarter
        self.quarter_index = quarter_index
        self.start_date = start_date
        self.week = week
        self.week_day = week_day
        self.week_index = week_index
        self.year = year
        # end new instance fields
        # self.example_field = example_field

    def __repr__(self):
        # Set model quick lookup
        return '<Calendar_periods %r>' % (self.id)
