# opendata-finance-kr-client

opendata-finance-kr의 python client입니다.

## Dependencies
**policy** google colab을 기준으로 의존성을 관리합니다.

**dependencies**
- python >= 3.7
- requests >= 2.25.1
- pandas >= 1.3.5
- matplotlib >= 3.2.2

## Usage

### Installation
```
pip install opendata_finance_kr
```

### Data Client
opendata-finance-kr이 제공하는 데이터셋을 불러올 수 있는 데이터 클라이언트 클래스를 소개합니다.

#### 1. Variable client<a name="variableClient"></a>

opendata-finance-kr이 제공하는 주요지표 데이터셋을 불러올 수 있는 데이터 클라이언트입니다.

```python
import opendata_finance_kr

client = opendata_finance_kr.client('variable')
```

##### listing variables

주요지표 데이터셋 리스트를 확인합니다.
```python
varlist = client.list_variables(to_dataframe=True)
print(varlist)
```

##### getting cross section data

지표명과 기준년월을 바탕으로 횡단면 데이터를 불러옵니다.
```python
cs = client.get_cross_section(
  variable_name = 'return_on_equity',
  yyyymm = '202209', # year month format with %Y%m
  to_dataframe = True # default=False returns a list of dictionaries
)
print(cs)
```

##### getting time series data for a corp

지표명과 종목코드를 바탕으로 시계열 데이터를 불러옵니다.
```python
ts = client.get_time_series(
  variable_name = 'return_on_equity',
  stock_code = '005930',
  to_dataframe = True # default=False returns a list of dictionaries
)
print(ts)
```

##### downloading panel data (in memory)

지표명과 다운로드 url을 바탕으로 패널 데이터를 다운로드합니다. zip파일로 다운로드되며 다음과 같은 in-memory 압축풀기 작업을 통해 로컬 스토리지에 파일을 저장하지 않고 데이터프레임으로 불러올 수 있습니다.
```python
from io import BytesIO, StringIO
import pandas as pd
import zipfile  # downloaded as zipfile

res = client.download_variable_panel(
  variable_name = 'return_on_equity'
)

zf = zipfile.ZipFile(BytesIO(res.content))
csv_filename = zf.namelist()[0]
with zf.open(csv_filename) as f:
  encoded = f.read()
  decoded = encoded.decode('utf-8')

panel = pd.read_csv(StringIO(decoded))
print(panel)
```

#### 2. Stock price client

opendata-finance-kr이 제공하는 종목별 횡단면 가격 데이터셋을 불러올 수 있는 데이터 클라이언트입니다.
```python
import opendata_finance_kr

client = opendata_finance_kr.client('stock_price')
```

##### listing downloadable data

가격 데이터셋의 목록을 확인합니다.
```python
client.list_data(to_dataframe=True)
```

##### directly getting dataframe by date

기준일자를 이용해 횡단면 데이터를 불러옵니다.
```python
df = client.get_dataframe(
  date = '20221229', # date to query in format %Y%m%d
  column_name = 'en', # default 'en'. 'kr' gives column names in Korean. 'raw' gives column names of openapi source
)
```

### Tools

opendata-finance-kr 데이터베이스를 기반으로 한 간단한 종목분석툴들을 소개합니다.

#### 1. Screener

 종목 스크리닝 툴의 활용법을 소개합니다.
```python
import opendata_finance_kr

screener = opendata_finance_kr.tool('screener')
```

##### listing available variable list

