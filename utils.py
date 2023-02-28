
def format_time(elapsed):
    """
    Returns specified formatted time.
    :param: elapsed(str):string of epoch time
    :Return: str
    """
    hours = int(elapsed/3600)
    minutes = int(elapsed/60 - hours * 60)
    seconds = int(elapsed - hours*3600 - minutes*60)
    return '%02d:%02d:%02d' %(hours, minutes, seconds)