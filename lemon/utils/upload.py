import os

from django.utils import timezone
from datetime import datetime


def get_current_datetime():
    return timezone.make_aware(datetime.now())


def get_current_date_path_name():
    return get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S')


def product_images_directory_path(instance, filename):
    category = instance.product.category.name
    product = instance.product.name
    name, extension = filename.split('.')
    return f'images/products/{category}/{product}/{name}_{get_current_date_path_name()}.{extension}'


# def delete_file(path):
#     """ Deletes file from filesystem. """
#     if os.path.isfile(path):
#         os.remove(path)
