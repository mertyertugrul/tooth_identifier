import os
import sys

import spacy
import pandas as pd
import numpy as np
import lorem
import re
from math import sqrt
from tqdm import tqdm_notebook, tqdm
import codecs

from IPython.core.display import display
import PyPDF2
from tooth_tenser import *

nlp = spacy.load('en_core_web_lg')

advance_vocab_df = pd.read_csv('vocabulary.csv')  # Advanced words
common_vocab_df = pd.read_csv('common.csv')  # Common Words


def syllables(word):
    """
    returns the number of syllables of a given word
    :param word: single word in string format
    :return: number of syllables
    """
    syllable_count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count


def check_verb(token):
    """Check verb type given spacy token
    :param token: single verb in a sting format
    :return: linguistic type of verb
    """
    indirect_object = False
    direct_object = False
    if token.tag_ == 'BES':
        return 'TOBEVERB'
    for item in token.children:
        if item.dep_ == "iobj" or item.dep_ == "pobj":
            indirect_object = True
        if item.dep_ == "dobj" or item.dep_ == "dative":
            direct_object = True
    if indirect_object and direct_object:
        return 'DITRANVERB'
    elif direct_object and not indirect_object:
        return 'TRANVERB'
    elif not direct_object and not indirect_object:
        return 'INTRANVERB'
    else:
        return 'VERB'


def word_finder(vocab, word):
    """
    Finds the verb in a given vocabulary
    :param vocab: vocabulary in dataformat
    :param word: word to look in vocabulary list
    :return: boolean, whether the word in the vocabulary or not
    """
    doc = nlp(word)
    if doc[0].is_punct is False:
        try:
            result = vocab.word.str.contains(r'(?:\s|^)' + word + '(?:\s|$)').any()
        except:
            result = False
        if result:
            return True
        else:
            return False
    else:
        return False


def is_advanced(word):
    """
    Checks the word is in advance vocabulary
    :return: boolean
    :param word: word to look at
    """
    return word_finder(advance_vocab_df, word)


def is_common(word):
    """
    Checks the word is in common vocabulary
    :param word: word to look at
    :return: boolean
    """
    return word_finder(common_vocab_df, word)


