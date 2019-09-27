from flask import Flask, request
from flask_restful import Resource, Api

import spacy
import pandas as pd
import numpy as np
import joblib
import json
import re
import os
from math import sqrt
from tika import parser
import PyPDF2
from tqdm import tqdm

from TextComplexityReader import *
from tooth_tenser import *
from SentenceParcerForTenses import sentence_parser as snt_parser
from SentenceParcerForTenses import tense_predictorH as tns_predictorH


app = Flask(__name__)
api = Api(app)

model = joblib.load('/Users/mertmacbook/Google Drive/Tooth Identifier/article_smote_rf_model')



class HelloWorld(Resource):
    def get(self):
        return {"About": "Hello World"}

    def post(self):
        text = str(request.get_data().decode('unicode_escape'))
        if len(text)>=100:
            df_get = get_article_df('Web Text', text)
            df2 = df_get
            result_json = df_get.to_json(orient='index')
            result_dic = json.loads(result_json)

            prediction = get_article_prediction(df2, model)
            print(type(np.array2string(prediction)))
            print(np.array2string(prediction))
            print(type(result_dic))
            result_dic['Prediction'] = np.array2string(prediction)
            result_json = json.dumps(result_dic, ensure_ascii=False)

            return result_json, 201
        else:
            print(type(text))
            parsed = snt_parser(text, print_sent=False)
            print(type(parsed))
            tense = tns_predictorH(parsed, df, dfd, dt, label_encoder)
            print(type(tense[0]))
            print(tense[0])
            # parsed = sentence_parser(text, print_sent=False)
            # tense = tense_predictorH(parsed, df, dfd, dt, label_encoder)
            # print(type(tense))
            tense_json = {"Tense": tense[0]}


            return tense_json


class Multi(Resource):
    def get(self, num):
        return {"result": num * 10}


api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
