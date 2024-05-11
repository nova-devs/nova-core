from rest_framework.exceptions import APIException

from nova import messages


class PermissionNotAllowedException(APIException):
    status_code = 403
    default_detail = messages.PERMISSION_NOT_ALLOWED


class InvalidPasswordException(APIException):
    status_code = 405
    default_detail = messages.INVALID_PASSWORD


class InvalidCredentials(APIException):
    status_code = 400
    default_detail = messages.INVALID_CREDENTIALS


class ActionFailedException(APIException):
    status_code = 500
    default_detail = messages.EXPORT_FIELDS


class NoRecordFoundException(APIException):
    status_code = 500
    default_detail = messages.NO_RECORD_FOUND
