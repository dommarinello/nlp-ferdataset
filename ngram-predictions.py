import os
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.util import ngrams
from natsort import natsorted
import streamlit as st

nltk.download('punkt')

trigrams = []
total_ngrams = 0
total_voc = 0
list_of_files = natsorted(os.listdir("data"))

for file_name in list_of_files:
    with open("data/"+file_name, "r") as data:
        data = data.read().split("\n")
        for line in data:
            data_in_line = line.split(" ")
            freq = int(data_in_line.pop())
            trigram = [tuple(data_in_line), freq]
            total_ngrams += freq
            trigrams.append(trigram)
            total_voc += 1


for trigram in trigrams:
    trigram[-1] = (trigram[-1]+1)/(total_ngrams+total_voc)



def tokenize_input(input_string):
    token = word_tokenize(input_string)
    ngram = list(ngrams(token, 2))[-1]
    return ngram


def make_prediction(ngrams, ngram_input, limit=4):
    pred = []
    count = 0
    for each in ngrams:
        if each[0][:-1] == ngram_input:
            count +=1
            pred.append(each[0][-1])
            if count == limit:
                break

    if count < limit:
        while (count != limit):
            pred.append("NOT FOUND")
            count +=1

    return pred

st.write("""
# Predviđanje riječi primjenom metoda strojnog učenja na temelju n-gramskih nizova 

*Postupak predviđanja sljedeće riječi na temelju zadanog niza riječi koristi se u području obrade prirodnog jezika, ponajviše kod strojnog prepoznavanja govora. Za predviđanje sljedeće riječi je ključan jezični model koji se može konstruirati iz tekstualnih korpusa ili obrađenih skupova podataka poput n-gramskih nizova. Vaš zadatak je implementirati sustav za predviđanje sljedeće riječi u zadanom nizu. Jezični model je potrebno konstruirati na temelju n-gramskih kolekcija različitih duljina i usporediti rezultate. *

""")

str1 = st.text_input("Unesite niz:", 'u skladu s')
if st.button('Generiraj slijdecu rijec'):
    ngram_1 = tokenize_input(str1)

    pred1 = make_prediction(trigrams, ngram_1)
    print("ngram model predictions: {}".format(pred1))

    st.write("Predikcija slijedece rijeci na temelju zadanog niza:\n")
    st.header("Niz - {}".format(str1))
    st.subheader("Predikcija: {}".format(pred1))
