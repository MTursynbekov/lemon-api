# from django.db.models.signals import post_delete
# from django.dispatch import receiver
#
# from core.models import Product
# from utils.upload import delete_file


# @receiver(post_delete, sender=Product)
# def delete_product_images(sender, instance, **kwargs):
#     images = instance.images
#     if images:
#         delete_file(images.src.path)




