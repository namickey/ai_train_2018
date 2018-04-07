import plotly

def plott():
    data = [plotly.graph_objs.Scatter(y=[2,3,1,2,5,2], name="legend"),
      plotly.graph_objs.Scatter(x=[1,2,3,4,5,6], y=[1,2,3,2,3,1], name="legend2")]
    layout = plotly.graph_objs.Layout(title="title",
    xaxis={"title":"xlabel"},
    yaxis={"title":"ylabel"})
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, show_link=False, image='png', image_filename='p.png', auto_open=False)
    #plotly.plotly.image.save_as(fig, filename='p.png')
plott()
