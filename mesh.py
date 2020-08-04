import plotly
import plotly.graph_objects as go
import femtomesh as fm
import timeit
import json

def create_plot(model, xbj, t, q2):
    start = timeit.default_timer()

    if model == 'A':
        csv_file = 'data/GPD_H.csv'

    mesh     = fm.FemtoMesh(csv_file)
    mesh.xbj = xbj
    mesh.t   = t
    mesh.q2  = q2

    df = mesh.process()

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    #figure = go.Figure()

    traces = {}
    traces['UP'] = go.Scatter(x=df.x,
                              y=df.xu,
                              fill='tozeroy',
                              name='GPD_UP (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2))
    traces['DN'] = go.Scatter(x=df.x,
                              y=df.xd,
                              fill='tozeroy',
                              name='GPD_DOWN (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2))

    data = list(traces.values())
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

    #return dict(data=traces['UP'], layout=dict(xaxis={'title': 'x'}, yaxis={'title': 'GPD'}))
