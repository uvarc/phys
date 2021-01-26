import json

import plotly
import plotly.graph_objects as go

import femtomesh.femtomesh as fm


def gpd_scatter_plot(model, gpd, xbj, t, q2):
    csv_file = 'femtomesh/data/models/model_{model}/{gpd}.csv'.format(model=model, gpd=gpd)
    mesh = fm.FemtoMesh(csv_file)
    mesh.xbj = xbj
    mesh.t = t
    mesh.q2 = q2

    mesh.build_data_frame(xbj, t)
    df = mesh.process(multiprocessing=True, dim=1)

    df.to_csv('download/gpd_model.csv', index=False, header=['x', 'u', 'd', 'xu', 'xd'])

    traces = {'UP': go.Scatter(x=df.x,
                               y=df.xu,
                               fill='tozeroy',
                               name='GPD_UP (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2)),
              'DN': go.Scatter(x=df.x,
                               y=df.xd,
                               fill='tozeroy',
                               name='GPD_DOWN (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2))}

    data = list(traces.values())
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
