import spacy
import pandas as pd
from IPython.core.display import display
from pandas import DataFrame
import numpy as np
import joblib
import pickle

# dt_model = joblib.load('Tense Model')


nlp = spacy.load('en_core_web_sm')


##
# To get dummy columns
##

def dummy_columns_create():
    df = pd.read_csv('SentenceToTenses.csv', sep=',')

    # df.drop(['Unnamed: 0', 'time_exp1', 'time_exp2', 'time_exp3', 'time_exp4', 'time_exp5'], inplace=True, axis=1)

    df.drop(['Unnamed: 0'], inplace=True, axis=1)

    df_columns = df.columns.tolist()

    columns_for_dummies = df_columns[1:]

    dfd = pd.get_dummies(df, drop_first=True, columns=columns_for_dummies)

    dfd = dfd.drop(['text'], axis=1)

    dummy_col_list = dfd.columns.tolist()

    return dummy_col_list


# dummy_columns = ['verb1_verb, modal auxiliary',
#                  'verb1_verb, non-3rd person singular present', 'verb1_verb, past tense',
#                  'verb2_verb, gerund or present participle',
#                  'verb2_verb, non-3rd person singular present',
#                  'verb2_verb, past participle', 'verb2_verb, past tense',
#                  'verb3_verb, gerund or present participle',
#                  'verb3_verb, non-3rd person singular present',
#                  'verb3_verb, past participle', 'verb3_verb, past tense',
#                  'verb4_verb, gerund or present participle',
#                  'verb4_verb, non-3rd person singular present',
#                  'verb4_verb, past participle', 'verb4_verb, past tense',
#                  'verb5_verb, base form', 'verb5_verb, non-3rd person singular present',
#                  'adverb1_ever', 'adverb1_finally', 'adverb1_later', 'adverb1_nan',
#                  'adverb1_now', 'adverb1_right', 'adverb2_later', 'adverb2_long',
#                  'adverb2_nan', 'adverb2_now', 'adverb2_yet',
#                  'tense_future perfect progressive', 'tense_future progressive',
#                  'tense_past perfect', 'tense_past perfect progressive',
#                  'tense_past progressive', 'tense_perfect past', 'tense_perfect present',
#                  'tense_perfect progressive past', 'tense_perfect progressive present',
#                  'tense_present perfect', 'tense_present perfect progressive',
#                  'tense_present progressive', 'tense_progressive future',
#                  'tense_progressive past', 'tense_progressive present',
#                  'tense_simple future', 'tense_simple past', 'tense_simple present',
#                  'tense_simple progressive']

time_expressions = [
    'every', 'day', 'week', 'month', 'year', 'evening', 'noon', 'afternoon', 'weekend', 'present', 'presently',
    'days', 'weeks', 'months', 'years',
    'usually', 'generally', 'regularly', 'frequently', 'anymore', 'weekends', 'sometimes', 'sometime',
    'habitually', 'repeatedly', 'once', 'twice', 'being', 'rarely',
    'times', 'now', 'right', 'just', 'currently', 'nowadays', 'constantly', 'continuously',
    'moment', 'yesterday', 'last', 'ago', 'morning', 'night',
    'when', 'as', 'while', 'since',
    'for', 'lately', 'recently', 'ever',
    'never', 'always', 'seldom', 'rarely',
    'often', 'already', 'yet', 'today', 'tonight',
    'this', 'today', 'before', 'by', 'these',
    'time', 'tomorrow', 'so', 'far',
    'few', 'days', 'past', 'until',
    'soon', 'next', 'general', 'generally',
    'moment'
]


def sentence_table(sentence):
    """
    Split any sentece into tokens and tags hem
    :param sentence: sentence in English should be a Spacy NLP object
    """
    print(f"{'TEXT':{10}} {'POS':{8}} {'TAG':{7}} {'Tag Explained':{44}} {'Is Alpha':{9}} {'Is Stop':{8}} {'Num':{8}}")
    print('--------------------------------------------------------------------------------------------------')
    for token in sentence:
        print(f"{token.text:{10}} {token.pos_:{8}} {token.tag_:{7}} {spacy.explain(token.tag_):{44}}\
 {str(token.is_alpha):{9}} {str(token.is_stop):{8}} {str(token.like_num):{8}}")
    print('--------------------------------------------------------------------------------------------------')
    print('\n')


def verb_counter(sentence):
    """
    Counts the words in the sentence
    :param sentence: sentence in English should be a Spacy NLP object
    :return: number of verb in integer
    """
    count = 0
    for token in sentence:
        if token.pos_ == 'VERB':
            count += 1
    return count


def adverb_counter(sentence):
    """
    Counts the adverb in the sentence
    :param sentence: sentence in English should be a Spacy NLP object
    :return: number of adverb in integer
    """
    count = 0
    for token in sentence:
        if token.tag_ == 'RB':
            count += 1
    return count


def time_expressions_counter(sentence):
    count = 0
    for token in sentence:
        if token.text.lower() in time_expressions:
            count += 1
    return count


