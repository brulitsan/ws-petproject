from rest_framework import exceptions, status


class UserBalanceException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User dont have enough money'


class CurrencyPriceException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'currency price  not enough'


class ProductPriceException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'product price  not enough'
