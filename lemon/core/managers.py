from django.db.models import QuerySet, Manager


class ProductQuerySet(QuerySet):
    def get_by_category(self, category_id):
        return self.filter(category_id=category_id)

    def get_by_brand(self, brand_id):
        return self.filter(brand_id=brand_id)

    def get_by_city(self, city_id):
        return self.filter(city_id=city_id)

    def get_by_type(self, product_type):
        return self.filter(type=product_type)


class PromotionManager(Manager):
    def get_by_brand(self, brand_id):
        return self.filter(brand_id=brand_id)