def analyse_sentence(sentence, tense=None):
    """
    Analyse the sentence and put values in proper parameters
    :param sentence: sentence in English should be a Spacy NLP object
    :param tense: tense of the sentence
    :return: tag of every verb and adverb in dictionary form
    """
    dic = {}
    verb_counter: int = 0
    time_phrases_counter_counter: int = 0
    dic['text'] = sentence.text
    if tense is not None:
        dic['tense'] = tense
    else:
        dic['tense'] = ''
    for token in sentence:
        if token.pos_ == 'VERB':
            dic['verb' + str(verb_counter + 1)] = spacy.explain(token.tag_)
            verb_counter += 1
        if token.text.lower() in time_expressions:
            dic['time_exp' + str(time_phrases_counter_counter + 1)] = token.text
            time_phrases_counter_counter += 1
    return dic


def dic_to_list(dic):
    """
    Reformat analyse of the sentence in dictionary format to list format
    so it can be used on data frames
    :param dic: analyse of the sentence in dictionary format
    :return: analyse of the sentence in list format
    """
    t_dic = dic
    d_list = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
    d_list[0] = t_dic['text']
    t_dic.pop('text', None)
    # columnC = 1
    for k, v in t_dic.items():
        if k[:-1] == 'verb':
            d_list[int(k[-1:])] = v
        elif k[:-1] == 'time_exp':
            d_list[6 + int(k[-1:])] = v
        elif k == 'tense':
            d_list[len(d_list) - 1] = v
    return d_list


def sentence_adder(sentence, tense, csv_file=None, num_col=False, print_it=True):
    """
    Insert any sentence with proper tense tag to .csv file
    :param print_it: If true prints parsed sentence and tail of the dataframe otherwise print numbers of records
    :param num_col: If there is a column for row numbers make it True
    :param sentence: sentence in English should be a Spacy NLP object
    :param tense: tense of the sentence
    :param csv_file: .csv file to save to
    """
    doc = nlp(sentence)
    if print_it:
        sentence_table(doc)
    dic = analyse_sentence(doc, tense)
    dic_list = dic_to_list(dic)
    df = pd.read_csv(csv_file)
    if num_col:
        df = df.drop(df.columns[0], axis=1)  # drop number column
    # if len(df.columns) > 9:
    #     df = df.drop(df.columns[13], axis=1)  # drop last adverb
    #     df = df.drop(df.columns[6:11], axis=1)  # drop unnecessary verb columns
    df = df.append(pd.Series(dic_list, index=df.columns), ignore_index=True)
    if csv_file is None:
        df.to_csv('wordsForGrammerChecker.csv', encoding='utf-8')
    else:
        df.to_csv(csv_file, encoding='utf-8')
    if print_it:
        display(df.tail(1))
    else:
        print(df.shape)


def dic_maker(r_list, r_col):
    """
    Make dictionary with given column names and values
    :param r_list: values of the keys
    :param r_col: keys of the dictionary
    :return: dictionary of the sentence with columns
    """
    dic = dict(zip(r_col, r_list))
    return dic


def sentence_parser(sentence, print_sent=True):
    """
    Parse the sentence into parts of verbs, adverbs and tense, then create
    data frame
    :param print_sent: True will print tne detailed sentence
    :param sentence: sentence in English should be a Spacy NLP object
    :return: data frame of the sentence in Pandas DataFrame object
    """
    doc = nlp(sentence)
    if print_sent:
        sentence_table(doc)
    dic = analyse_sentence(doc)
    dic_list = dic_to_list(dic)
    columns = ['text', 'verb1', 'verb2', 'verb3', 'verb4', 'verb5', 'verb6', 'time_exp1', 'time_exp2', 'time_exp3',
               'time_exp4', 'time_exp5', 'tense']
    dic_df = dic_maker(dic_list, columns)

    dfs: DataFrame = pd.DataFrame(dic_df, index=[0])
    return dfs


def tense_predictorH(sentence_df, model_df, model_df_d, model, encoder=None):
    """
    Return the tense of the sentence
    :param encoder: label encoder of the model
    :param model_df: dataframe of the model
    :param model_df_d: dummified datafare of the model
    :param sentence_df: sentence to find out its tense in Pandas DataFrame object
    :param model: Scikit-Learn model use for prediction
    :return: tense of the sentence in Pandas DataFrame object
    :rtype: DataFrame
    """

    if 'Unnamed: 0' in sentence_df.columns:
        sentence_df.drop(['Unnamed: 0'], inplace=True, axis=1)

    df_columns = model_df.columns.tolist()
    columnsForDummies = df_columns[1:]
    df_td = pd.get_dummies(sentence_df, drop_first=False, columns=columnsForDummies)

    for col in model_df_d.columns.tolist():
        if col not in df_td.columns:
            df_td[col] = 0

    for d_col in df_td.columns:
        if d_col not in model_df_d.columns.tolist():
            df_td = df_td.drop([d_col], axis=1)

    df_td = df_td.reindex(model_df_d.columns, axis=1)

    df_td.to_csv('sen_test.csv')

    X = np.array(df_td.drop(['text', 'tense'], axis=1))

    if encoder is None:
        prediction = model.predict(X)
    else:
        prediction = encoder.inverse_transform(model.predict(X))

    return prediction
