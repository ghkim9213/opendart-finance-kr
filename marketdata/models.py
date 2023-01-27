from django.db import models


class AccountRatio(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()
    numerator = models.JSONField()
    denominator = models.JSONField()

    class Meta:
        managed = False
        db_table = 'account_ratio'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)

    def get_numerator_object(self):
        return eval(self.numerator['model_name']).objects.get(id=self.numerator['id'])

    def get_denominator_object(self):
        return eval(self.denominator['model_name']).objects.get(id=self.denominator['id'])


class Backtester(models.Model):
    id = models.BigAutoField(primary_key=True)
    factors = models.JSONField()
    rebalancing_frequency = models.IntegerField()
    rebalancing_history = models.JSONField()
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'backtester'

    def __str__(self):
        ls_factors = self.list_factor_variable_objects()
        return ' x '.join([factor.__str__() for factor in ls_factors])

    @property
    def portfolios(self):
        return FactorPortfolio.objects.filter(backtester=self)

    def list_factor_variable_objects(self):
        ls = list()
        for factor in self.factors:
            ls.append(eval(factor['model_name']).objects.get(id=factor['id']))
        return ls


class CorpList(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    records = models.JSONField()

    class Meta:
        managed = False
        db_table = 'corp_list'

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class FactorPortfolio(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantile_locs = models.JSONField()
    backtester = models.ForeignKey(Backtester, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'factor_portfolio'

    def __str__(self):
        return f"{self.label.upper()} ({self.backtester.__str__()})"

    @property
    def label(self):
        return '_'.join([
            self.backtester.factors[i]['labels'][qloc]
            for i, qloc in enumerate(self.quantile_locs)
        ])

    @property
    def data(self):
        return FactorPortfolioData.objects.filter(portfolio=self)


class FactorPortfolioData(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    mktcap = models.BigIntegerField()
    portfolio = models.ForeignKey(FactorPortfolio, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'factor_portfolio_data'

    def __str__(self):
        return f"{self.portfolio.__str__()} ({self.date.strftime('%Y-%m-%d')})"


class MixedAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()
    ordered_single_accounts = models.JSONField()

    class Meta:
        managed = False
        db_table = 'mixed_account'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)

    def list_ordered_single_account_objects(self):
        return [
            eval(acnt['model_name']).objects.get(id=acnt['id'])
            for acnt in self.ordered_single_accounts
        ]


class Momentum(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()
    near = models.IntegerField()
    far = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'momentum'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)


class StockPrice(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    records = models.JSONField()
    is_monthend = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_price'


class PriceRatio(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()
    numerator = models.JSONField()

    class Meta:
        managed = False
        db_table = 'price_ratio'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)

    def get_numerator_object(self):
        return eval(self.numerator['model_name']).objects.get(id=self.numerator['id'])


class SingleAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()

    class Meta:
        managed = False
        db_table = 'single_account'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)



class Size(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    label_en = models.CharField(max_length=128, blank=True, null=True)
    label_kr = models.CharField(max_length=128, blank=True, null=True)
    file = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    last_update = models.DateField()

    class Meta:
        managed = False
        db_table = 'size'

    def __str__(self):
        return ''.join([x.capitalize() for x in self.name.split('_')])

    @property
    def address(self):
        return {
            'model_name': self._meta.model.__name__,
            'id': self.id,
        }

    @property
    def data(self):
        return VariableData.objects.filter(variable=self.address)


class VariableData(models.Model):
    id = models.BigAutoField(primary_key=True)
    variable = models.JSONField()
    date = models.DateField()
    records = models.JSONField()

    class Meta:
        managed = False
        db_table = 'variable_data'

    def __str__(self):
        return f"{self.get_variable().__str__()} ({self.date.strftime('%Y-%m-%d')})"

    def get_variable(self):
        return eval(self.variable['model_name']).objects.get(id=self.variable['id'])
