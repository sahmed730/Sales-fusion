import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class VisualizationBuilder:
    """Helper class to build consistent Plotly visualizations."""
    
    def __init__(self, color_scheme=None):
        self.color_scheme = color_scheme or px.colors.qualitative.Plotly
        
    def line_chart(self, data: pd.DataFrame, x_col: str, y_col: str, title: str):
        fig = px.line(data, x=x_col, y=y_col, title=title)
        fig.update_layout(template='plotly_dark')
        return fig
        
    def bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str, title: str, color_col=None):
        fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=title)
        fig.update_layout(template='plotly_dark')
        return fig
        
    def kpi_card(self, title: str, value: str, delta: str = None):
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "number+delta" if delta else "number",
            value = float(value.replace(',', '').replace('₹', '')),
            title = {"text": title},
            delta = {'reference': 0, 'relative': False, 'valueformat': '.2f'} if delta else None
        ))
        fig.update_layout(template='plotly_dark')
        return fig

if __name__ == "__main__":
    print("Visualization builder module ready to be imported.")
