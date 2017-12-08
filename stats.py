from plotly.offline import plot
import plotly.graph_objs as go

def plot_stance(stances): 
    labels = ['Orthodox','Southpaw']
    values = [stances['Orthodox'],stances['Southpaw']]

    data = [
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=['#b70000', '#00158e']),
            textfont=dict(size=14, color='#ffffff')
        )
    ]

    layout = go.Layout(
        title = "<b>Dominated by Orthodox stance!</b>",
        autosize=False,
        width=500,
        height=500,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return plot(fig, validate=False, include_plotlyjs=False, output_type='div')

def plot_height(heights):    
    data = [
        go.Box(
            y=heights,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            name=' '
        )
    ]

    layout = go.Layout(
        title = "<b>They're Giants!</b><br> mean = 189cm, max = 214cm",
        autosize=False,
        width=400,
        height=500,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        yaxis=dict(
            title='Height (cm)'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return plot(fig, validate=False, include_plotlyjs=False, output_type='div')

def plot_reach(reachs):    
    data = [
        go.Box(
            x=reachs,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            name=' ',
            marker = dict(color = 'rgb(0, 128, 128)')
        )
    ]

    layout = go.Layout(
        title = "<b>With Long Arms!</b><br> mean = 198cm, max = 218cm",
        autosize=False,
        width=500,
        height=400,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(
            title='Reach (cm)'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return plot(fig, validate=False, include_plotlyjs=False, output_type='div')