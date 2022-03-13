from rest_framework import status
from rest_framework.exceptions import APIException


class SiteUnreachable(APIException):
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    default_detail = "Site couldn't be reached"
