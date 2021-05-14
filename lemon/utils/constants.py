USER_ROLE_SUPER_USER = 1
USER_ROLE_CUSTOMER = 2
USER_ROLE_MANAGER = 3
USER_ROLES = (
    (USER_ROLE_SUPER_USER, 'admin'),
    (USER_ROLE_CUSTOMER, 'customer'),
    (USER_ROLE_MANAGER, 'manager'),
)

MEN_PRODUCT = 'M'
WOMEN_PRODUCT = 'W'
GIRLS_PRODUCT = 'G'
BOYS_PRODUCT = 'B'
NEWBORNS_PRODUCT = 'N'
PRODUCT_TYPE = (
    (MEN_PRODUCT, 'Мужской'),
    (WOMEN_PRODUCT, 'Женский'),
    (GIRLS_PRODUCT, 'Для девочек'),
    (BOYS_PRODUCT, 'Для мальчиков'),
    (NEWBORNS_PRODUCT, 'Для новорожденных'),
)
