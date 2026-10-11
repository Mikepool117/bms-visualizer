import plotly.express as px
import polars as pl


def main():
    df = pl.read_csv("dataset/dataset.csv")
    fig = px.line(df, x='Timestamp',y='Battery_Current', title="test graph")
    fig.show()
