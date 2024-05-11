from drf_yasg import openapi


class AccountParameters:
    parameters_account = [
        openapi.Parameter(
            'app_label_in',
            openapi.IN_QUERY,
            description="value of app_label_in",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'app_label',
            openapi.IN_QUERY,
            description="value of app_label",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'model',
            openapi.IN_QUERY,
            description="value of model",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'app_label_or_model',
            openapi.IN_QUERY,
            description="value of app_label_or_model",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'app_label_not_in',
            openapi.IN_QUERY,
            description="value of app_label_not_in (can be separated by commas)",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'ordering',
            openapi.IN_QUERY,
            description="value of ordering",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="value of limit",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'offset',
            openapi.IN_QUERY,
            description="value of offset",
            type=openapi.TYPE_INTEGER
        )
    ]
