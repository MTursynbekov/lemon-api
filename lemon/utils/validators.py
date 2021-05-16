import os
import re

from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 2048000
ALLOWED_EXTENSIONS = ['.jpg', '.png']


def validate_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'max file size is: {MAX_FILE_SIZE / 1000} KB')


def validate_extension(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS}')


def validate_phone_number(value):
    value = value.replace(" ", "")
    is_valid = bool(re.match(r"(\+7)(7\d{2})\d(\d){6}$", value))
    if not is_valid:
        raise ValidationError(f'invalid phone number format, correct format is +77XXXXXXXXX')


def validate_discount(value):
    if value > 100:
        raise ValidationError(f'invalid discount value, discount should not be more than 100')
