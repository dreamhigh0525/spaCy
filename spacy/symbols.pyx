# cython: optimize.unpack_method_calls=False
IDS = {
    "": NIL,
    "IS_ALPHA": IS_ALPHA,
    "IS_ASCII": IS_ASCII,
    "IS_DIGIT": IS_DIGIT,
    "IS_LOWER": IS_LOWER,
    "IS_PUNCT": IS_PUNCT,
    "IS_SPACE": IS_SPACE,
    "IS_TITLE": IS_TITLE,
    "IS_UPPER": IS_UPPER,
    "LIKE_URL": LIKE_URL,
    "LIKE_NUM": LIKE_NUM,
    "LIKE_EMAIL": LIKE_EMAIL,
    "IS_STOP": IS_STOP,
    "IS_OOV_DEPRECATED": IS_OOV_DEPRECATED,
    "IS_BRACKET": IS_BRACKET,
    "IS_QUOTE": IS_QUOTE,
    "IS_LEFT_PUNCT": IS_LEFT_PUNCT,
    "IS_RIGHT_PUNCT": IS_RIGHT_PUNCT,
    "IS_CURRENCY": IS_CURRENCY,

    "FLAG19": FLAG19,
    "FLAG20": FLAG20,
    "FLAG21": FLAG21,
    "FLAG22": FLAG22,
    "FLAG23": FLAG23,
    "FLAG24": FLAG24,
    "FLAG25": FLAG25,
    "FLAG26": FLAG26,
    "FLAG27": FLAG27,
    "FLAG28": FLAG28,
    "FLAG29": FLAG29,
    "FLAG30": FLAG30,
    "FLAG31": FLAG31,
    "FLAG32": FLAG32,
    "FLAG33": FLAG33,
    "FLAG34": FLAG34,
    "FLAG35": FLAG35,
    "FLAG36": FLAG36,
    "FLAG37": FLAG37,
    "FLAG38": FLAG38,
    "FLAG39": FLAG39,
    "FLAG40": FLAG40,
    "FLAG41": FLAG41,
    "FLAG42": FLAG42,
    "FLAG43": FLAG43,
    "FLAG44": FLAG44,
    "FLAG45": FLAG45,
    "FLAG46": FLAG46,
    "FLAG47": FLAG47,
    "FLAG48": FLAG48,
    "FLAG49": FLAG49,
    "FLAG50": FLAG50,
    "FLAG51": FLAG51,
    "FLAG52": FLAG52,
    "FLAG53": FLAG53,
    "FLAG54": FLAG54,
    "FLAG55": FLAG55,
    "FLAG56": FLAG56,
    "FLAG57": FLAG57,
    "FLAG58": FLAG58,
    "FLAG59": FLAG59,
    "FLAG60": FLAG60,
    "FLAG61": FLAG61,
    "FLAG62": FLAG62,
    "FLAG63": FLAG63,

    "ID": ID,
    "ORTH": ORTH,
    "LOWER": LOWER,
    "NORM": NORM,
    "SHAPE": SHAPE,
    "PREFIX": PREFIX,
    "SUFFIX": SUFFIX,

    "LENGTH": LENGTH,
    "CLUSTER": CLUSTER,
    "LEMMA": LEMMA,
    "POS": POS,
    "TAG": TAG,
    "DEP": DEP,
    "ENT_IOB": ENT_IOB,
    "ENT_TYPE": ENT_TYPE,
    "ENT_ID": ENT_ID,
    "ENT_KB_ID": ENT_KB_ID,
    "HEAD": HEAD,
    "SENT_START": SENT_START,
    "SPACY": SPACY,
    "PROB": PROB,
    "LANG": LANG,
    "IDX": IDX,

    "ADJ": ADJ,
    "ADP": ADP,
    "ADV": ADV,
    "AUX": AUX,
    "CONJ": CONJ,
    "CCONJ": CCONJ, # U20
    "DET": DET,
    "INTJ": INTJ,
    "NOUN": NOUN,
    "NUM": NUM,
    "PART": PART,
    "PRON": PRON,
    "PROPN": PROPN,
    "PUNCT": PUNCT,
    "SCONJ": SCONJ,
    "SYM": SYM,
    "VERB": VERB,
    "X": X,
    "EOL": EOL,
    "SPACE": SPACE,

    "DEPRECATED001": DEPRECATED001,
    "DEPRECATED002": DEPRECATED002,
    "DEPRECATED003": DEPRECATED003,
    "DEPRECATED004": DEPRECATED004,
    "DEPRECATED005": DEPRECATED005,
    "DEPRECATED006": DEPRECATED006,
    "DEPRECATED007": DEPRECATED007,
    "DEPRECATED008": DEPRECATED008,
    "DEPRECATED009": DEPRECATED009,
    "DEPRECATED010": DEPRECATED010,
    "DEPRECATED011": DEPRECATED011,
    "DEPRECATED012": DEPRECATED012,
    "DEPRECATED013": DEPRECATED013,
    "DEPRECATED014": DEPRECATED014,
    "DEPRECATED015": DEPRECATED015,
    "DEPRECATED016": DEPRECATED016,
    "DEPRECATED017": DEPRECATED017,
    "DEPRECATED018": DEPRECATED018,
    "DEPRECATED019": DEPRECATED019,
    "DEPRECATED020": DEPRECATED020,
    "DEPRECATED021": DEPRECATED021,
    "DEPRECATED022": DEPRECATED022,
    "DEPRECATED023": DEPRECATED023,
    "DEPRECATED024": DEPRECATED024,
    "DEPRECATED025": DEPRECATED025,
    "DEPRECATED026": DEPRECATED026,
    "DEPRECATED027": DEPRECATED027,
    "DEPRECATED028": DEPRECATED028,
    "DEPRECATED029": DEPRECATED029,
    "DEPRECATED030": DEPRECATED030,
    "DEPRECATED031": DEPRECATED031,
    "DEPRECATED032": DEPRECATED032,
    "DEPRECATED033": DEPRECATED033,
    "DEPRECATED034": DEPRECATED034,
    "DEPRECATED035": DEPRECATED035,
    "DEPRECATED036": DEPRECATED036,
    "DEPRECATED037": DEPRECATED037,
    "DEPRECATED038": DEPRECATED038,
    "DEPRECATED039": DEPRECATED039,
    "DEPRECATED040": DEPRECATED040,
    "DEPRECATED041": DEPRECATED041,
    "DEPRECATED042": DEPRECATED042,
    "DEPRECATED043": DEPRECATED043,
    "DEPRECATED044": DEPRECATED044,
    "DEPRECATED045": DEPRECATED045,
    "DEPRECATED046": DEPRECATED046,
    "DEPRECATED047": DEPRECATED047,
    "DEPRECATED048": DEPRECATED048,
    "DEPRECATED049": DEPRECATED049,
    "DEPRECATED050": DEPRECATED050,
    "DEPRECATED051": DEPRECATED051,
    "DEPRECATED052": DEPRECATED052,
    "DEPRECATED053": DEPRECATED053,
    "DEPRECATED054": DEPRECATED054,
    "DEPRECATED055": DEPRECATED055,
    "DEPRECATED056": DEPRECATED056,
    "DEPRECATED057": DEPRECATED057,
    "DEPRECATED058": DEPRECATED058,
    "DEPRECATED059": DEPRECATED059,
    "DEPRECATED060": DEPRECATED060,
    "DEPRECATED061": DEPRECATED061,
    "DEPRECATED062": DEPRECATED062,
    "DEPRECATED063": DEPRECATED063,
    "DEPRECATED064": DEPRECATED064,
    "DEPRECATED065": DEPRECATED065,
    "DEPRECATED066": DEPRECATED066,
    "DEPRECATED067": DEPRECATED067,
    "DEPRECATED068": DEPRECATED068,
    "DEPRECATED069": DEPRECATED069,
    "DEPRECATED070": DEPRECATED070,
    "DEPRECATED071": DEPRECATED071,
    "DEPRECATED072": DEPRECATED072,
    "DEPRECATED073": DEPRECATED073,
    "DEPRECATED074": DEPRECATED074,
    "DEPRECATED075": DEPRECATED075,
    "DEPRECATED076": DEPRECATED076,
    "DEPRECATED077": DEPRECATED077,
    "DEPRECATED078": DEPRECATED078,
    "DEPRECATED079": DEPRECATED079,
    "DEPRECATED080": DEPRECATED080,
    "DEPRECATED081": DEPRECATED081,
    "DEPRECATED082": DEPRECATED082,
    "DEPRECATED083": DEPRECATED083,
    "DEPRECATED084": DEPRECATED084,
    "DEPRECATED085": DEPRECATED085,
    "DEPRECATED086": DEPRECATED086,
    "DEPRECATED087": DEPRECATED087,
    "DEPRECATED088": DEPRECATED088,
    "DEPRECATED089": DEPRECATED089,
    "DEPRECATED090": DEPRECATED090,
    "DEPRECATED091": DEPRECATED091,
    "DEPRECATED092": DEPRECATED092,
    "DEPRECATED093": DEPRECATED093,
    "DEPRECATED094": DEPRECATED094,
    "DEPRECATED095": DEPRECATED095,
    "DEPRECATED096": DEPRECATED096,
    "DEPRECATED097": DEPRECATED097,
    "DEPRECATED098": DEPRECATED098,
    "DEPRECATED099": DEPRECATED099,
    "DEPRECATED100": DEPRECATED100,
    "DEPRECATED101": DEPRECATED101,
    "DEPRECATED102": DEPRECATED102,
    "DEPRECATED103": DEPRECATED103,
    "DEPRECATED104": DEPRECATED104,
    "DEPRECATED105": DEPRECATED105,
    "DEPRECATED106": DEPRECATED106,
    "DEPRECATED107": DEPRECATED107,
    "DEPRECATED108": DEPRECATED108,
    "DEPRECATED109": DEPRECATED109,
    "DEPRECATED110": DEPRECATED110,
    "DEPRECATED111": DEPRECATED111,
    "DEPRECATED112": DEPRECATED112,
    "DEPRECATED113": DEPRECATED113,
    "DEPRECATED114": DEPRECATED114,
    "DEPRECATED115": DEPRECATED115,
    "DEPRECATED116": DEPRECATED116,
    "DEPRECATED117": DEPRECATED117,
    "DEPRECATED118": DEPRECATED118,
    "DEPRECATED119": DEPRECATED119,
    "DEPRECATED120": DEPRECATED120,
    "DEPRECATED121": DEPRECATED121,
    "DEPRECATED122": DEPRECATED122,
    "DEPRECATED123": DEPRECATED123,
    "DEPRECATED124": DEPRECATED124,
    "DEPRECATED125": DEPRECATED125,
    "DEPRECATED126": DEPRECATED126,
    "DEPRECATED127": DEPRECATED127,
    "DEPRECATED128": DEPRECATED128,
    "DEPRECATED129": DEPRECATED129,
    "DEPRECATED130": DEPRECATED130,
    "DEPRECATED131": DEPRECATED131,
    "DEPRECATED132": DEPRECATED132,
    "DEPRECATED133": DEPRECATED133,
    "DEPRECATED134": DEPRECATED134,
    "DEPRECATED135": DEPRECATED135,
    "DEPRECATED136": DEPRECATED136,
    "DEPRECATED137": DEPRECATED137,
    "DEPRECATED138": DEPRECATED138,
    "DEPRECATED139": DEPRECATED139,
    "DEPRECATED140": DEPRECATED140,
    "DEPRECATED141": DEPRECATED141,
    "DEPRECATED142": DEPRECATED142,
    "DEPRECATED143": DEPRECATED143,
    "DEPRECATED144": DEPRECATED144,
    "DEPRECATED145": DEPRECATED145,
    "DEPRECATED146": DEPRECATED146,
    "DEPRECATED147": DEPRECATED147,
    "DEPRECATED148": DEPRECATED148,
    "DEPRECATED149": DEPRECATED149,
    "DEPRECATED150": DEPRECATED150,
    "DEPRECATED151": DEPRECATED151,
    "DEPRECATED152": DEPRECATED152,
    "DEPRECATED153": DEPRECATED153,
    "DEPRECATED154": DEPRECATED154,
    "DEPRECATED155": DEPRECATED155,
    "DEPRECATED156": DEPRECATED156,
    "DEPRECATED157": DEPRECATED157,
    "DEPRECATED158": DEPRECATED158,
    "DEPRECATED159": DEPRECATED159,
    "DEPRECATED160": DEPRECATED160,
    "DEPRECATED161": DEPRECATED161,
    "DEPRECATED162": DEPRECATED162,
    "DEPRECATED163": DEPRECATED163,
    "DEPRECATED164": DEPRECATED164,
    "DEPRECATED165": DEPRECATED165,
    "DEPRECATED166": DEPRECATED166,
    "DEPRECATED167": DEPRECATED167,
    "DEPRECATED168": DEPRECATED168,
    "DEPRECATED169": DEPRECATED169,
    "DEPRECATED170": DEPRECATED170,
    "DEPRECATED171": DEPRECATED171,
    "DEPRECATED172": DEPRECATED172,
    "DEPRECATED173": DEPRECATED173,
    "DEPRECATED174": DEPRECATED174,
    "DEPRECATED175": DEPRECATED175,
    "DEPRECATED176": DEPRECATED176,
    "DEPRECATED177": DEPRECATED177,
    "DEPRECATED178": DEPRECATED178,
    "DEPRECATED179": DEPRECATED179,
    "DEPRECATED180": DEPRECATED180,
    "DEPRECATED181": DEPRECATED181,
    "DEPRECATED182": DEPRECATED182,
    "DEPRECATED183": DEPRECATED183,
    "DEPRECATED184": DEPRECATED184,
    "DEPRECATED185": DEPRECATED185,
    "DEPRECATED186": DEPRECATED186,
    "DEPRECATED187": DEPRECATED187,
    "DEPRECATED188": DEPRECATED188,
    "DEPRECATED189": DEPRECATED189,
    "DEPRECATED190": DEPRECATED190,
    "DEPRECATED191": DEPRECATED191,
    "DEPRECATED192": DEPRECATED192,
    "DEPRECATED193": DEPRECATED193,
    "DEPRECATED194": DEPRECATED194,
    "DEPRECATED195": DEPRECATED195,
    "DEPRECATED196": DEPRECATED196,
    "DEPRECATED197": DEPRECATED197,
    "DEPRECATED198": DEPRECATED198,
    "DEPRECATED199": DEPRECATED199,
    "DEPRECATED200": DEPRECATED200,
    "DEPRECATED201": DEPRECATED201,
    "DEPRECATED202": DEPRECATED202,
    "DEPRECATED203": DEPRECATED203,
    "DEPRECATED204": DEPRECATED204,
    "DEPRECATED205": DEPRECATED205,
    "DEPRECATED206": DEPRECATED206,
    "DEPRECATED207": DEPRECATED207,
    "DEPRECATED208": DEPRECATED208,
    "DEPRECATED209": DEPRECATED209,
    "DEPRECATED210": DEPRECATED210,
    "DEPRECATED211": DEPRECATED211,
    "DEPRECATED212": DEPRECATED212,
    "DEPRECATED213": DEPRECATED213,
    "DEPRECATED214": DEPRECATED214,
    "DEPRECATED215": DEPRECATED215,
    "DEPRECATED216": DEPRECATED216,
    "DEPRECATED217": DEPRECATED217,
    "DEPRECATED218": DEPRECATED218,
    "DEPRECATED219": DEPRECATED219,
    "DEPRECATED220": DEPRECATED220,
    "DEPRECATED221": DEPRECATED221,
    "DEPRECATED222": DEPRECATED222,
    "DEPRECATED223": DEPRECATED223,
    "DEPRECATED224": DEPRECATED224,
    "DEPRECATED225": DEPRECATED225,
    "DEPRECATED226": DEPRECATED226,
    "DEPRECATED227": DEPRECATED227,
    "DEPRECATED228": DEPRECATED228,
    "DEPRECATED229": DEPRECATED229,
    "DEPRECATED230": DEPRECATED230,
    "DEPRECATED231": DEPRECATED231,
    "DEPRECATED232": DEPRECATED232,
    "DEPRECATED233": DEPRECATED233,
    "DEPRECATED234": DEPRECATED234,
    "DEPRECATED235": DEPRECATED235,
    "DEPRECATED236": DEPRECATED236,
    "DEPRECATED237": DEPRECATED237,
    "DEPRECATED238": DEPRECATED238,
    "DEPRECATED239": DEPRECATED239,
    "DEPRECATED240": DEPRECATED240,
    "DEPRECATED241": DEPRECATED241,
    "DEPRECATED242": DEPRECATED242,
    "DEPRECATED243": DEPRECATED243,
    "DEPRECATED244": DEPRECATED244,
    "DEPRECATED245": DEPRECATED245,
    "DEPRECATED246": DEPRECATED246,
    "DEPRECATED247": DEPRECATED247,
    "DEPRECATED248": DEPRECATED248,
    "DEPRECATED249": DEPRECATED249,
    "DEPRECATED250": DEPRECATED250,
    "DEPRECATED251": DEPRECATED251,
    "DEPRECATED252": DEPRECATED252,
    "DEPRECATED253": DEPRECATED253,
    "DEPRECATED254": DEPRECATED254,
    "DEPRECATED255": DEPRECATED255,
    "DEPRECATED256": DEPRECATED256,
    "DEPRECATED257": DEPRECATED257,
    "DEPRECATED258": DEPRECATED258,
    "DEPRECATED259": DEPRECATED259,
    "DEPRECATED260": DEPRECATED260,
    "DEPRECATED261": DEPRECATED261,
    "DEPRECATED262": DEPRECATED262,
    "DEPRECATED263": DEPRECATED263,
    "DEPRECATED264": DEPRECATED264,
    "DEPRECATED265": DEPRECATED265,
    "DEPRECATED266": DEPRECATED266,
    "DEPRECATED267": DEPRECATED267,
    "DEPRECATED268": DEPRECATED268,
    "DEPRECATED269": DEPRECATED269,
    "DEPRECATED270": DEPRECATED270,
    "DEPRECATED271": DEPRECATED271,
    "DEPRECATED272": DEPRECATED272,
    "DEPRECATED273": DEPRECATED273,
    "DEPRECATED274": DEPRECATED274,
    "DEPRECATED275": DEPRECATED275,
    "DEPRECATED276": DEPRECATED276,

    "PERSON": PERSON,
    "NORP": NORP,
    "FACILITY": FACILITY,
    "ORG": ORG,
    "GPE": GPE,
    "LOC": LOC,
    "PRODUCT": PRODUCT,
    "EVENT": EVENT,
    "WORK_OF_ART": WORK_OF_ART,
    "LANGUAGE": LANGUAGE,

    "DATE": DATE,
    "TIME": TIME,
    "PERCENT": PERCENT,
    "MONEY": MONEY,
    "QUANTITY": QUANTITY,
    "ORDINAL": ORDINAL,
    "CARDINAL": CARDINAL,

    "acomp": acomp,
    "advcl": advcl,
    "advmod": advmod,
    "agent": agent,
    "amod": amod,
    "appos": appos,
    "attr": attr,
    "aux": aux,
    "auxpass": auxpass,
    "cc": cc,
    "ccomp": ccomp,
    "complm": complm,
    "conj": conj,
    "cop": cop, # U20
    "csubj": csubj,
    "csubjpass": csubjpass,
    "dep": dep,
    "det": det,
    "dobj": dobj,
    "expl": expl,
    "hmod": hmod,
    "hyph": hyph,
    "infmod": infmod,
    "intj": intj,
    "iobj": iobj,
    "mark": mark,
    "meta": meta,
    "neg": neg,
    "nmod": nmod,
    "nn": nn,
    "npadvmod": npadvmod,
    "nsubj": nsubj,
    "nsubjpass": nsubjpass,
    "num": num,
    "number": number,
    "oprd": oprd,
    "obj": obj, # U20
    "obl": obl, # U20
    "parataxis": parataxis,
    "partmod": partmod,
    "pcomp": pcomp,
    "pobj": pobj,
    "poss": poss,
    "possessive": possessive,
    "preconj": preconj,
    "prep": prep,
    "prt": prt,
    "punct": punct,
    "quantmod": quantmod,
    "rcmod": rcmod,
    "relcl": relcl,
    "root": root,
    "xcomp": xcomp,

    "acl": acl,
    "LAW": LAW,
    "MORPH": MORPH,
    "_": _,
}


def sort_nums(x):
    return x[1]


NAMES = [it[0] for it in sorted(IDS.items(), key=sort_nums)]
# Unfortunate hack here, to work around problem with long cpdef enum
# (which is generating an enormous amount of C++ in Cython 0.24+)
# We keep the enum cdef, and just make sure the names are available to Python
locals().update(IDS)
