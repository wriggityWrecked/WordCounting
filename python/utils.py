from datetime import datetime
import pickle
import json
import os
from counter_stats import CounterStats  # needed for main


def get_filename(filename, extension):
    """
    Append the current date to the input filename.

    :param filename:
    :param extension:
    :return:
    """
    now = datetime.now()
    return filename + '_' + now.strftime("%Y-%m-%dT%H-%M-%S") + '.' + extension


def save_json_data(data, filename):
    """
    Save the input data as a JSON file.

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
    """
    Using this method to load CounterStats will require the following import:
    from counter_stats import CounterStats

    :param file_name:
    :return:
    """
    with open(file_name, 'rb') as opened_file:
        return pickle.load(opened_file)


def make_directory(path):
    """
    Create a directory if it does not exist
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    print load_pickle_counter_stats('realDonaldTrump_pickle_2018-06-07T23-14-15.pkl')
