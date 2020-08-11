import numpy
import pandas
import pandas as pd
import numpy as np
import bisect
import os

from tqdm import tqdm
from itertools import chain


class FemtoMesh:
    def __init__(self, name):
        self.data_frame = None
        self.data_frame_name = name
        self.chunksize = 1000000
        self.model_generated = False

        self._xbj = 0
        self._t = 0
        self._q2 = 0

    def build_data_frame(self, xbj: 'float', t: 'float') -> 'pandas.DataFrame':
        """
        Build PANDAS DataFrame from mesh csv. The mesh values are read in chucks keeping only
        the relevant data points to reduce the file size.

        xbj: x-bjorken
        t: proton momentum transfer

        """
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

    def build_data_frame_heat(self, t: 'float') -> 'pandas.DataFrame':
        """
        Build PANDAS DataFrame from mesh csv. The mesh values are read in chucks keeping only
        the relevant data points to reduce the file size.

        t: proton momentum transfer

        """

        df_list = []
        for chunk in pd.read_csv(self.data_frame_name, dtype=float, chunksize=self.chunksize):
            df = chunk[chunk.t == t]
            if df.empty:
                pass
            else:
                df_list.append(df)

        return pd.concat(df_list)

    @property
    def xbj(self) -> 'float':
        return self._xbj

    @xbj.setter
    def xbj(self, xbj: 'float'):
        self._xbj = xbj

    @property
    def t(self) -> 'float':
        return self._t

    @t.setter
    def t(self, t: 'float'):
        self._t = t

    @property
    def q2(self) -> 'float':
        return self._q2

    @q2.setter
    def q2(self, q2: 'float'):
        self._q2 = q2

    @staticmethod
    def search(v: 'numpy.array', value: 'float') -> 'float, float':
        """
        Search for specific value in array v and return former and prior value in list.

        value: value to search for in list
        v: list of possible values
        """
        i = bisect.bisect_left(v, value)

        return v[i], v[i - 1]

    @staticmethod
    def extrapolate(value: 'float', u_gpd: 'float', l_gpd: 'float', u_value: 'float', l_value: 'float') -> 'float':
        """
        Determine local relationship between Q2 and quark GPD values in a kinematic range; assumes a linear
        relationship. The slope and intercept are then used to determine the GPD value(s) at a Q2 of value.

        value: Q2 value to determine GPD
        u_gpd: upper GPD value
        l_gpd: lower GPD value
        l_value: lower Q2 value
        u_value: upper Q2 value
        """

        m = (u_gpd - l_gpd) / (u_value - l_value)
        b = l_gpd - m * l_value
        return m * value + b

    def model_to_csv(self):
        """
        Convert GPD model DataFrame to csv file
        """
        try:
            assert self.model_generated is True
            self.data_frame.to_csv("gpd_model.csv", index=False, header=['x', 'u', 'd', 'xu', 'xd'])
        except AssertionError as ex:
            print('Model {0} not saved. Returned {1}'.format(self.data_frame_name, ex))

    @staticmethod
    def model_search() -> 'list':
        """
        Search model directory for all listed GPD models and return list for selection on frontend.
        """
        models = []
        try:
            models = os.listdir('./data/models/')
            assert len(models) > 0, 'No models returned.'

        except AssertionError as ex:
            print('{0}:{1} >\tNo model files found.'.format(ex, __name__))

        return models

    def process(self) -> 'pandas.DataFrame':
        """
        Process is the main worker function of Femtomesh. The method builds the model for a given kinematic
        region and then determines the UP and DOWN quark GPDs for every value of x at a given Q2. A new DataFrame
        built containing the new information and returned to the user for plotting and analysis.
        """
        gpd_value_u = np.array([])
        gpd_value_d = np.array([])

        dff = self.build_data_frame(self.xbj, self.t)
        x_value = dff['x'].unique()

        for x in x_value:
            sub_df = dff[dff.x == x][['Q2', 'gpd_u', 'gpd_d']]

            upper, lower = self.search(sub_df.Q2.to_numpy(), self._q2)

            df_upper = sub_df[sub_df.Q2 == upper][['gpd_u', 'gpd_d']]
            df_lower = sub_df[sub_df.Q2 == lower][['gpd_u', 'gpd_d']]

            gpd_upper_u = df_upper.gpd_u.iloc[0]
            gpd_lower_u = df_lower.gpd_u.iloc[0]
            gpd_upper_d = df_upper.gpd_d.iloc[0]
            gpd_lower_d = df_lower.gpd_d.iloc[0]

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

    def process_heat(self) -> 'pandas.DataFrame':
        x_value = np.array([])
        xbj_value = np.array([])
        gpd_value_u = np.array([])
        gpd_value_d = np.array([])

        dff = self.build_data_frame_heat(self.t)

        iters = [(i, j) for i in dff['x'].unique() for j in dff['xbj'].unique()]
        total_elements = 0.5 * len(list(chain.from_iterable(iters)))
        progress_bar = tqdm(total=total_elements)

        for x, xbj in iters:
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
            progress_bar.update(1)
        progress_bar.close()

        d_frame = pd.DataFrame({'x': x_value,
                                'xbj': xbj_value,
                                'u': gpd_value_u,
                                'd': gpd_value_d})

        d_frame['xu'] = d_frame['x'] * d_frame['u']
        d_frame['xd'] = d_frame['x'] * d_frame['d']

        self.model_generated = True
        self.data_frame = d_frame

        return d_frame
