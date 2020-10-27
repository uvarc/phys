import redis
from colorama import Fore


class FemtoDB:
    def __init__(self, host='localhost', port=6379):
        self.db = redis.Redis(host=host, port=port)

    def get_model_list(self):
        """
            Helper function used to return a list of models available for analysis.
        """

        models = []
        for key in self.db.keys():
            models.append(key.decode())

        return models


    def get_parameter_limits(self, model, parameter, dtype=float):
        """
            Get model parameter limits form database.
        """
        try:
            if self.db.exists(model) == 0:
                raise Exception('ModelException')

        except Exception as ex:
            print(Fore.RED + '{}: Model does not exists in database.'.format(ex) + Fore.WHITE)

        return tuple(map(dtype, self.db.hget(model, parameter).decode().split(':')))

    def add_model(self, name=None, origin=None, xbj_limits=None, t_limits=None, q2_limits=None, model_dict=None):
        """
            Add new models to Redis database.
        """
        try:
            if self.db.exists(name):
                raise Exception('ModelException')
        except Exception as ex:
            print(Fore.RED + '{}: Model exists in database already.'.format(ex) + Fore.WHITE)

        if model_dict is not None:
            model = model_dict
        else:
            model = {'origin': origin,
                     'xbj_limits': xbj_limits,
                     't_limits': t_limits,
                     'q2_limits': q2_limits}

        for key, value in model.items():
            try:
                self.db.hset(name, key, value)
            except ValueError as ex:
                print(Fore.RED + 'Database error: {}', format(ex.args) + Fore.WHITE)
