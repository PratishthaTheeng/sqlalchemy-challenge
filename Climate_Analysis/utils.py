from datetime import datetime,timedelta

def convert_date_to_str(date):
    return datetime.strptime(date, '%Y-%m-%d')

def get_year_ago(date):
    return date - timedelta(days=365)
