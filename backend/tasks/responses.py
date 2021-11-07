from rest_framework.exceptions import APIException


class TaskHintNotAvailable(APIException):
    status_code = 404
    default_detail = 'Task hint is not available.'
    default_code = 'task_unavailable'
