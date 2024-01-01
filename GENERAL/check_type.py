def check_number(target : str):
    try: 
        float(target)
        return True
    except:
        return False
    