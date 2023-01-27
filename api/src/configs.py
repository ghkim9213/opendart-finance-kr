from rest_framework import status

STATUS_OK = {
    'code': 200,
    'description': 'ok',
}

STATUS_NO_CONTENT = {
    'code': 204,
    'description': 'no content',
}

README = {
    'url': 'readme.md',
    'view_name': 'Readme',
    'status': [STATUS_OK]
}


API_DOC = {
    'url': 'swagger.json',
    'view_name': 'ApiDoc',
    'status': [STATUS_OK]
}

VARIABLE_LIST = {
    'url': 'variable/list',
    'view_name': 'VariableList',
    'status': [STATUS_OK],
}

VARIABLE_CROSS_SECTION = {
    'url': 'variable/<str:model_name>/<int:id>/cross-section/<str:ym>',
    'view_name': 'VariableCrossSection',
    'status': [
        STATUS_OK,
        STATUS_NO_CONTENT,
    ]
}

VARIABLE_TIME_SERIES = {
    'url': 'variable/<str:model_name>/<int:id>/time-series/<str:stock_code>',
    'view_name': 'VariableTimeSeries',
    'status': [
        STATUS_OK,
        STATUS_NO_CONTENT,
    ]
}

FACTOR_GROUP_LIST = {
    'url': 'factor-group/list',
    'view_name': 'FactorGroupList',
    'status': [STATUS_OK],
}

FACTOR_GROUP_PORTFOLIO_LIST = {
    'url': 'factor-group/<int:group_id>/portfolio/list',
    'view_name': 'FactorGroupPortfolioList',
    'status': [
        STATUS_OK,
        STATUS_NO_CONTENT,
    ]
}

FACTOR_GROUP_PORTFOLIO_PERFORMANCE = {
    'url': 'factor-group/<int:group_id>/portfolio/<str:portfolio_label>/performance',
    'view_name': 'FactorGroupPortfolioPerformance',
    'status': [
        STATUS_OK,
        STATUS_NO_CONTENT,
    ]
}

LIST = [
    README,
    API_DOC,
    VARIABLE_LIST,
    VARIABLE_CROSS_SECTION,
    VARIABLE_TIME_SERIES,
    FACTOR_GROUP_LIST,
    FACTOR_GROUP_PORTFOLIO_LIST,
    FACTOR_GROUP_PORTFOLIO_PERFORMANCE
]