def feature_computer(doc):
    """
    Creates and calculate features of the article
    :param doc: tokenized article, spacy object
    :return: dictionary of the features
    """
    result = {}
    # Linguistic
    c_syllable = 0
    c_monosylable = 0
    c_disyllable = 0
    c_complex_word = 0
    c_word = 0
    c_sentence = 0
    c_character = 0
    c_advance = 0
    c_common = 0
    c_paragraph = 0
    # Word Usage
    c_ditransverb = 0
    c_transverb = 0
    c_intransverb = 0
    c_verb = 0
    c_conjunction = 0
    c_auxverb = 0
    c_noun = 0
    c_punct = 0
    c_adjective = 0
    c_adposition = 0
    c_adverb = 0
    c_pronoun = 0
    c_unknown = 0
    # Tenses
    c_present_simple = 0
    c_past_simple = 0
    c_future_simple = 0
    c_past_progressive = 0
    c_present_progressive = 0
    c_future_progressive = 0
    c_present_perfect = 0
    c_past_perfect = 0
    c_future_perfect = 0
    c_present_perfect_progressive = 0
    c_past_perfect_progressive = 0
    c_future_perfect_progressive = 0
    tense_passed = False
    c_tense_passed = 1

    for sent in tqdm(doc.sents, total=len(list(doc.sents))):
        c_sentence += 1
        try:
            parsed = sentence_parser(sent.text, print_sent=False)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, ' - ', c_tense_passed)
            print(str(e))
            tense_passed = True
            c_tense_passed += 1
            pass
        if tense_passed is False:
            tense = tense_predictorH(parsed, df, dfd, dt, label_encoder)
            if tense == 'present simple':
                c_present_simple += 1
            if tense == 'past simple':
                c_past_simple += 1
            if tense == 'future simple':
                c_future_simple += 1
            if tense == 'past progressive':
                c_past_progressive += 1
            if tense == 'present progressive':
                c_present_progressive += 1
            if tense == 'future progressive':
                c_future_progressive += 1
            if tense == 'present perfect':
                c_past_perfect += 1
            if tense == 'present perfect progressive':
                c_present_perfect_progressive += 1
            if tense == 'past perfect progressive':
                c_past_perfect_progressive += 1
            if tense == 'future perfect progressive':
                c_future_perfect_progressive += 1
            if tense == 'future perfect':
                c_future_perfect += 1
            if tense == 'past perfect':
                c_past_perfect += 1

        for token in sent:
            if token.is_stop is False and token.is_punct is False:
                # Number of words
                c_word += 1
                # Number of characters
                c_character += len(token.text)
                # Syllables
                num_syllable = syllables(token.text)
                if num_syllable == 1:
                    c_monosylable += 1
                if num_syllable == 2:
                    c_disyllable += 1
                if num_syllable >= 3:
                    c_complex_word += 1
                c_syllable += num_syllable
                # Advance Word
                if is_advanced(token.text):
                    c_advance += 1
                # Common Word
                if is_common(token.text):
                    c_common += 1
                # Paragraph
                if token.is_space:
                    c_paragraph += 1
                # Word Usage
                if token.pos_ == 'VERB':
                    verb = check_verb(token)
                    if verb == 'DITRANVERB':
                        c_ditransverb += 1
                    elif verb == 'TRANVERB':
                        c_transverb += 1
                    elif verb == 'INTRANVERB':
                        c_intransverb += 1
                    c_verb += 1
                elif token.tag_ == 'CC' or token.pos_ == 'CCONJ' or token.pos_ == 'CONJ' or token.pos_ == 'SCONJ':
                    c_conjunction += 1
                elif token.pos_ == 'AUX':
                    c_auxverb += 1
                elif token.pos_ == 'NOUN':
                    c_noun += 1
                elif token.pos_ == 'PUNCT':
                    c_punct += 1
                elif token.pos_ == 'ADJ':
                    c_adjective += 1
                elif token.pos_ == 'ADP':
                    c_adposition += 1
                elif token.pos_ == 'ADV':
                    c_adverb += 1
                elif token.pos_ == 'PRON' or token.pos_ == 'PROPN':
                    c_pronoun += 1
                elif token.pos_ == 'X':
                    c_unknown += 1
        c_tense_passed = False

    # Score calculating
    dale_chall_score = (0.1579 * (100 - (c_common / c_word * 100))) + (0.0496 * (c_word / c_sentence))
    Flesch_Reading_Ease_Score = 206.835 - (1.015 * c_word / c_sentence) - (84.6 * c_syllable / c_word)
    new_flesch_reading_ease_score = (1.599 * c_monosylable / c_word * 100) - (1.015 * c_word / c_sentence) - 31.517
    gunning_fog_score = 0.4 * ((c_word / c_sentence) + ((c_complex_word / c_word) * 100))
    smog_score = 3 + sqrt((c_disyllable + c_complex_word) / c_word * 30)
    forcast_score = 20 - (((c_monosylable / c_word) * 150) / 10)
    ari_score = 4.71 * (c_character / c_word) + (0.5 * (c_word / c_sentence)) - 21.43
    coleman_liau_score = (0.0588 * c_character / c_word * 100) - (0.296 * (c_sentence / c_word) * 100) - 15.8
    lix_score = (c_word / c_sentence) + (c_complex_word / c_word * 100)
    rix_score = ((c_complex_word / c_word) * 100) + (c_word / c_sentence)
    powers_sumner_kearl = (0.0778 * (c_word / c_sentence)) + (0.0455 * (c_syllable / c_word) * 100) + 2.7971
    spache_score = (0.121 * c_word / c_sentence) + (0.082 * (100 - (c_common / c_word) * 100)) + 0.659
    linsear_write = (((c_disyllable * 2) + (c_complex_word * 3) / c_word) * 100) / 10000

    # Linguistic Features to Dictionary

    result['Number of Sentence'] = c_sentence
    result['Number of Words'] = c_word
    result['Number of Paragraph'] = c_paragraph
    try:
        result['Words per Sentence (%)'] = c_word / c_sentence * 100
    except ZeroDivisionError:
        result['Words per Sentence (%)'] = 0
    result['Number of Characters'] = c_character
    try:
        result['Character per Words (%)'] = c_character / c_word * 100
    except ZeroDivisionError:
        result['Character per Words (%)'] = 0
    try:
        result['Sentence per Paragraph (%)'] = c_sentence / c_paragraph * 100
    except ZeroDivisionError:
        result['Sentence per Paragraph (%)'] = 0
    result['Number of Sylables'] = c_syllable
    try:
        result['Syllables per Word (%)'] = c_syllable / c_word * 100
    except ZeroDivisionError:
        result['Syllables per Word (%)'] = 0
    result['Number of Monosyllable'] = c_monosylable
    try:
        result['Monosyllable per Word (%)'] = c_monosylable / c_word * 100
    except ZeroDivisionError:
        result['Monosyllable per Word (%)'] = 0
    try:
        result['Disyllable per Word (%)'] = c_disyllable / c_word * 100
    except ZeroDivisionError:
        result['Disyllable per Word (%)'] = 0
    result['Number of Complex Words'] = c_complex_word
    try:
        result['Complex Words per Word (%)'] = c_complex_word / c_word * 100
    except ZeroDivisionError:
        result['Complex Words per Word (%)'] = 0
    result['Number of Advance Words'] = c_advance
    try:
        result['Advance Words per Words (%)'] = c_advance / c_word * 100
    except ZeroDivisionError:
        result['Advance Words per Words (%)'] = 0
    result['Number of Common Words'] = c_common
    try:
        result['Common Words per Words (%)'] = c_common / c_word * 100
    except ZeroDivisionError:
        result['Common Words per Words (%)'] = 0
    try:
        result['Verbs per Words (%)'] = c_verb / c_word * 100
    except ZeroDivisionError:
        result['Verbs per Words (%)'] = 0
    try:
        result['Verbs per Sentences (%)'] = c_verb / c_sentence * 100
    except ZeroDivisionError:
        result['Verbs per Sentence (%)'] = 0
    try:
        result['Ditransverbs per Sentences (%)'] = c_ditransverb / c_sentence * 100
    except ZeroDivisionError:
        result['Ditransverbs per Verbs (%)'] = 0
    try:
        result['Transverbs per Sentences (%)'] = c_transverb / c_sentence * 100
    except ZeroDivisionError:
        result['Transverbs per Sentences (%)'] = 0
    try:
        result['Intransitverbs per Sentences (%)'] = c_intransverb / c_sentence * 100
    except ZeroDivisionError:
        result['Intransitverbs per Sentences (%)'] = 0
    try:
        result['Auxverbs per Sentences (%)'] = c_auxverb / c_sentence * 100
    except ZeroDivisionError:
        result['Auxverbs per Sentences (%)'] = 0
    try:
        result['Conjuctions per Sentences (%)'] = c_conjunction / c_sentence * 100
    except ZeroDivisionError:
        result['Conjuctions per Sentences (%)'] = 0
    try:
        result['Nouns per Words (%)'] = c_noun / c_word * 100
    except ZeroDivisionError:
        result['Nouns per Words (%)'] = 0
    try:
        result['Nouns per Sentence (%)'] = c_noun / c_sentence * 100
    except ZeroDivisionError:
        result['Nouns per Sentence (%)'] = 0
    try:
        result['Puctuation per Sentence'] = c_punct / c_sentence * 100
    except ZeroDivisionError:
        result['Puctuation per Sentence'] = 0
    try:
        result['Adjective per Word (%)'] = c_adjective / c_word * 100
    except ZeroDivisionError:
        result['Adjective per Word (%)'] = 0
    try:
        result['Adjective per Sentence (%)'] = c_adjective / c_sentence * 100
    except ZeroDivisionError:
        result['Adjective per Sentence (%)'] = 0
    try:
        result['Adpositions per Sentences (%)'] = c_adposition / c_sentence * 100
    except ZeroDivisionError:
        result['Adpositions per Sentences (%)'] = 0
    try:
        result['Adverb per Sentence (%)'] = c_adverb / c_sentence * 100
    except ZeroDivisionError:
        result['Adverb per Sentence (%)'] = 0
    try:
        result['Pronoun per Sentence (%)'] = c_pronoun / c_sentence * 100
    except ZeroDivisionError:
        result['Pronoun per Sentence (%)'] = 0
    result['Number of Unknown Words'] = c_unknown
    try:
        result['Unknown Words per Words (%)'] = c_unknown / c_word * 100
    except ZeroDivisionError:
        result['Unknown Words per Words (%)'] = 0

    # Scores to dictionary
    result['Dale Chall Score'] = dale_chall_score
    result['Flesch Reading Ease Score'] = Flesch_Reading_Ease_Score
    result['New Flesch Reading Ease Score'] = new_flesch_reading_ease_score
    result['Gunning Fog Score'] = gunning_fog_score
    result['SMOG Score'] = smog_score
    result['FORCAST Score'] = forcast_score
    result['ARI Score'] = ari_score
    result['Coleman Liau Score'] = coleman_liau_score
    result['LIX Score'] = lix_score
    result['RIX Score'] = rix_score
    result['Powers Sumner Kearl'] = powers_sumner_kearl
    result['Spache Score'] = spache_score
    result['Linsear Write'] = linsear_write

    # Tenses to Dictionary
    try:
        result['Future Perfect Progressive (%)'] = c_future_perfect_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Future Perfect Progressive  (%)'] = 0
    try:
        result['Past Simple (%)'] = c_past_simple / c_sentence * 100
    except ZeroDivisionError:
        result['Past Simple (%)'] = 0
    try:
        result['Present Perfect Progressive (%)'] = c_present_perfect_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Present Perfect Progressive (%)'] = 0
    try:
        result['Future Progressive (%)'] = c_future_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Future Progressive (%)'] = 0
    try:
        result['Past Perfect Progressive (%)'] = c_past_perfect_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Past Perfect Progressive (%)'] = 0
    try:
        result['Past Progressive (%)'] = c_past_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Past Progressive (%)'] = 0
    try:
        result['Future Simple (%)'] = c_future_simple / c_sentence * 100
    except ZeroDivisionError:
        result['Future Simple (%)'] = 0
    try:
        result['Future Perfect (%)'] = c_future_perfect / c_sentence * 100
    except ZeroDivisionError:
        result['Future Perfect (%)'] = 0
    try:
        result['Present Simple (%)'] = c_present_simple / c_sentence * 100
    except ZeroDivisionError:
        result['Present Simple (%)'] = 0
    try:
        result['Past Perfect (%)'] = c_past_perfect / c_sentence * 100
    except ZeroDivisionError:
        result['Past Perfect (%)'] = 0
    try:
        result['Present Progressive (%)'] = c_present_progressive / c_sentence * 100
    except ZeroDivisionError:
        result['Present Progressive (%)'] = 0
    try:
        result['Present Perfect (%)'] = c_present_perfect / c_sentence * 100
    except ZeroDivisionError:
        result['Present Perfect (%)'] = 0

    return result


