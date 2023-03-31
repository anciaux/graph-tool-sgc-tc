from wc import stopwords
from Levenshtein import distance
import numpy as np
import pandas as pd

################################################################
stopwords = set(stopwords.split('\n'))
stopwords.add('several')


def filter_word_lists(df):

    def format_description(x):
        if not x:
            return x
        w_list = []
        for e in x:
            w_list += [e.strip() for e in e.split(' ') if e.strip() != '']

        def replace_punctuation(e):
            reps = '+-./%,:;_=?~1234567890()'
            for c in reps:
                e = e.replace(c, '')
            return e
        w_list = [replace_punctuation(e).lower() for e in w_list]
        w_list = [e for e in w_list if e != '']

        x = set(w_list)
        x = x-stopwords
        return x

    df['Description'] = df['Description'].apply(format_description)
    df['Learning outcomes'] = df['Learning outcomes'].apply(format_description)
    df['Pre-requisites'] = df['Pre-requisites'].apply(format_description)

    df = df.drop(columns=['URL', 'Degree'])
    return df

################################################################


def word_to_cloud_distance(word, cloud):
    if not cloud:
        return 5e15

    distances = []
    for w in cloud:
        distances.append(distance(word, w))
    return np.array(distances).min()
################################################################


def cloud_to_cloud_distances(cloud1, cloud2):
    if not cloud1:
        return 5e15
    distances = []
    for w in cloud1:
        distances.append(word_to_cloud_distance(w, cloud2))
    return np.mean(distances)

################################################################


def find_matching_classes(df1, df2, field='Description'):
    matching_classes = {}

    for i, _class1 in df1.iterrows():
        correlation = []
        for idx, _class2 in df2.iterrows():
            d = cloud_to_cloud_distances(
                _class1[field],
                _class2[field])
            if d < 50000:
                correlation.append((idx, d, _class2['Course Title']))
        correlation = pd.DataFrame(correlation, columns=[
                                   'original_index', 'Distance', 'Course Title'])
        correlation = correlation.sort_values(by=['Distance'])
        correlation = correlation.iloc[:4]
        matching_classes[i] = correlation
    return matching_classes

################################################################
