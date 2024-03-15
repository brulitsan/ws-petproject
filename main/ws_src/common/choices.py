from django.db.models import TextChoices


class BaseUserTypes(TextChoices):
    DEFAULT_USER = "Пользователь", "Пользователь"
    ANALYST = "Аналитик", "Аналитик"
    ADMIN = "Администратор", "Администратор"


class BaseOrderType(TextChoices):
    PURCHASE = "Покупка", "Покупка"
    SALE = "Продажа", "Продажа"


class BaseProductType(TextChoices):
    CRYPTOCURRENCY = "криптовалюта", "криптовалюта"
    STOCK = "акции", "акции"
    FUTURES = "фьючерсы", "фьючерсы"
    BONDS = "облигации", "облигации"
