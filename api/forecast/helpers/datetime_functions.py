
def round_datetime_to_hours(datetime):
    if not datetime:
        return None
    return datetime.replace(minute=0, second=0, microsecond=0)


def round_datetime_to_days(datetime):
    if not datetime:
        return None
    rounded_hours_datetime = datetime.replace(hour=0)
    return round_datetime_to_hours(rounded_hours_datetime)
