from wc import stopwords
from Levenshtein import distance
import numpy as np
import pandas as pd

################################################################
stopwords = set(stopwords.split('\n'))
stopwords.add('several')
stopwords.add('ii')
stopwords.add('rr')


def filter_word_lists(df):

    def format_description(x):
        if not x:
            return x
        if isinstance(x, str):
            x = x.split('\n')

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
        return [e for e in x]

    df['Description'] = df['Course Title'].apply(
        format_description) + df['Description'].apply(format_description)
    df['Description'] = df['Description'].apply(lambda x: list(set(x)))

    df['Learning outcomes'] = df['Learning outcomes'].apply(format_description)
    df['Pre-requisites'] = df['Pre-requisites'].apply(format_description)

    # df = df.drop(columns=['URL', 'Degree'])
    return df

################################################################


def word_to_cloud_distance(word, cloud):
    if not cloud:
        return 5e15

    distances = []
    cloud = list(cloud)
    for w in cloud:
        distances.append(distance(word, w))
    idx = np.array(distances).argmin()
    return np.array(distances).min(), cloud[idx]
################################################################


def cloud_to_cloud_distances(cloud1, cloud2):
    if not cloud1:
        return 5e15
    distances = []
    for w in cloud1:
        d, closest_word = word_to_cloud_distance(w, cloud2)
        distances.append(d)
    return np.mean(distances)

################################################################


def cloud_to_cloud_score(cloud1, cloud2, threshold=1):
    if not cloud1:
        return 5e15
    num_perfect_match = 0
    closests_words = []
    for w in cloud1:
        d, closest_word = word_to_cloud_distance(w, cloud2)
        if d <= threshold:
            num_perfect_match += 1
            closests_words.append(closest_word)
    return num_perfect_match, closests_words

################################################################


def find_matching_classes(df1, df2, field='Description'):

    df1 = filter_word_lists(df1)
    df2 = filter_word_lists(df2)

    matching_classes = {}

    for i, _class1 in df1.iterrows():
        correlation_distance = []
        correlation_match = []
        for idx, _class2 in df2.iterrows():
            d = cloud_to_cloud_distances(
                _class1[field],
                _class2[field])
            if d < 50000:
                correlation_distance.append((idx, d, _class2['Course Title']))

            num_match, closests_words = cloud_to_cloud_score(
                _class1[field],
                _class2[field])

            correlation_match.append(
                (idx, num_match, _class2['Course Title'],
                 closests_words
                 ))

        correlation_distance = pd.DataFrame(correlation_distance, columns=[
            'original_index', 'Distance', 'Course Title'])
        correlation_match = pd.DataFrame(correlation_match, columns=[
            'original_index', 'Number Match', 'Course Title', 'closest_words'])

        correlation_distance = correlation_distance.sort_values(by=[
                                                                'Distance'])
        correlation_distance = correlation_distance.iloc[:4]
        correlation_match = correlation_match.sort_values(by=[
            'Number Match'], ascending=False)
        correlation_match = correlation_match.iloc[:6]
        matching_classes[i] = correlation_match
    return matching_classes

################################################################
