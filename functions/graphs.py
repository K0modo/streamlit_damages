import plotly.express as px
import plotly.graph_objects as go

season_colors = {
    'Spring': '#6CC417',
    'Summer': '#EDE275',
    'Fall': '#EAC117',
    'Winter': '#56A5EC'
}

property_colors = {
    'Concord': '#0000A0',
    'Fairfax': '#566D7E',
    'Glouster': '#368BC1',
    'Helena': '#B93B8F',
    'Miami': '#CC6600',
    'Wilton': '#387C44',
}

chart_title_size = 24


def make_monthly_line(table):
    fig = go.Figure(
        data=[go.Scatter(
            x=table.index,
            y=table['Damages']
        )
        ]
    )
    fig.update_layout(
        title=dict(text="Damages by Month",
                   x=0.5,
                   y=0.85,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=chart_title_size)
                   ),
        yaxis=dict(tickprefix='$', )
    )

    return fig


def make_unit_strip(table):
    fig = px.strip(
        table,
        x='Property_Name',
        y='Damages',
        hover_data=['Unit_Number'],
        # color=['Property_Name'],
        # color_discrete_map=property_colors

    )
    fig.update_traces(marker=dict(size=3))
    fig.update_layout(
        title=dict(text="Damages by Unit",
                   x=0.5,
                   y=0.85,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=chart_title_size)
                   ),
        yaxis=dict(tickprefix='$',
                   separatethousands=True),
        xaxis_title=""
    )

    return fig


def make_season_pie(table):
    fig = go.Figure(
        data=[go.Pie(
            labels=table['Seasons'],
            values=table['Damages'],
            marker_colors=table['Seasons'].map(season_colors)
        )
        ]
    )

    fig.update_traces(textposition='inside',
                      text=table['Damages'].map("${:,.0f}".format),
                      textinfo='label+text+percent')

    fig.update_layout(
        title=dict(
            text='Damages by Season',
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
            font=dict(size=chart_title_size)
        ),
        showlegend=False,
    )

    return fig


def make_property_season_pie(table):
    fig = go.Figure(
        data=[go.Pie(
            labels=table['Seasons'],
            values=table['Damages'],
            marker_colors=table['Seasons'].map(season_colors))
        ]
    )

    fig.update_traces(textposition='inside',
                      text=table['Damages'].map("${:,.0f}".format),
                      textinfo='label+text+percent', )

    fig.update_layout(
        title=dict(
            text='Damages by Season',
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
            font=dict(size=chart_title_size)
        ),
        showlegend=False)

    return fig


def make_bed_bar(table):
    fig = go.Figure(
        data=[go.Bar(
            x=table['Beds'],
            y=table['Damages'], )
        ]
    )
    fig.update_layout(
        title=dict(text="Damages by Unit Bedrooms",
                   x=0.5,
                   y=0.9,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=chart_title_size)
                   ),
        yaxis=dict(tickprefix='$')
    )
    fig.update_xaxes(type='category')

    return fig


def make_property_bed_bar(table):
    fig = go.Figure(
        data=[go.Bar(
            x=table['Beds'],
            y=table['Damages'])
        ]
    )
    fig.update_layout(
        title=dict(text="Damages by Unit Bedrooms",
                   x=0.5,
                   y=0.9,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=chart_title_size)
                   ),
        yaxis=dict(tickprefix='$')
    )
    fig.update_xaxes(type='category')

    return fig


def make_property_bed_chart(table):
    fig = go.Figure(
        data=go.Bar(
            x=table.index,
            y=table['Damages_x'],
            name='Property Total', )
    )

    fig.add_trace(
        go.Scatter(
            x=table.index,
            y=table['Damages_y'],
            yaxis='y2',
            name='Population Average')
    )

    fig.update_layout(title=dict(text='Total vs Average Damages',
                                 y=0.9,
                                 x=0.5,
                                 yanchor='top',
                                 xanchor='center'),
                      xaxis=dict(title_text='Unit Bedrooms'),
                      yaxis=dict(title_text='Total Damages',
                                 side='left',
                                 tickprefix='$',
                                 separatethousands=True),
                      yaxis2=dict(title_text='Lawsuit Average',
                                  side='right',
                                  range=[0, 20],
                                  overlaying='y',
                                  tickmode='sync',
                                  tickprefix='$'),
                      legend=dict(orientation='h',
                                  y=1.15,
                                  x=0.5,
                                  xanchor='center'),
                      ),

    return fig
