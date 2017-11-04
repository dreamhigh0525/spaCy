# coding: utf8
from __future__ import unicode_literals


TAG_MAP = {
    "ADJ___": {"morph": "_", "pos": "ADJ"},
    "ADJ__AdpType=Prep": {"morph": "AdpType=Prep", "pos": "ADJ"},
    "ADJ__AdpType=Preppron|Gender=Masc|Number=Sing": {"morph": "AdpType=Preppron|Gender=Masc|Number=Sing", "pos": "ADV"},
    "ADJ__AdvType=Tim": {"morph": "AdvType=Tim", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Plur": {"morph": "Gender=Fem|Number=Plur", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Plur|NumType=Ord": {"morph": "Gender=Fem|Number=Plur|NumType=Ord", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Plur|VerbForm=Part": {"morph": "Gender=Fem|Number=Plur|VerbForm=Part", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Sing": {"morph": "Gender=Fem|Number=Sing", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Sing|NumType=Ord": {"morph": "Gender=Fem|Number=Sing|NumType=Ord", "pos": "ADJ"},
    "ADJ__Gender=Fem|Number=Sing|VerbForm=Part": {"morph": "Gender=Fem|Number=Sing|VerbForm=Part", "pos": "ADJ"},
    "ADJ__Gender=Masc": {"morph": "Gender=Masc", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Plur": {"morph": "Gender=Masc|Number=Plur", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Plur|NumType=Ord": {"morph": "Gender=Masc|Number=Plur|NumType=Ord", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Plur|VerbForm=Part": {"morph": "Gender=Masc|Number=Plur|VerbForm=Part", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Sing": {"morph": "Gender=Masc|Number=Sing", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Sing|NumType=Ord": {"morph": "Gender=Masc|Number=Sing|NumType=Ord", "pos": "ADJ"},
    "ADJ__Gender=Masc|Number=Sing|VerbForm=Part": {"morph": "Gender=Masc|Number=Sing|VerbForm=Part", "pos": "ADJ"},
    "ADJ__Number=Plur": {"morph": "Number=Plur", "pos": "ADJ"},
    "ADJ__Number=Sing": {"morph": "Number=Sing", "pos": "ADJ"},
    "ADP__AdpType=Prep": {"morph": "AdpType=Prep", "pos": "ADP"},
    "ADP__AdpType=Preppron|Gender=Fem|Number=Sing": {"morph": "AdpType=Preppron|Gender=Fem|Number=Sing", "pos": "ADP"},
    "ADP__AdpType=Preppron|Gender=Masc|Number=Plur": {"morph": "AdpType=Preppron|Gender=Masc|Number=Plur", "pos": "ADP"},
    "ADP__AdpType=Preppron|Gender=Masc|Number=Sing": {"morph": "AdpType=Preppron|Gender=Masc|Number=Sing", "pos": "ADP"},
    "ADP": { "pos": "ADP"},
    "ADV___": {"morph": "_", "pos": "ADV"},
    "ADV__AdpType=Prep": {"morph": "AdpType=Prep", "pos": "ADV"},
    "ADV__AdpType=Preppron|Gender=Masc|Number=Sing": {"morph": "AdpType=Preppron|Gender=Masc|Number=Sing", "pos": "ADV"},
    "ADV__AdvType=Tim": {"morph": "AdvType=Tim", "pos": "ADV"},
    "ADV__Gender=Masc|Number=Sing": {"morph": "Gender=Masc|Number=Sing", "pos": "ADV"},
    "ADV__Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin", "pos": "ADV"},
    "ADV__Negative=Neg": {"morph": "Negative=Neg", "pos": "ADV"},
    "ADV__Number=Plur": {"morph": "Number=Plur", "pos": "ADV"},
    "ADV__Polarity=Neg": {"morph": "Polarity=Neg", "pos": "ADV"},
    "AUX__Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part": {"morph": "Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part", "pos": "AUX"},
    "AUX__Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part": {"morph": "Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part", "pos": "AUX"},
    "AUX__Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part": {"morph": "Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part", "pos": "AUX"},
    "AUX__Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part": {"morph": "Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part", "pos": "AUX"},
    "AUX__Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Cnd|Number=Sing|Person=3|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=3|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Imp|Number=Plur|Person=3|VerbForm=Fin": {"morph": "Mood=Imp|Number=Plur|Person=3|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Imp|Number=Sing|Person=2|VerbForm=Fin": {"morph": "Mood=Imp|Number=Sing|Person=2|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Imp|Number=Sing|Person=3|VerbForm=Fin": {"morph": "Mood=Imp|Number=Sing|Person=3|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=2|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin", "pos": "AUX"},
    "AUX__Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", "pos": "AUX"},
    "AUX__VerbForm=Ger": {"morph": "VerbForm=Ger", "pos": "AUX"},
    "AUX__VerbForm=Inf": {"morph": "VerbForm=Inf", "pos": "AUX"},
    "CCONJ___": {"morph": "_", "pos": "CONJ"},
    "CONJ___": {"morph": "_", "pos": "CONJ"},
    "DET__Definite=Def|Gender=Fem|Number=Plur|PronType=Art": {"morph": "Definite=Def|Gender=Fem|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Definite=Def|Gender=Fem|Number=Sing|PronType=Art": {"morph": "Definite=Def|Gender=Fem|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Definite=Def|Gender=Masc|Number=Plur|PronType=Art": {"morph": "Definite=Def|Gender=Masc|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art": {"morph": "Definite=Def|Gender=Masc|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Definite=Def|Gender=Masc|PronType=Art": {"morph": "Definite=Def|Gender=Masc|PronType=Art", "pos": "DET"},
    "DET__Definite=Def|Number=Sing|PronType=Art": {"morph": "Definite=Def|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Fem|Number=Plur|PronType=Art": {"morph": "Definite=Ind|Gender=Fem|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Fem|Number=Sing|NumType=Card|PronType=Art": {"morph": "Definite=Ind|Gender=Fem|Number=Sing|NumType=Card|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Fem|Number=Sing|PronType=Art": {"morph": "Definite=Ind|Gender=Fem|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Masc|Number=Plur|PronType=Art": {"morph": "Definite=Ind|Gender=Masc|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Masc|Number=Sing|NumType=Card|PronType=Art": {"morph": "Definite=Ind|Gender=Masc|Number=Sing|NumType=Card|PronType=Art", "pos": "DET"},
    "DET__Definite=Ind|Gender=Masc|Number=Sing|PronType=Art": {"morph": "Definite=Ind|Gender=Masc|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|Number[psor]=Plur|Person=2|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Number[psor]=Plur|Person=2|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|PronType=Art": {"morph": "Gender=Fem|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|PronType=Dem": {"morph": "Gender=Fem|Number=Plur|PronType=Dem", "pos": "DET"},
    "DET__Gender=Fem|Number=Plur|PronType=Ind": {"morph": "Gender=Fem|Number=Plur|PronType=Ind", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|Number[psor]=Plur|Person=2|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Plur|Person=2|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|PronType=Art": {"morph": "Gender=Fem|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|PronType=Dem": {"morph": "Gender=Fem|Number=Sing|PronType=Dem", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|PronType=Ind": {"morph": "Gender=Fem|Number=Sing|PronType=Ind", "pos": "DET"},
    "DET__Gender=Fem|Number=Sing|PronType=Int": {"morph": "Gender=Fem|Number=Sing|PronType=Int", "pos": "DET"},
    "DET__Gender=Masc|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Masc|Number=Plur|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Plur|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Masc|Number=Plur|PronType=Art": {"morph": "Gender=Masc|Number=Plur|PronType=Art", "pos": "DET"},
    "DET__Gender=Masc|Number=Plur|PronType=Dem": {"morph": "Gender=Masc|Number=Plur|PronType=Dem", "pos": "DET"},
    "DET__Gender=Masc|Number=Plur|PronType=Ind": {"morph": "Gender=Masc|Number=Plur|PronType=Ind", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|PronType=Art": {"morph": "Gender=Masc|Number=Sing|PronType=Art", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|PronType=Dem": {"morph": "Gender=Masc|Number=Sing|PronType=Dem", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|PronType=Ind": {"morph": "Gender=Masc|Number=Sing|PronType=Ind", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|PronType=Int": {"morph": "Gender=Masc|Number=Sing|PronType=Int", "pos": "DET"},
    "DET__Gender=Masc|Number=Sing|PronType=Tot": {"morph": "Gender=Masc|Number=Sing|PronType=Tot", "pos": "DET"},
    "DET__Number=Plur|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Number=Plur|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Plur|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs": {"morph": "Number=Plur|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Plur|Person=3|Poss=Yes|PronType=Prs": {"morph": "Number=Plur|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Plur|PronType=Dem": {"morph": "Number=Plur|PronType=Dem", "pos": "DET"},
    "DET__Number=Plur|PronType=Ind": {"morph": "Number=Plur|PronType=Ind", "pos": "DET"},
    "DET__Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs": {"morph": "Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "DET"},
    "DET__Number=Sing|PronType=Dem": {"morph": "Number=Sing|PronType=Dem", "pos": "DET"},
    "DET__Number=Sing|PronType=Ind": {"morph": "Number=Sing|PronType=Ind", "pos": "DET"},
    "DET__PronType=Int": {"morph": "PronType=Int", "pos": "DET"},
    "DET__PronType=Rel": {"morph": "PronType=Rel", "pos": "DET"},
    "DET": { "pos": "DET"},
    "INTJ___": {"morph": "_", "pos": "INTJ"},
    "NOUN___": {"morph": "_", "pos": "NOUN"},
    "NOUN__AdvType=Tim": {"morph": "AdvType=Tim", "pos": "NOUN"},
    "NOUN__AdvType=Tim|Gender=Masc|Number=Sing": {"morph": "AdvType=Tim|Gender=Masc|Number=Sing", "pos": "NOUN"},
    "NOUN__Gender=Fem": {"morph": "Gender=Fem", "pos": "NOUN"},
    "NOUN__Gender=Fem|Number=Plur": {"morph": "Gender=Fem|Number=Plur", "pos": "NOUN"},
    "NOUN__Gender=Fem|Number=Sing": {"morph": "Gender=Fem|Number=Sing", "pos": "NOUN"},
    "NOUN__Gender=Masc": {"morph": "Gender=Masc", "pos": "NOUN"},
    "NOUN__Gender=Masc|Number=Plur": {"morph": "Gender=Masc|Number=Plur", "pos": "NOUN"},
    "NOUN__Gender=Masc|Number=Sing": {"morph": "Gender=Masc|Number=Sing", "pos": "NOUN"},
    "NOUN__Gender=Masc|Number=Sing|VerbForm=Part": {"morph": "Gender=Masc|Number=Sing|VerbForm=Part", "pos": "NOUN"},
    "NOUN__Number=Plur": {"morph": "Number=Plur", "pos": "NOUN"},
    "NOUN__Number=Sing": {"morph": "Number=Sing", "pos": "NOUN"},
    "NOUN__NumForm=Digit": {"morph": "NumForm=Digit", "pos": "NOUN"},
    "NUM__Gender=Fem|Number=Plur|NumType=Card": {"morph": "Gender=Fem|Number=Plur|NumType=Card", "pos": "NUM"},
    "NUM__Gender=Fem|Number=Sing|NumType=Card": {"morph": "Gender=Fem|Number=Sing|NumType=Card", "pos": "NUM"},
    "NUM__Gender=Masc|Number=Plur|NumType=Card": {"morph": "Gender=Masc|Number=Plur|NumType=Card", "pos": "NUM"},
    "NUM__Gender=Masc|Number=Sing|NumType=Card": {"morph": "Gender=Masc|Number=Sing|NumType=Card", "pos": "NUM"},
    "NUM__Number=Plur|NumType=Card": {"morph": "Number=Plur|NumType=Card", "pos": "NUM"},
    "NUM__Number=Sing|NumType=Card": {"morph": "Number=Sing|NumType=Card", "pos": "NUM"},
    "NUM__NumForm=Digit": {"morph": "NumForm=Digit", "pos": "NUM"},
    "NUM__NumForm=Digit|NumType=Card": {"morph": "NumForm=Digit|NumType=Card", "pos": "NUM"},
    "NUM__NumForm=Digit|NumType=Frac": {"morph": "NumForm=Digit|NumType=Frac", "pos": "NUM"},
    "NUM__NumType=Card": {"morph": "NumType=Card", "pos": "NUM"},
    "PART___": {"morph": "_", "pos": "PART"},
    "PART__Negative=Neg": {"morph": "Negative=Neg", "pos": "PART"},
    "PRON___": {"morph": "_", "pos": "PRON"},
    "PRON__Case=Acc|Gender=Fem|Number=Plur|Person=3|PronType=Prs": {"morph": "Case=Acc|Gender=Fem|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Gender=Fem|Number=Sing|Person=3|PronType=Prs": {"morph": "Case=Acc|Gender=Fem|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Gender=Masc|Number=Plur|Person=3|PronType=Prs": {"morph": "Case=Acc|Gender=Masc|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Gender=Masc|Number=Sing|Person=3|PronType=Prs": {"morph": "Case=Acc|Gender=Masc|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Number=Plur|Person=3|PronType=Prs": {"morph": "Case=Acc|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Number=Sing|Person=3|PronType=Prs": {"morph": "Case=Acc|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Acc|Person=3|PronType=Prs": {"morph": "Case=Acc|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Dat|Number=Plur|Person=3|PronType=Prs": {"morph": "Case=Dat|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Dat|Number=Sing|Person=3|PronType=Prs": {"morph": "Case=Dat|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Nom|Number=Sing|Person=1|PronType=Prs": {"morph": "Case=Nom|Number=Sing|Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Case=Nom|Number=Sing|Person=2|PronType=Prs": {"morph": "Case=Nom|Number=Sing|Person=2|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Person=3|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|Person=3|PronType=Prs": {"morph": "Gender=Fem|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|PronType=Dem": {"morph": "Gender=Fem|Number=Plur|PronType=Dem", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|PronType=Ind": {"morph": "Gender=Fem|Number=Plur|PronType=Ind", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|PronType=Int": {"morph": "Gender=Fem|Number=Plur|PronType=Int", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Plur|PronType=Rel": {"morph": "Gender=Fem|Number=Plur|PronType=Rel", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Person=1|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|Person=3|PronType=Prs": {"morph": "Gender=Fem|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|PronType=Dem": {"morph": "Gender=Fem|Number=Sing|PronType=Dem", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|PronType=Ind": {"morph": "Gender=Fem|Number=Sing|PronType=Ind", "pos": "PRON"},
    "PRON__Gender=Fem|Number=Sing|PronType=Rel": {"morph": "Gender=Fem|Number=Sing|PronType=Rel", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|Person=1|PronType=Prs": {"morph": "Gender=Masc|Number=Plur|Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|Person=2|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Plur|Person=2|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|Person=3|PronType=Prs": {"morph": "Gender=Masc|Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|PronType=Dem": {"morph": "Gender=Masc|Number=Plur|PronType=Dem", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|PronType=Ind": {"morph": "Gender=Masc|Number=Plur|PronType=Ind", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|PronType=Int": {"morph": "Gender=Masc|Number=Plur|PronType=Int", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Plur|PronType=Rel": {"morph": "Gender=Masc|Number=Plur|PronType=Rel", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Number[psor]=Plur|Person=1|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Number[psor]=Sing|Person=1|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Number[psor]=Sing|Person=2|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|Person=3|PronType=Prs": {"morph": "Gender=Masc|Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|PronType=Dem": {"morph": "Gender=Masc|Number=Sing|PronType=Dem", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|PronType=Ind": {"morph": "Gender=Masc|Number=Sing|PronType=Ind", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|PronType=Int": {"morph": "Gender=Masc|Number=Sing|PronType=Int", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|PronType=Rel": {"morph": "Gender=Masc|Number=Sing|PronType=Rel", "pos": "PRON"},
    "PRON__Gender=Masc|Number=Sing|PronType=Tot": {"morph": "Gender=Masc|Number=Sing|PronType=Tot", "pos": "PRON"},
    "PRON__Number=Plur|Person=1": {"morph": "Number=Plur|Person=1", "pos": "PRON"},
    "PRON__Number=Plur|Person=1|PronType=Prs": {"morph": "Number=Plur|Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Plur|Person=2|Polite=Form|PronType=Prs": {"morph": "Number=Plur|Person=2|Polite=Form|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Plur|Person=2|PronType=Prs": {"morph": "Number=Plur|Person=2|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Plur|Person=3|Poss=Yes|PronType=Prs": {"morph": "Number=Plur|Person=3|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Plur|Person=3|PronType=Prs": {"morph": "Number=Plur|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Plur|PronType=Dem": {"morph": "Number=Plur|PronType=Dem", "pos": "PRON"},
    "PRON__Number=Plur|PronType=Ind": {"morph": "Number=Plur|PronType=Ind", "pos": "PRON"},
    "PRON__Number=Plur|PronType=Int": {"morph": "Number=Plur|PronType=Int", "pos": "PRON"},
    "PRON__Number=Plur|PronType=Rel": {"morph": "Number=Plur|PronType=Rel", "pos": "PRON"},
    "PRON__Number=Sing|Person=1": {"morph": "Number=Sing|Person=1", "pos": "PRON"},
    "PRON__Number=Sing|Person=1|PrepCase=Pre|PronType=Prs": {"morph": "Number=Sing|Person=1|PrepCase=Pre|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=1|PronType=Prs": {"morph": "Number=Sing|Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=2": {"morph": "Number=Sing|Person=2", "pos": "PRON"},
    "PRON__Number=Sing|Person=2|Polite=Form|PronType=Prs": {"morph": "Number=Sing|Person=2|Polite=Form|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=2|PrepCase=Pre|PronType=Prs": {"morph": "Number=Sing|Person=2|PrepCase=Pre|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=2|PronType=Prs": {"morph": "Number=Sing|Person=2|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=3|Poss=Yes|PronType=Prs": {"morph": "Number=Sing|Person=3|Poss=Yes|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|Person=3|PronType=Prs": {"morph": "Number=Sing|Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__Number=Sing|PronType=Dem": {"morph": "Number=Sing|PronType=Dem", "pos": "PRON"},
    "PRON__Number=Sing|PronType=Ind": {"morph": "Number=Sing|PronType=Ind", "pos": "PRON"},
    "PRON__Number=Sing|PronType=Int": {"morph": "Number=Sing|PronType=Int", "pos": "PRON"},
    "PRON__Number=Sing|PronType=Rel": {"morph": "Number=Sing|PronType=Rel", "pos": "PRON"},
    "PRON__Person=1|PronType=Prs": {"morph": "Person=1|PronType=Prs", "pos": "PRON"},
    "PRON__Person=3": {"morph": "Person=3", "pos": "PRON"},
    "PRON__Person=3|PrepCase=Pre|PronType=Prs": {"morph": "Person=3|PrepCase=Pre|PronType=Prs", "pos": "PRON"},
    "PRON__Person=3|PronType=Prs": {"morph": "Person=3|PronType=Prs", "pos": "PRON"},
    "PRON__PronType=Ind": {"morph": "PronType=Ind", "pos": "PRON"},
    "PRON__PronType=Int": {"morph": "PronType=Int", "pos": "PRON"},
    "PRON__PronType=Rel": {"morph": "PronType=Rel", "pos": "PRON"},
    "PROPN___": {"morph": "_", "pos": "PROPN"},
    "PUNCT___": {"morph": "_", "pos": "PUNCT"},
    "PUNCT__PunctSide=Fin|PunctType=Brck": {"morph": "PunctSide=Fin|PunctType=Brck", "pos": "PUNCT"},
    "PUNCT__PunctSide=Fin|PunctType=Excl": {"morph": "PunctSide=Fin|PunctType=Excl", "pos": "PUNCT"},
    "PUNCT__PunctSide=Fin|PunctType=Qest": {"morph": "PunctSide=Fin|PunctType=Qest", "pos": "PUNCT"},
    "PUNCT__PunctSide=Ini|PunctType=Brck": {"morph": "PunctSide=Ini|PunctType=Brck", "pos": "PUNCT"},
    "PUNCT__PunctSide=Ini|PunctType=Excl": {"morph": "PunctSide=Ini|PunctType=Excl", "pos": "PUNCT"},
    "PUNCT__PunctSide=Ini|PunctType=Qest": {"morph": "PunctSide=Ini|PunctType=Qest", "pos": "PUNCT"},
    "PUNCT__PunctType=Colo": {"morph": "PunctType=Colo", "pos": "PUNCT"},
    "PUNCT__PunctType=Comm": {"morph": "PunctType=Comm", "pos": "PUNCT"},
    "PUNCT__PunctType=Dash": {"morph": "PunctType=Dash", "pos": "PUNCT"},
    "PUNCT__PunctType=Peri": {"morph": "PunctType=Peri", "pos": "PUNCT"},
    "PUNCT__PunctType=Quot": {"morph": "PunctType=Quot", "pos": "PUNCT"},
    "PUNCT__PunctType=Semi": {"morph": "PunctType=Semi", "pos": "PUNCT"},
    "SCONJ___": {"morph": "_", "pos": "SCONJ"},
    "SYM___": {"morph": "_", "pos": "SYM"},
    "SYM__NumForm=Digit": {"morph": "NumForm=Digit", "pos": "SYM"},
    "SYM__NumForm=Digit|NumType=Frac": {"morph": "NumForm=Digit|NumType=Frac", "pos": "SYM"},
    "VERB__Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part": {"morph": "Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part", "pos": "VERB"},
    "VERB__Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part": {"morph": "Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part", "pos": "VERB"},
    "VERB__Gender=Masc|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Gender=Masc|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part": {"morph": "Gender=Masc|Number=Plur|Tense=Past|VerbForm=Part", "pos": "VERB"},
    "VERB__Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part": {"morph": "Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part", "pos": "VERB"},
    "VERB__Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Cnd|Number=Sing|Person=3|VerbForm=Fin": {"morph": "Mood=Cnd|Number=Sing|Person=3|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Imp|Number=Plur|Person=1|VerbForm=Fin": {"morph": "Mood=Imp|Number=Plur|Person=1|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Imp|Number=Plur|Person=2|VerbForm=Fin": {"morph": "Mood=Imp|Number=Plur|Person=2|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Imp|Number=Plur|Person=3|VerbForm=Fin": {"morph": "Mood=Imp|Number=Plur|Person=3|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Imp|Number=Sing|Person=2|VerbForm=Fin": {"morph": "Mood=Imp|Number=Sing|Person=2|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Imp|Number=Sing|Person=3|VerbForm=Fin": {"morph": "Mood=Imp|Number=Sing|Person=3|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Past|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Ind|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Ind|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin", "pos": "VERB"},
    "VERB__Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin": {"morph": "Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", "pos": "VERB"},
    "VERB__VerbForm=Ger": {"morph": "VerbForm=Ger", "pos": "VERB"},
    "VERB__VerbForm=Inf": {"morph": "VerbForm=Inf", "pos": "VERB"},
    "X___": {"morph": "_", "pos": "X"},
    "_SP": {"morph": "_", "pos": "SPACE"},
}
