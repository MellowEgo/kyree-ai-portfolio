import typer
from pathlib import Path
from typing import List
import pandas as pd
import numpy as np
from .evaluation.metrics import wmape, mase

app = typer.Typer(no_args_is_help=True)

@app.command()
def generate_data(out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    brands = ["Alpha","Beta"]; skus=["10mg","20mg"]; regions=["US","EU"]
    weeks = pd.date_range("2022-01-02", periods=156, freq="W-SUN")
    rows=[]
    for b in brands:
        for s in skus:
            for r in regions:
                base = rng.uniform(200,1000)
                seasonal = 1 + 0.2*np.sin(np.arange(len(weeks))/6.28)
                noise = rng.normal(0,30,len(weeks))
                y = np.maximum(0, base*seasonal + noise)
                rows += [(b,s,r,t,float(v)) for t,v in zip(weeks,y)]
    df = pd.DataFrame(rows, columns=["brand","sku","region","week","sales"])
    df.to_parquet(out)
    typer.echo(f"wrote {out} ({len(df):,} rows)")

@app.command()
def backtest(out: Path = Path("projects/03_financial_forecasting/data/processed/backtest.csv"),
             data: Path = Path("projects/03_financial_forecasting/data/raw/synth.parquet"),
             horizons: List[int] = [4,8,13]):
    df = pd.read_parquet(data).sort_values("week")
    results=[]
    for key,g in df.groupby(["brand","sku","region"]):
        y = g["sales"].to_numpy()
        for H in horizons:
            if len(y) <= H:
                continue
            train = y[:-H]
            pred = np.full(H, train[-13:].mean() if len(train)>=13 else train.mean())
            actual = y[-H:]
            results.append((*key,H, wmape(actual,pred), mase(actual,pred,seasonality=52)))
    bt = pd.DataFrame(results, columns=["brand","sku","region","h","wmape","mase"])
    out.parent.mkdir(parents=True, exist_ok=True)
    bt.to_csv(out, index=False); typer.echo(f"wrote {out}")

@app.command()
def forecast(out: Path = Path("projects/03_financial_forecasting/data/processed/forecast.parquet"),
             data: Path = Path("projects/03_financial_forecasting/data/raw/synth.parquet"),
             quantiles: List[float] = [0.1,0.5,0.9], horizon: int = 13):
    df = pd.read_parquet(data)
    last = df["week"].max()
    rows=[]
    for key,g in df.groupby(["brand","sku","region"]):
        y = g.sort_values("week")["sales"].to_numpy()
        mean = y[-13:].mean() if len(y)>=13 else y.mean()
        qvals = {q: max(0.0, mean*(1 + (q-0.5)*0.4)) for q in quantiles}
        for h in range(1,horizon+1):
            date = last + pd.Timedelta(weeks=h)
            for q,val in qvals.items():
                rows.append((*key,date,q,val))
    fc = pd.DataFrame(rows, columns=["brand","sku","region","week","quantile","value"])
    out.parent.mkdir(parents=True, exist_ok=True)
    fc.to_parquet(out); typer.echo(f"wrote {out}")

if __name__ == "__main__":
    app()
