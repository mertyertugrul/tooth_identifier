import warnings

import pandas as pd
import joblib
from sklearn import preprocessing

from SentenceParcerForTenses import tense_predictorH, sentence_parser, sentence_adder

warnings.filterwarnings("ignore")  # Don't want to see the warnings in the notebook

df = pd.read_csv('SentenceToTenses.csv', sep=',')
df.drop(['Unnamed: 0'], inplace=True, axis=1)
df_columns = df.columns.tolist()
columnsForDummies = df_columns[1:len(df_columns) - 1]
dfd = pd.get_dummies(df, drop_first=True, columns=columnsForDummies)
label_encoder = preprocessing.LabelEncoder()
df['tense'] = label_encoder.fit_transform(df['tense'])
dt = joblib.load('tense_dt_model')
