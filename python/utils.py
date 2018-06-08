from datetime import datetime
import pickle
import json
from counter_stats import CounterStats

def get_filename(prepend, extension):
    """

    :param prepend:
    :param extension:
    :return:
    """
    now = datetime.now()
    return prepend + '_' + now.strftime("%Y-%m-%dT%H-%M-%S") + '.' + extension

def save_json_data(data, filename):
    """
    Pickle a counter_stats import CounterStats named tuple

    :param data:
    :param filename:
    :return:
    """
    with open(filename, 'w') as file_to_save:
        json.dump(data, file_to_save)

def save_pickle_counter_stats(data, filename):
    """
    Un-pickle a counter_stats import CounterStats named tuple

    :param data:
    :param filename:
    :return:
    """
    with open(filename, 'w') as file_to_save:
        pickle.dump(data, file_to_save)

def load_pickle_counter_stats(file_name):

    with open(file_name, 'rb') as opened_file:
        return pickle.load(opened_file)

if __name__ == "__main__":
    print load_pickle_counter_stats('realDonaldTrump_pickle_2018-06-07T23-14-15.pkl')