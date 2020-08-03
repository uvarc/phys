import plotly.graph_objects as go
import femtomesh as fm
import timeit

if __name__ == "__main__":
    start = timeit.default_timer()

    mesh = fm.FemtoMesh('data/GPD_H.csv')
    mesh.xbj = 0.0001     # This should come from the front-end
    mesh.t = -0.1         # This should come from the front-end
    mesh.q2 = 6           # This should come from the front-end

    df = mesh.process()

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    figure = go.Figure()

    figure.add_trace(go.Scatter(x=df.x,
                                y=df.xu,
                                fill='tozeroy',
                                name='GPD_UP (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2)))
    figure.add_trace(go.Scatter(x=df.x,
                                y=df.xd,
                                fill='tozeroy',
                                name='GPD_DOWN (xbj={0}, t={1}, q2={2})'.format(mesh.xbj, mesh.t, mesh.q2)))
    figure.update_layout(
        xaxis={
            'title': 'x'},
        yaxis={'title': 'GPD'})

    figure.show()
