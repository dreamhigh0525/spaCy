from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...symbols import ORTH, LEMMA
from ...util import update_exc


_exc = {
    "tayo'y": [{ORTH: "tayo", LEMMA: "tayo"}, {ORTH: "'y", LEMMA: "ay"}],
    "isa'y": [{ORTH: "isa", LEMMA: "isa"}, {ORTH: "'y", LEMMA: "ay"}],
    "baya'y": [{ORTH: "baya", LEMMA: "bayan"}, {ORTH: "'y", LEMMA: "ay"}],
    "sa'yo": [{ORTH: "sa", LEMMA: "sa"}, {ORTH: "'yo", LEMMA: "iyo"}],
    "ano'ng": [{ORTH: "ano", LEMMA: "ano"}, {ORTH: "'ng", LEMMA: "ang"}],
    "siya'y": [{ORTH: "siya", LEMMA: "siya"}, {ORTH: "'y", LEMMA: "ay"}],
    "nawa'y": [{ORTH: "nawa", LEMMA: "nawa"}, {ORTH: "'y", LEMMA: "ay"}],
    "papa'no": [{ORTH: "papa'no", LEMMA: "papaano"}],
    "'di": [{ORTH: "'di", LEMMA: "hindi"}],
}


TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
