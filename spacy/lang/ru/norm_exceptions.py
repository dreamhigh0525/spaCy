_exc = {
    # Slang
    "прив": "привет",
    "дарова": "привет",
    "дак": "так",
    "дык": "так",
    "здарова": "привет",
    "пакедава": "пока",
    "пакедаво": "пока",
    "ща": "сейчас",
    "спс": "спасибо",
    "пжлст": "пожалуйста",
    "плиз": "пожалуйста",
    "ладненько": "ладно",
    "лады": "ладно",
    "лан": "ладно",
    "ясн": "ясно",
    "всм": "всмысле",
    "хош": "хочешь",
    "хаюшки": "привет",
    "оч": "очень",
    "че": "что",
    "чо": "что",
    "шо": "что",
}


NORM_EXCEPTIONS = {}

for string, norm in _exc.items():
    NORM_EXCEPTIONS[string] = norm
    NORM_EXCEPTIONS[string.title()] = norm
