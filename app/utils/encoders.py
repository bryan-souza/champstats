from datetime import datetime, time


def datetime_encoder(value: datetime):
    return value.isoformat()


def time_encoder(value: time):
    return value.isoformat()
