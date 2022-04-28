import plotly.express as px
import plotly.graph_objects as go

class StrategyGraph:
    def __init__(self, data):
        self.data = data
        price = px.line(self.data, x=self.data.index, y='price', labels ={'price': 'Price', 'short': 'SMA_Short', 'long': 'SMA_Long'} )
        buying_points = px.scatter(self.data, x=self.data.index, y='buy', symbol_sequence=['triangle-up'], color_discrete_sequence=['green'])
        selling_points = px.scatter(self.data, x=self.data.index, y='sell', symbol_sequence=['triangle-down'], color_discrete_sequence=['red'])        
        
        buying_points.update_traces(marker={'size': 10})
        selling_points.update_traces(marker={'size': 10})

        self.fig = go.Figure(data=price.data + buying_points.data + selling_points.data)
        self.fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    # dict(count=1, label="1day", step="day", stepmode="backward"),
                    dict(count=2, label="week", step="month", stepmode="backward"),
                    dict(count=7, label="month", step="month", stepmode="backward"),
                    dict(count=7, label="year", step="all", stepmode="backward")
                    # dict(step="all")
                ])
            )
        )
        # self._build_graph()

    def _build_graph(self):
        # ['price', 'short', 'long']
        price = px.line(self.data, x=self.data.index, y='price', labels ={'price': 'Price', 'short': 'SMA_Short', 'long': 'SMA_Long'} )
        buying_points = px.scatter(self.data, x=self.data.index, y='buy', symbol_sequence=['triangle-up'], color_discrete_sequence=['green'])
        selling_points = px.scatter(self.data, x=self.data.index, y='sell', symbol_sequence=['triangle-down'], color_discrete_sequence=['red'])        
        
        buying_points.update_traces(marker={'size': 14})
        selling_points.update_traces(marker={'size': 14})

        self.fig.data = price.data + buying_points.data + selling_points.data
        # fig = go.Figure(data=fig1.data + fig2.data + fig3.data)
        # fig.update_xaxes(
        #     rangeslider_visible=True,
        #     rangeselector=dict(
        #         buttons=list([
        #             dict(count=1, label="1min", step="minute", stepmode="backward"),
        #             dict(count=6, label="6mins", step="minute", stepmode="backward"),
        #             dict(count=1, label="1h", step="hour", stepmode="todate"),
        #             dict(count=1, label="1d", step="day", stepmode="backward"),
        #             dict(step="all")
        #         ])
        #     )
        # )

        # return fig
    

