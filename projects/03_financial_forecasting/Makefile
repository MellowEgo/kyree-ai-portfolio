PY=uv run python
PKG=projects.03_financial_forecasting

setup:
	uv sync || pip install -r requirements.txt

data:
	$(PY) -m $(PKG).src.pipeline generate-data --out projects/03_financial_forecasting/data/raw/synth.parquet

backtest:
	$(PY) -m $(PKG).src.pipeline backtest --out projects/03_financial_forecasting/data/processed/backtest.csv

forecast:
	$(PY) -m $(PKG).src.pipeline forecast --out projects/03_financial_forecasting/data/processed/forecast.parquet

test:
	uv run pytest -q || pytest -q