def feature_computer_df(dic):
    """
    Creates dataframe of the feature dictionary
    :param dic: Features of the article in dictionary format
    :return: pandas dataframe
    """
    dictionary = feature_computer(dic)
    return pd.DataFrame(dictionary, index=[0])


def add_article(name, text, level, csv_file=None, is_pdf=False, num_col=False, print_it=True):
    """
    Insert any sentence with proper tense tag to .csv file
    :param is_pdf: True if the text is pdf
    :param name: Name of the article
    :param print_it: If true prints features of the document
    :param num_col: If there is a column for row numbers in the csv files make it True
    :param text: Text file to added
    :param level: level of the sentence
    :param csv_file: .csv file to save to
    """
    if is_pdf is False:
        with codecs.open(text, 'r', encoding='utf-8',
                         errors='ignore') as myfile:
            data = str(myfile.read()).replace('.', ' . ')
            data = data.replace('-', '')
            doc = nlp(data)
    else:
        pdf_file_obj = open(text, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

        text = ''

        for page in range(pdf_reader.numPages):
            page_obj = pdf_reader.getPage(page)
            text += page_obj.extractText()
        doc = nlp(text)

    new_article_df = feature_computer_df(doc)
    new_article_df['Level'] = level
    new_article_df.insert(0, 'Name', name)
    data_df = pd.read_csv(csv_file)
    if num_col:
        data_df = df.drop(df.columns[0], axis=1)  # drop number column
    data_df = data_df.append(new_article_df)
    data_df.to_csv(csv_file, encoding='utf-8', index=False)
    if print_it:
        display('New data frame added')
        display(data_df.tail(1))
        # print(data_df.info())
    else:
        print(df.shape)


def get_article_df(name, text):

    data = text.replace('.', ' . ')
    data = data.replace('-', '')
    doc = nlp(data)
    new_article_df = feature_computer_df(doc)
    new_article_df.insert(0, 'Name', name)

    return new_article_df


def get_article_prediction(dataframe, model):
    df_p = dataframe
    try:
        df_p.drop(
            ['Number of Sentence', 'Number of Words', 'Number of Paragraph', 'Number of Characters', 'Number of Sylables',
             'Number of Monosyllable', 'Number of Complex Words', 'Number of Advance Words', 'Number of Common Words', \
             'Auxverbs per Sentences (%)', 'Verbs per Words (%)', 'Sentence per Paragraph (%)', 'Dale Chall Score', \
             'Flesch Reading Ease Score', 'New Flesch Reading Ease Score', 'Gunning Fog Score', 'SMOG Score', \
             'FORCAST Score', 'ARI Score', 'Coleman Liau Score', 'LIX Score', 'RIX Score', 'Powers Sumner Kearl', \
             'Spache Score', 'Puctuation per Sentence', 'Adjective per Word (%)', 'Adpositions per Sentences (%)', \
             'Conjuctions per Sentences (%)', 'Nouns per Words (%)', 'Number of Unknown Words', 'Disyllable per Word (%)', \
             'Transverbs per Sentences (%)', 'Intransitverbs per Sentences (%)', 'Verbs per Sentences (%)', \
             'Adjective per Sentence (%)', 'Pronoun per Sentence (%)', 'Unknown Words per Words (%)', \
             'Future Perfect (%)', 'Future Progressive (%)', 'Future Perfect (%)', 'Present Perfect (%)'], inplace=True,
            axis=1)
    except Exception:
        pass

    X = np.array(df_p.drop(['Name'], axis=1))
    print(df_p.columns)
    print(X.shape)
    prediction = model.predict(X)
    return prediction