스크리너에 활용 가능한 주요지표의 목록을 확인합니다. screener object 내부의 variable_client object는 앞서 확인한 [variable client](#variableClient) object와 동일한 클래스에 속합니다.
```python
screener.variable_client.list_variables(to_dataframe=True)
```

##### creating screening logics

지표명 (variable_name), 기준년월 (yyyymm), 기준 분위 (quantile) 및 방향 (keep)을 이용해 스크리닝에 활용할 기준을 생성합니다. 예를 들어, '2022년 9월 기준 자기자본 이익률 상위 30%'라는 기준은
```python
logic0 = {
  'variable_name': 'return_on_quity',
  'yyyymm': '202209',
  'quantile': .7,
  'keep': 'top',
}
```
과 같이, 마찬가지로 '2022년 9월 기준 시가총액 하위 30%'라는 기준은
```python
logic1 = {
  'variable_name': 'market_equity',
  'yyyymm': '202209',
  'quantile': .3,
  'keep': 'bottom',
}
```
과 같이 정의할 수 있습니다. 기준을 정의한 후 다음과 같이 스크리너 object에 정의를 등록합니다. 등록된 순서에 따라 id가 자동으로 부여됩니다.

```python
screener.create_logic(
  variable_name = 'return_on_equity',
  yyyymm = '202209',
  quantile = .7,
  keep = 'top'  # keep 'top' above quantile .7
)
# or equivaliently,
# screener.create_logic(**logic0)

screener.create_logic(
  variable_name = 'market_equity',
  yyyymm = '202209',
  quantile = .3,
  keep = 'bottom'  # keep 'bottom' below quantile .3
)
# or equivaliently,
# screener.create_logic(**logic1)
```

##### listing created logics

생성한 스크리닝 기준의 목록을 확인합니다.
```python
print(screener.logic_list)
```

##### get a logic by auto-generated id

자동으로 부여된 id를 이용해 등록된 기준 object를 불러옵니다.
```python
logic1 = screener.get_logic(id=1) # will give the logic of return_on_quity created above section
logic2 = screener.get_logic(id=2) # will give the logic of market_quity created above section

print(logic1, logic2)
```

##### executing ordered (sequential) screening

등록된 기준의 순서에 따라 순차적 스크리닝을 실행합니다.
```python
screener.execute(ordered=True)
print(screener.result)
```

##### reordering logics by auto-generated id

다음과 같이 자동 생성된 id를 이용해 기준의 순서를 재정렬하여 순차적 스크리닝을 실행할 수 있습니다.
```python
screener.order_logics([2, 1])
print(screener.logic_list)

screener.execute(ordered=True)

print(screener.result)
```

##### executing unordered screening

등록된 기준들을 이용해 비순차적 스크리닝을 실행합니다.
```python
screener.execute(ordered=False)
print(screener.result)
```

##### checking dataframe

다음과 같이 백테스트에 활용된 데이터프레임을 확인할 수 있습니다.
```python
print(screener.dataframe)
```

##### resetting the screener

등록된 모든 스크리닝 기준과 결과를 지웁니다.
```python
screener.reset()
```


#### 2. Backtester

포트폴리오 백테스팅 툴의 활용법을 소개합니다.
```python
backtester = opendata_finance_kr.tool('backtester')
```

##### checking available date range

활용가능한 가격 횡단면데이터의 날짜 범위를 확인합니다. 2022년 12월 29일 이후의 데이터부터 조회 가능합니다.
```python
backtester.range_date()
```

##### creating a portfolio to backtest

포트폴리오 구성일 (date), 종목코드 목록 (stock_codes), 가중치 (weights), 보유기간 (개월, holding_period_in_month), 표기명 (label)을 이용해 백테스트를 실행할 포트폴리오를 생성합니다. 예를 들어 '2022년 12월 29일에 삼성전자와 네이버를 각 한 주씩 매입한 포트폴리오를 한 달 간 보유'했다면
```python
pf0 = {
  'date': '20221229',
  'stock_codes': ['005930', '035420'],
  'weights': [.5, .5],
  'holding_period_in_month': 1,
  'label': 'equal_weighted'
}
```
와 같이 포트폴리오를 정의할 수 있습니다. 정의된 포트폴리오를 다음과 같이 백테스터에 등록합니다.
- 등록 순서에 따라 자동으로 id가 부여됩니다.
- weights를 입력하지 않으면 입력한 종목들의 value weighted porfolio를 구성하여 백테스트가 실행됩니다.
- holding_period_in_month를 입력하지 않으면 입력한 포트폴리오 구성일로부터 backtester.date_range()로 조회된 최말일까지 백테스트가 실행됩니다.
- label을 입력하지 않으면 자동생성된 id를 포트폴리오의 식별자로 이용합니다.

```python
backtester.create_portfolio(
  date = '20221229', # date a portfolio was created
  stock_codes = ['005930', '035420'], # stock codes the portfolio contians
  weights = [.5, .5], # weights for each stock. default=None gives you a result with value weighted portfoilio
  holding_period_in_month = 1, # holding period in month. default=None gives you a result with full range of backtester.range_date()
  label = 'equal_weighted', # default=None gives this portfolio a label same as id
)
# or equivalently,
# backtester.create_portfolio(**pf0)

backtester.create_portfolio(
  date = '20221229', # date a portfolio was created
  stock_codes = ['005930', '035420'], # stock codes the portfolio contians
  holding_period_in_month = 1,
  label = 'value_weighted',
)
```

##### listing portfolios you've created

생성한 포트폴리오의 목록을 확인합니다.
```python
print(backtester.portfolio_list)
```

##### getting a portfolio you've created

다음과 같이 입력한 label 혹은 자동생성된 id를 이용해 포트폴리오 object를 불러올 수 있습니다.
```python
pf = backtester.get_portfolio(
  'value_weighted' # auto generated id or label you give
)
```


##### executing backtest for all portfolios

등록한 모든 포트폴리오에 대하여 백테스트를 실행합니다. 실행시 백테스트에 필요한 데이터를 다운로드하고 데이터셋을 구성하는 과정에서 입력된 기간에 비례하여 시간이 소요됩니다 (colab 기준 1일당 약 1.5초, 로컬 테스트 기준 1일당 약 0.2초).
```python
backtester.execute()
print(backtester.result)
```

##### checking dataframe

다음과 같이 백테스트에 활용된 데이터프레임을 확인할 수 있습니다.
```python
print(backtester.dataframe)
```


##### resetting the backtester

등록된 모든 포트폴리오 및 백테스트 결과를 지웁니다.
```python
backtester.reset()
```
