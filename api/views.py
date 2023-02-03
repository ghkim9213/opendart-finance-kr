from .clients import (
    VariableClient,
    FactorGroupClient,
)
from .src import configs as c
from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import json
import pandas as pd


class Readme(APIView):
    def get(self, request, format=None):
        with open('./README.md') as f:
            return Response(f.read())

class ApiDoc(APIView):
    def get(self, request, format=None):
        with open('./api/src/swagger.json') as f:
            swagger = json.load(f)
        return Response(swagger)


def find_status(config, code):
    for status in config['status']:
        if status['code'] == code:
            return status

def replace_status_desc(status, new_desc):
    return {**status, 'description': new_desc}


def encode_status(_status):
    CODE_STATUS_MAP = {
        200: status.HTTP_200_OK,
        204: status.HTTP_204_NO_CONTENT,
    }
    code = _status.get('code')
    return CODE_STATUS_MAP.get(code)



class VariableList(APIView):
    client = VariableClient()
    config = c.VARIABLE_LIST

    def get(self, request, format=None):
        _status = find_status(self.config, 200)
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': self.client.list_variables(to_dict=True)
        }
        return Response(data, status=status)


class VariableCrossSection(APIView):
    client = VariableClient()
    config = c.VARIABLE_CROSS_SECTION

    def merge_records(self, qs):
        merged = list()
        for obj in qs:
            merged += [{
                'date': obj.date.strftime('%Y%m%d'),
                **r
            } for r in obj.records]
        return merged

    def get(self, request, model_name, id, ym, format=None):
        strym = ym
        ym = datetime.datetime.strptime(ym, '%Y%m').date()
        is_price_var = model_name in ['Size', 'Momentum']
        var = self.client.get_variable(model_name, id)
        if is_price_var:
            qs = var.data.filter(
                date__year = ym.year,
                date__month = ym.month,
            )
        else:
            qs = var.data.filter(
                date__year = ym.year,
                date__month__gt = ym.month - 3,
                date__month__lte = ym.month
            )
        if qs.exists():
            _status = find_status(self.config, 200)
            records = self.merge_records(qs)
        else:
            _status = find_status(self.config, 204)
            records = list()
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': {
                'variable': self.client.model_to_dict(var),
                'records': records,
            }
        }
        return Response(data, status=status)


class VariableTimeSeries(APIView):
    client = VariableClient()
    config = c.VARIABLE_TIME_SERIES

    def merge_records(self, qs, stock_code):
        merged = list()
        for obj in qs:
            _data = list(filter(
                lambda r: r['stock_code'] == stock_code,
                obj.records
            ))
            if len(_data) == 0:
                continue
            _r = _data[0]
            merged.append({**_r, 'date': obj.date.strftime('%Y%m%d')})
        return sorted(merged, key=lambda r: r['date'])

    def get(self, request, model_name, id, stock_code, format=None):
        var = self.client.get_variable(model_name, id)
        qs = var.data.all()
        merged = self.merge_records(qs, stock_code)
        if len(merged) == 0:
            _status = find_status(self.config, 204)
        else:
            _status = find_status(self.config, 200)
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': {
                'variable': self.client.model_to_dict(var),
                'records': merged,
            }
        }
        return Response(data, status=status)


class FactorGroupList(APIView):
    client = FactorGroupClient()
    config = c.FACTOR_GROUP_LIST

    def get(self, request, format=None):
        _status = find_status(self.config, 200)
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': self.client.list_factor_groups(to_dict=True)
        }
        return Response(data, status)

class FactorGroupPortfolioList(APIView):
    client = FactorGroupClient()
    config = c.FACTOR_GROUP_PORTFOLIO_LIST

    def get(self, request, group_id, format=None):
        group = self.client.get_factor_group(group_id)
        portfolios = self.client.get_portfolios(group)
        last_rebalance = list(group.rebalancing_history.keys())[-1]
        portfolios = [{
            **pf,
            'entries': group.rebalancing_history.get(last_rebalance).get(pf['label'])
        } for pf in portfolios]
        # entries = self.get_entries(group, matched_dt)
        _status = find_status(self.config, 200)
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': {
                'factor_group': self.client.model_to_dict(group),
                'portfolios': portfolios
            }
        }
        return Response(data, status=status)


class FactorGroupPortfolioPerformance(APIView):
    client = FactorGroupClient()
    config = c.FACTOR_GROUP_PORTFOLIO_PERFORMANCE

    def get(self, request, group_id, portfolio_label, format=None):
        pf_d = self.client.find_portfolio_by_label(
            group_id = group_id,
            label = portfolio_label,
            to_dict = True
        )
        pf = self.client.find_portfolio_by_label(
            group_id = group_id,
            label = portfolio_label,
        )
        _records = pf.data.values('date', 'mktcap')
        df = pd.DataFrame.from_records(_records)
        df['rp'] = round((df.mktcap / df.mktcap.shift(1) - 1) * 100, 2)
        df = df[['date', 'rp']].dropna().copy()
        df.date = df.date.apply(lambda s: s.strftime('%Y%m%d'))
        records = df.to_dict(orient='records')
        _status = find_status(self.config, 200)
        status = encode_status(_status)
        data = {
            'status': _status,
            'data': {
                'portfolio': pf_d,
                'records': records
            }
        }
        return Response(data, status=status)


class StockPriceList(APIView):
    config = c.STOCK_PRICE_LIST
    model = apps.get_model('marketdata', 'StockPrice')
    MIN_DATE = datetime.date(year=2022, month=12, day=29)

    def get(self, request, format=None):
        records = self.model.objects.filter(date__gte=self.MIN_DATE).values('date', 'url')
        for r in records:
            r['date'] = r['date'].strftime('%Y%m%d')
            url = r.pop('url')
            r['download_url'] = url.replace('s3.ap-northeast-2', 's3-accelerate')
            # r['download_url'] = r.pop('url')
        _status = find_status(self.config, 200)
        status = encode_status(_status)

        data = {
            'status': _status,
            'data': records
        }
        return Response(data, status=status)
