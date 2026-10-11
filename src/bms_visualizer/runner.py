import plotly.graph_objects as go
import polars as pl


def main():
    df = pl.read_csv("dataset/dataset.csv")

    fig = go.Figure()

    # Trace 1: Voltage (Primary Y-axis, Left)
    fig.add_trace(go.Scattergl(
        x=df["Timestamp"],
        y=df["Battery_Voltage"],
        name="Voltage (V)",
        yaxis="y1",
        line={"color": "#1f77b4"}
    ))

    # Trace 2: Current (Secondary Y-axis, Right)
    fig.add_trace(go.Scattergl(
        x=df["Timestamp"],
        y=df["Battery_Current"],
        name="Current (A)",
        yaxis="y2",
        line={"color": "#ff7f0e"}
    ))

    # Trace 3: SoC (Tertiary Y-axis, Right offset)
    fig.add_trace(go.Scattergl(
        x=df["Timestamp"],
        y=df["SoC"],
        name="SoC (%)",
        yaxis="y3",
        line={"color": "#2ca02c", "shape":"hv"},
        fill="tozeroy",
        legendgroup="soc"
    ))

    fig.add_trace(go.Scattergl(
        x=[df["Timestamp"][0],df["Timestamp"][-1]],
        y=[20, 20],
        mode="lines",
        line={"color": "#ef4444", "dash": "dash", "width": 1.5},
        name="Critical Reserve (20%)",
        legendgroup="soc",
        hoverinfo="skip",
        yaxis="y3",
    ))

    # Lock all y-axes to prevent vertical drift during dragging

    fig.update_layout(
        title="Battery Telemetry with Multi-Axis Toggle",
        xaxis={"domain": [0.05, 0.9], "rangeslider": {"visible": True}, "fixedrange": False},

        # Primary Y-Axis (Left)
        yaxis={
            "title": "Voltage (V)",
            "tickfont": {"color": "#1f77b4"},
        },

        # Secondary Y-Axis (Right)
        yaxis2={
            "title": "Current (A)",
            "tickfont": {"color": "#ff7f0e"},
            "overlaying": "y",
            "side": "right",
        },

        # Tertiary Y-Axis (Far Right with offset)
        yaxis3={
            "title": "SoC (%)",
            "tickfont": {"color": "#2ca02c"},
            "anchor": "free",
            "overlaying": "y",
            "side": "right",
            "position": 0.96,
        },

        legend={"x": 0.05, "y": 1.15, "orientation": "h"}
    )

    # fix for scrolling
    fig.update_yaxes(fixedrange=True)
    fig.show(config={"scrollZoom":True})
