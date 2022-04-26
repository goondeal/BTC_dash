import plotly.express as px
import plotly.graph_objects as go

class StrategyGraph:
    def __init__(self, data):
        self.data = data


    def _build_graph(self):
        fig1 = px.line(self.data, x=self.data.index, y=['price', 'short', 'long'], labels ={'price': 'Price', 'short': 'SMA_Short', 'long': 'SMA_Long'} )
        fig2 = px.scatter(self.data, x=self.data.index, y='buy', symbol_sequence=['triangle-up'], color_discrete_sequence=['green'])
        fig3 = px.scatter(self.data, x=self.data.index, y='sell', symbol_sequence=['triangle-down'], color_discrete_sequence=['red'])        
        fig2.update_traces(marker={'size': 14})
        
        # fig3.update_traces(marker={'size': 15})
        fig = go.Figure(data=fig1.data + fig2.data + fig3.data)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1min", step="minute", stepmode="backward"),
                    dict(count=6, label="6mins", step="minute", stepmode="backward"),
                    dict(count=1, label="1h", step="hour", stepmode="todate"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        return fig
    
    
