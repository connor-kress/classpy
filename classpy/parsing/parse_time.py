from datetime import datetime, timedelta
from typing import Optional


def parse_exam_time(time_str: str) -> Optional[tuple[datetime, datetime]]:
    if time_str == '--':
        return None
    time_str = time_str.replace('\xa0', ' ')
    date_str, time_strs = time_str.split(' @ ')
    start_str, end_str = time_strs.split(' - ')
    date = datetime.strptime(date_str, '%m/%d/%Y')
    st = datetime.strptime(start_str, '%I:%M %p')
    et = datetime.strptime(end_str, '%I:%M %p')
    start = date + timedelta(hours=st.hour, minutes=st.minute)
    end = date + timedelta(hours=et.hour, minutes=et.minute)
    return (start, end)


def parse_class_dates(date_strs: str) -> tuple[datetime, datetime]:
    start_str, end_str = date_strs.split(' - ')
    start = datetime.strptime(start_str, '%m/%d/%Y')
    end = datetime.strptime(end_str, '%m/%d/%Y')
    return (start, end)
