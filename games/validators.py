from django.core.exceptions import ValidationError

PERIODS = ['Not Started', '1', '2', '3', 'F', 'OT', '2OT', '3OT', '4OT', '5OT']


def validate_period(period):
    if period not in PERIODS:
        raise ValidationError(
            'Period must be valid. {} is not a valid period (periods list {})'.format(period, PERIODS))

def validate_event_type(t):
    if t != 'scoring':
        raise ValidationError(
            'Game Event\'s type must be valid. {} is not a valid type'.format(t)
        )