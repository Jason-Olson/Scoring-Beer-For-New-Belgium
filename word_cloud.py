from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle



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
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(out_file)

if __name__ == '__main__':
    df = pd.read_pickle('data/joined_results.pickle')
    dfco = df[df['correct']==1]
    dfttb = df[df['mcFresh']==1]
    dfttb= dfttb.sample(10)
    df = pd.concat([df,dfttb])
    df = df.replace(np.nan, '', regex=True)
    X = df[['cClarity', 'cAroma', 'cFlavor', 'cMouthfeel', 'cFresh','cNotFresh']].values
    text = ''.join([''.join(str(row)) for row in X])
    text = text.replace('[',"")
    text = text.replace(']',"")
    text = text.replace('\'',"")
    gen_word_could(text,'word_cloud.png')
