from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_age(value):
    birthday = datetime.datetime.strptime(str(value), "%Y-%m-%d")
    now = datetime.datetime.now()
    delta = now - birthday
    age_years = int(delta.days / 365)
    if delta.days < 365 * 18:
        raise ValidationError(_('Ваш возраст %(value)s, меньше чем 18 лет.'), params={'value': age_years})
