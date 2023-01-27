from django.apps import apps
from itertools import product
import datetime

class VariableClient:
    account_ratio = apps.get_model('marketdata', 'AccountRatio')
    mixed_account = apps.get_model('marketdata', 'MixedAccount')
    momentum = apps.get_model('marketdata', 'Momentum')
    price_ratio = apps.get_model('marketdata', 'PriceRatio')
    single_account = apps.get_model('marketdata', 'SingleAccount')
    size = apps.get_model('marketdata', 'Size')

    def list_models(self):
        return [
            self.account_ratio,
            self.mixed_account,
            self.momentum,
            self.price_ratio,
            self.single_account,
            self.size,
        ]

    def list_variables(self, to_dict=False):
        ls = list()
        ls_models = self.list_models()
        for model in ls_models:
            qs_vars = model.objects.all()
            ls += [var for var in qs_vars]
        if to_dict:
            return [self.model_to_dict(var) for var in ls]
        return ls


    def find(self, name):
        ls_models = self.list_models()
        for model in ls_models:
            qs_vars = model.objects.all()
            for var in qs_vars:
                if var.name == name:
                    return var
        return None

    def get_variable(self, model_name, id, to_dict=False):
        var = apps.get_model('marketdata', model_name).objects.get(id=id)
        if to_dict:
            return self.model_to_dict(var)
        return var

    def model_to_dict(self, var):
        return {
            'name': var.name,
            'address': var.address,
            'label_en': var.label_en,
            'label_kr': var.label_kr,
            'download_url': var.url.split('?')[0],
        }


class FactorGroupClient:
    model = apps.get_model('marketdata', 'Backtester')
    variable_client = VariableClient()

    def list_factor_groups(self, to_dict=False):
        qs = self.model.objects.all()
        if to_dict:
            return [self.model_to_dict(group) for group in qs]
        return [group for group in qs]

    def get_factor_group(self, group_id, to_dict=False):
        group = self.model.objects.get(id=group_id)
        if to_dict:
            return self.model_to_dict(group)
        return group

    def get_portfolios(self, group):
        portfolios = list()
        labels = [factor['labels'] for factor in group.factors]
        keys = list(product(*labels))
        for k in keys:
            d = dict()
            d['label'] = '_'.join(k)
            ranges = list()
            for i, label in enumerate(k):
                factor = group.factors[i]
                var = self.variable_client.get_variable(
                    model_name = factor['model_name'],
                    id = factor['id'],
                )
                lbloc = factor['labels'].index(label)
                ubloc = lbloc + 1
                lb = factor['quantiles'][lbloc]
                ub = factor['quantiles'][ubloc]
                ranges.append({
                    'factor_name': var.name,
                    'labelled_by': label,
                    'range': [lb, ub]
                })
            d['ranges'] = ranges
            portfolios.append(d)
        return portfolios

    def model_to_dict(self, group):
        return {
            'name': group.__str__(),
            'address': {'group_id': group.id},
            'rebalancing_frequency': group.rebalancing_frequency,
            'last_rebalance': list(group.rebalancing_history.keys())[-1],
            'factors': [{
                "variable": self.variable_client.get_variable(
                    model_name = factor['model_name'],
                    id = factor['id'],
                    to_dict = True
                ),
                'lookback': factor['lookback'],
                'quantiles': factor['quantiles'],
                'labels': factor['labels'],
            } for factor in group.factors],
            'download_url': group.url.split('?')[0],
        }

    def find_portfolio_by_label(self, group_id, label, to_dict=False):
        group = self.get_factor_group(group_id = group_id)
        portfolios = group.portfolios.all()
        found = False
        for pf in portfolios:
            if pf.label == label:
                found = True
                break
        if not found:
            return None
        if not to_dict:
            return pf
        pf_d = dict()
        pf_d['label'] = label
        k = tuple(label.split('_'))
        ranges = list()
        for i, labelled_by in enumerate(k):
            factor = group.factors[i]
            var = self.variable_client.get_variable(
                model_name = factor['model_name'],
                id = factor['id'],
            )
            lbloc = factor['labels'].index(labelled_by)
            ubloc = lbloc + 1
            lb = factor['quantiles'][lbloc]
            ub = factor['quantiles'][ubloc]
            ranges.append({
                'factor_name': var.name,
                'labelled_by': labelled_by,
                'range': [lb, ub]
            })
        pf_d['ranges'] = ranges
        return pf_d
