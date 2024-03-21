from django.db.models import TextChoices


class BaseUserTypes(TextChoices):
    DEFAULT_USER = "Пользователь", "Пользователь"
    ANALYST = "Аналитик", "Аналитик"
    ADMIN = "Администратор", "Администратор"


class BaseOrderType(TextChoices):
    PURCHASE = "Покупка", "Покупка"
    SALE = "Продажа", "Продажа"
    AUTO_SALE = "Авто_Продажа", "Авто_Продажа"
    AUTO_PURCHASE = "Авто_Покупка", "Авто_Покупка"


class BaseProductType(TextChoices):
    CRYPTOCURRENCY = "криптовалюта", "криптовалюта"
    STOCK = "акции", "акции"
    FUTURES = "фьючерсы", "фьючерсы"
    BONDS = "облигации", "облигации"


class BaseOrderStatus(TextChoices):
    success = "Успешно", "Успешно"
    cancelled = "Отменено", "Отменено"
    in_process = "В_процессе", "В_процессе"
