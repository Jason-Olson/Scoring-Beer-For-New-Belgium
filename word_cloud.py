from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import spacy

plt.style.use('ggplot')
plt.close('all')

def gen_word_could(text,out_file):
    # # Generate a word cloud image
    # wordcloud = WordCloud().generate(text)
    #
    # # Display the generated image:
    # # the matplotlib way:
    #
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud().generate(text)#max_font_size=40
    plt.figure(figsize=(8,4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(out_file,dpi=400,facecolor='#ffffe6', edgecolor='none')

def word_cloud_by_df(df,nlp,outfile):
    df = df.replace(np.nan, '', regex=True)
    X = df[['cClarity', 'cAroma', 'cFlavor', 'cMouthfeel', 'cFresh','cNotFresh']].values
    text = ''.join([''.join(str(row).lower()) for row in X])
    text = text.replace('[',"")
    text = text.replace(']',"")
    text = text.replace('\'',"")
    text = text.replace('\n',"")
    text = text.replace('-tim',"")
    lem_word_string = lemmatize_words(nlp,text)
    lem_word_string = lem_word_string.replace('kelly',"")
    lem_word_string = lem_word_string.replace('aaron',"")
    lem_word_string = lem_word_string.replace(' tim ',"")
    lem_word_string = lem_word_string.replace(' kd ',"")
    lem_word_string = lem_word_string.replace(' sl ',"")
    lem_word_string = lem_word_string.replace(' pat ',"")
    lem_word_string = lem_word_string.replace(' e ',"")
    lem_word_string = lem_word_string.replace('salazar',"")
    lem_word_string = lem_word_string.replace(' bg ',"")
    lem_word_string = lem_word_string.replace(' tv ',"")
    lem_word_string = lem_word_string.replace(' cody ',"")
    lem_word_string = lem_word_string.replace(' mc ',"")
    lem_word_string = lem_word_string.replace(' grady ',"")
    lem_word_string = lem_word_string.replace(' gr ',"")
    lem_word_string = lem_word_string.replace('_eh',"")
    lem_word_string = lem_word_string.replace('jeff',"")
    lem_word_string = lem_word_string.replace('maire',"")
    lem_word_string = lem_word_string.replace('marie',"")
    lem_word_string = lem_word_string.replace('-ds',"")
    lem_word_string = lem_word_string.replace('penelope',"")
    lem_word_string = lem_word_string.replace('tamar',"")
    lem_word_string = lem_word_string.replace('pd',"")
    lem_word_string = lem_word_string.replace('dm',"dms")

    gen_word_could(lem_word_string,outfile)
    gen_word_could(text,'graphs/word_cloud_text.png')
    return lem_word_string, text

def lemmatize_words(nlp,words):
    tok_list = []
    doc = nlp(str(words))
    for w in doc:
        if w.is_stop == False:
            tok_list.append(w.lemma_)
    lem_word_string = " ".join(tok_list)
    return lem_word_string

if __name__ == '__main__':
    df = pd.read_pickle('data/joined_results.pickle')
    # dfco = df[df['correct']==1]
    # dfttb = df[df['mcFresh']==1]
    df= df.sample(10)
    # df = pd.concat([df,dfttb])
    if not 'nlp' in locals():
        print("Loading English Module...")
        nlp = spacy.load('en')
        nlp.vocab["thin"].is_stop = False
    # gen_word_could(text,'word_cloud.png')
    outfile = 'graphs/word_cloud.png'
    lem_word_string, text = word_cloud_by_df(df,nlp,outfile)
