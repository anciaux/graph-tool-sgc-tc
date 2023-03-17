#!/usr/bin/env python

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st

additional_stopwords = """
e.g.
eg.
etc
tout
grand
petit
même
autre
seul
jeune
premier
bon
quel
beau
vieux
noir
nouveau
dernier
blanc
cher
long
pauvre
plein
toute
bas
gros
doux
heureux
haut
profond
rouge
humain
général
froid
sombre
sûr
ancien
propre
politique
possible
immense
public
pareil
bleu
fort
entier
simple
nécessaire
mauvais
social
important
certain
triste
joli
différent
ne
pas
plus
bien
si
là
encore
aussi
peu
alors
toujours
jamais
non
très
ainsi
moins
ici
oui
trop
déjà
tant
enfin
maintenant
beaucoup
assez
loin
point
presque
ailleurs
seulement
aujourd'hui
mieux
autour
souvent
dessus
longtemps
comme
comment
autant
d'abord
surtout
cependant
vite
tard
pourtant
ci
mal
parfois
vraiment
bientôt
partout
debout
plutôt
lentement
combien
hier
et
que
mais
ou
quand
puis
donc
car
ni
parce que
pourquoi
lorsque
tandis que
puisque
soit
or
le
un
son
ce
du
au
de
mon
leur
notre
votre
quelque
ton
chaque
aucun
tel
plusieurs
d'autres
nul
deux
cent
mille
trois
quatre
vingt
cinq
dix
neuf
six
huit
sept
trente
quarante
cinquante
quinze
douze
à
en
dans
pour
par
sur
avec
sans
sous
après
entre
vers
chez
jusque
contre
devant
depuis
pendant
avant
voilà
près
dès
malgré
voici
selon
derrière
parmi
afin de
auprès
quant à
hors
durant
grâce
il
je
se
qui
elle
vous
me
on
lui
nous
y
où
tu
moi
te
celui
rien
dont
ça
cela
toi
lequel
quoi
personne
l'un
chacun
auquel
quelqu'un
ceci
l'une
soi
sien
mien
la
les
des
une
quels
quelle
quelles
lesquels
laquelle
lesquelles
duquel
afin
aux
""".split()


comment_words = ''
stopwords = list(STOPWORDS)
stopwords += additional_stopwords
stopwords = set(stopwords)
stopwords = '\n'.join(stopwords)


def make_cloud_word(text):
    text = text.replace('\n', ' ')
    text = text.split()
    text = [e.lower().strip() for e in text]

    comment_words = " ".join(text)

    wordcloud = WordCloud(width=1500, height=int(1500*9/16),
                          background_color='white',
                          stopwords=stopwords.split(),
                          min_font_size=10).generate(comment_words)

    fig = plt.figure(figsize=(10, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)
