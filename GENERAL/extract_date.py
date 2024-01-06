def get_date(stringDate):
    
    date = {}
    
    date['year'] = int(stringDate[:4])
    date['month'] = int(stringDate[4:6])
    date['day'] = int(stringDate[6:8])
    
    return date