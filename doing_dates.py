from datetime import date
from time import strptime

def calc_date_between_dates(start_date:str, end_date:str) -> int:
    """ calculate the date between two given dates, includes the start and end date in the calculation, converts from YYYY-MM-DD to date object used for calc """
    # dates must strings in format YYYY-MM-DD
    # use strpttime to covert string dates to year month and day 
    dateS = strptime(start_date, "%Y-%m-%d") # d0 = date(2020, 11, 28)
    dateE = strptime(end_date, "%Y-%m-%d") # d1 = date(2021, 1, 5)
    # then make date objects from striped string
    d0 = date(dateS.tm_year, dateS.tm_mon, dateS.tm_mday)
    d1 = date(dateE.tm_year, dateE.tm_mon, dateE.tm_mday)
    # remember doesn't includes the start and end date in the calculation
    delta = d1 - d0
    # returns the difference as an int
    return(delta.days)

    # examples
    # print(calc_date_between_dates("2020-12-01", "2020-12-05")) # returns 4
    # print(calc_date_between_dates("2020-11-28", "2021-1-5")) # returns 38
    # print(calc_date_between_dates("2020-11-28", "2021-01-05")) # returns 38
    # print(type(calc_date_between_dates("2020-11-28", "2021-01-05"))) # returns 'int'


# get dates for year ending function? 