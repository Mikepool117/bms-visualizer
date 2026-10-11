import numpy as np
import plotly.graph_objects as go

# Generate data
x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-x/10)

# Create the plot
fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))

# Configure layout for scrolling
fig.update_layout(
    title='Scrollable Plot with Plotly',
    xaxis={
        'rangeslider': {'visible': True},
        'type': "linear"
    },
    yaxis_title="Amplitude",
    xaxis_title="Time"
)

fig.show()
