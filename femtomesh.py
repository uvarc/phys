import pandas as pd
import numpy as np
import bisect
import os


class FemtoMesh:
    def __init__(self, name):
        self.data_frame = None
        self.data_frame_name = name
        self.chunksize = 1000000
        self.model_generated = False

        self._xbj = 0
        self._t = 0
        self._q2 = 0

    def build_data_frame(self, xbj, t):
        df_list = []
        try:
            for chunk in pd.read_csv(self.data_frame_name, dtype=float, chunksize=self.chunksize):
                df = chunk[(chunk.xbj == xbj) & (chunk.t == t)]
                if df.empty:
                    pass
                else:
                    df_list.append(df)
        except FileNotFoundError as ex:
            print('{0}:{1} >\tFile not found.'.format(ex, __name__))

        return pd.concat(df_list)

    def build_data_frame_heat(self, t):
        df_list = []
        for chunk in pd.read_csv(self.data_frame_name, dtype=float, chunksize=self.chunksize):
            df = chunk[chunk.t == t]
            if df.empty:
                pass
            else:
                df_list.append(df)

        return pd.concat(df_list)

    @property
    def xbj(self):
        return self._xbj

    @xbj.setter
    def xbj(self, xbj):
        self._xbj = xbj

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t = t

    @property
    def q2(self):
        return self._q2

    @q2.setter
    def q2(self, q2):
        self._q2 = q2

    @staticmethod
    def search(v, value):
        i = bisect.bisect_left(v, value)

        return v[i], v[i - 1]

    @staticmethod
    def extrapolate(value, u_gpd, l_gpd, u_value, l_value):
        m = (u_gpd - l_gpd) / (u_value - l_value)
        b = l_gpd - m * l_value
        return m * value + b

    def model_to_csv(self):
        try:
            assert self.model_generated is True
            self.data_frame.to_csv("gpd_model.csv", index=False, header=['x', 'u', 'd', 'xu', 'xd'])
        except AssertionError as ex:
            print('Model {0} not saved. Returned {1}'.format(self.data_frame_name, ex))

    @staticmethod
    def model_search():
        models = []
        try:
            models = os.listdir('./data/models/')
            assert len(models) > 0, 'No models returned.'

        except AssertionError as ex:
            print('{0}:{1} >\tNo model files found.'.format(ex, __name__))

        return models

    def process(self):
        x_value = np.array([])
        gpd_value_u = np.array([])
        gpd_value_d = np.array([])

        dff = self.build_data_frame(self.xbj, self.t)

        for x in dff['x'].unique():
            x_value = np.append(x_value, x)

            sub_df = dff[dff['x'] == x][['Q2', 'gpd_u', 'gpd_d']]

            upper, lower = self.search(dff[dff['x'] == x]['Q2'].to_numpy(), self._q2)

            gpd_upper_u = sub_df[sub_df['Q2'] == upper]['gpd_u'].iloc[0]
            gpd_lower_u = sub_df[sub_df['Q2'] == lower]['gpd_u'].iloc[0]
            gpd_upper_d = sub_df[sub_df['Q2'] == upper]['gpd_d'].iloc[0]
            gpd_lower_d = sub_df[sub_df['Q2'] == lower]['gpd_d'].iloc[0]

            gpd_value_u = np.append(gpd_value_u, self.extrapolate(self._q2, gpd_upper_u, gpd_lower_u, upper, lower))
            gpd_value_d = np.append(gpd_value_d, self.extrapolate(self._q2, gpd_upper_d, gpd_lower_d, upper, lower))

        d_frame = pd.DataFrame({'x': x_value,
                                'u': gpd_value_u,
                                'd': gpd_value_d})

        d_frame['xu'] = d_frame['x'] * d_frame['u']
        d_frame['xd'] = d_frame['x'] * d_frame['d']

        self.model_generated = True
        self.data_frame = d_frame

        return d_frame

    def process_heat(self):
        x_value = np.array([])
        xbj_value = np.array([])
        gpd_value_u = np.array([])
        gpd_value_d = np.array([])

        dff = self.build_data_frame_heat(self.t)

        for x, xbj in zip(dff['x'].unique(), dff['xbj'].unique()):
            x_value = np.append(x_value, x)
            xbj_value = np.append(xbj_value, xbj)

            sub_df = dff[(dff.x == x) & (dff.xbj == xbj)][['Q2', 'gpd_u', 'gpd_d']]

            upper, lower = self.search(dff[(dff.x == x) & (dff.xbj == xbj)]['Q2'].to_numpy(), self._q2)

            gpd_upper_u = sub_df[sub_df['Q2'] == upper]['gpd_u'].iloc[0]
            gpd_lower_u = sub_df[sub_df['Q2'] == lower]['gpd_u'].iloc[0]
            gpd_upper_d = sub_df[sub_df['Q2'] == upper]['gpd_d'].iloc[0]
            gpd_lower_d = sub_df[sub_df['Q2'] == lower]['gpd_d'].iloc[0]

            gpd_value_u = np.append(gpd_value_u, self.extrapolate(self._q2, gpd_upper_u, gpd_lower_u, upper, lower))
            gpd_value_d = np.append(gpd_value_d, self.extrapolate(self._q2, gpd_upper_d, gpd_lower_d, upper, lower))

        d_frame = pd.DataFrame({'x': x_value,
                                'xbj': xbj_value,
                                'u': gpd_value_u,
                                'd': gpd_value_d})

        d_frame['xu'] = d_frame['x'] * d_frame['u']
        d_frame['xd'] = d_frame['x'] * d_frame['d']

        self.model_generated = True
        self.data_frame = d_frame

        return d_frame
