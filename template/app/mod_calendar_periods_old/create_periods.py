def create_periods(start = None, end = None, range_history_periods = 104, range_future_periods = 52, freq_period_start_day = '-SUN', freq_normalize = True, freq_closed = 'left'):

    """
    This function will create and return a standardized calendar between two dates.
    This calendar will follow the 4-4-5 standard using the ISO week number to calculate months and quarters.
    This calendar will address leap years, by converting week 53 into week 52.

    This calendar will have the following columns:
        - start_date
        - end_date
        - week_day
        - day
        - week
        - week_index
        - month
        - month_index
        - quarter
        - quarter_index
        - year

    Parameters:
        start = None # Default is None that will then be set to: (today - range_history_periods)
        end = None # Default is None that will then be set to: (today + range_future_periods)
        range_history_periods = 104 # this is used only when `start` is set to: None
        range_future_periods = 52 # this is used only when `end` is set to: None
        freq_period_start_day = '-SUN' # this is used to ensure that you get a full week of the start date provided, otherwise you will sometimes
        freq_normalize = True
        freq_closed = 'left'
    """

    import pandas as pd  # noqa: E402
    from datetime import date  # noqa: E402
    from dateutil.relativedelta import relativedelta  # noqa: E402
    from datetime import datetime, timedelta  # noqa: E402
    import numpy as np # noqa: E402
    
    start_day_dict = {
        '-SUN':-1,
        '-MON':0,
        '-TUE':+1,
        '-WED':+2,
        '-THU':+3,
        '-FRI':+4,
        '-SAT':+5
    }
    
    if start is None:
        start = date.today()
        start = (start + relativedelta(weeks = -range_history_periods))
    else:
        start = date(start)
    if end is None:
        end = date.today()
        end = end + relativedelta(weeks = +range_future_periods)
    else:
        end = date(end)
    
    start_of_week = start - timedelta(days = start.weekday()) 
    start_of_week = start_of_week + relativedelta(days = start_day_dict[freq_period_start_day])
    
    end_of_week = end - timedelta(days = end.weekday()) 
    end_of_week = end_of_week + relativedelta(days = start_day_dict[freq_period_start_day])

    df = pd.DataFrame({"date": pd.date_range(start = start_of_week, end = end_of_week, normalize = freq_normalize, closed = freq_closed)})
    df["start_date"] = pd.to_datetime(df['date'], format="%m/%d/%Y, %H:%M:%S.%m")
    # df["end_date"] = df.start_date.replace(hour=59)
    df["end_date"] = [df.start_date[i].replace(hour = 23, minute = 59, second = 59, microsecond = 999999) for i in range(len(df))]
    # df["end_date"] = pd.to_datetime(df.start_date, format="%y-%m-%d, %H:%M:%S")
    df["week_day"] = df.date.dt.day_name()
    df["day"] = df.date.dt.day
    df["week"] = df.date.dt.isocalendar().week
    df.loc[df['week'] == 53, 'week'] = 52 # Handle leap years (week 53)
    df["week_index"] = df.date.dt.year.astype(str) + df.week.astype(str)
    df["month"] = ((df.week.astype(int)*7)/(7*(52/12))).apply(np.ceil).astype(int)
    df["month_index"] = df.date.dt.year.astype(str) + df.month.astype(str)
    df["quarter"] = (df.month/3).apply(np.ceil).astype(int)
    df["quarter_index"] = df.date.dt.year.astype(str) + df.quarter.astype(str)
    df["year"] = df.date.dt.year
    return df


if __name__ == '__main__':
    periods = create_periods(range_history_periods = 15,range_future_periods = 45)
    # print(periods)
    print(periods.head(60))

