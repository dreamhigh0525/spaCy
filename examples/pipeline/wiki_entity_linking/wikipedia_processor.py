# coding: utf-8
from __future__ import unicode_literals

import re
import bz2
import csv
import datetime

"""
Process a Wikipedia dump to calculate entity frequencies and prior probabilities in combination with certain mentions.
"""


# TODO: remove hardcoded paths
ENWIKI_DUMP = 'C:/Users/Sofie/Documents/data/wikipedia/enwiki-20190320-pages-articles-multistream.xml.bz2'
ENWIKI_INDEX = 'C:/Users/Sofie/Documents/data/wikipedia/enwiki-20190320-pages-articles-multistream-index.txt.bz2'

map_alias_to_link = dict()

# these will/should be matched ignoring case
wiki_namespaces = ["b", "betawikiversity", "Book", "c", "Category", "Commons",
                   "d", "dbdump", "download", "Draft", "Education", "Foundation",
                   "Gadget", "Gadget definition", "gerrit", "File", "Help", "Image", "Incubator",
                   "m", "mail", "mailarchive", "media", "MediaWiki", "MediaWiki talk", "Mediawikiwiki",
                   "MediaZilla", "Meta", "Metawikipedia", "Module",
                   "mw", "n", "nost", "oldwikisource", "outreach", "outreachwiki", "otrs", "OTRSwiki",
                   "Portal", "phab", "Phabricator", "Project", "q", "quality", "rev",
                   "s", "spcom", "Special", "species", "Strategy", "sulutil", "svn",
                   "Talk", "Template", "Template talk", "Testwiki", "ticket", "TimedText", "Toollabs", "tools", "tswiki",
                   "User", "User talk", "v", "voy",
                   "w", "Wikibooks", "Wikidata", "wikiHow", "Wikinvest", "wikilivres", "Wikimedia", "Wikinews",
                   "Wikipedia", "Wikipedia talk", "Wikiquote", "Wikisource", "Wikispecies", "Wikitech",
                   "Wikiversity", "Wikivoyage", "wikt", "wiktionary", "wmf", "wmania", "WP"]

# find the links
link_regex = re.compile(r'\[\[[^\[\]]*\]\]')

# match on interwiki links, e.g. `en:` or `:fr:`
ns_regex = r":?" + "[a-z][a-z]" + ":"

# match on Namespace: optionally preceded by a :
for ns in wiki_namespaces:
    ns_regex += "|" + ":?" + ns + ":"

ns_regex = re.compile(ns_regex, re.IGNORECASE)


def read_wikipedia_prior_probs(prior_prob_output):
    """
    Read the XML wikipedia data and parse out intra-wiki links to estimate prior probabilities
    The full file takes about 2h to parse 1100M lines (update printed every 5M lines).
    It works relatively fast because we don't care about which article we parsed the interwiki from,
    we just process line by line.
    """

    with bz2.open(ENWIKI_DUMP, mode='rb') as file:
        line = file.readline()
        cnt = 0
        while line:
            if cnt % 5000000 == 0:
                print(datetime.datetime.now(), "processed", cnt, "lines of Wikipedia dump")
            clean_line = line.strip().decode("utf-8")

            aliases, entities, normalizations = get_wp_links(clean_line)
            for alias, entity, norm in zip(aliases, entities, normalizations):
                _store_alias(alias, entity, normalize_alias=norm, normalize_entity=True)
                _store_alias(alias, entity, normalize_alias=norm, normalize_entity=True)

            line = file.readline()
            cnt += 1

    # write all aliases and their entities and occurrences to file
    with open(prior_prob_output, mode='w', encoding='utf8') as outputfile:
        outputfile.write("alias" + "|" + "count" + "|" + "entity" + "\n")
        for alias, alias_dict in sorted(map_alias_to_link.items(), key=lambda x: x[0]):
            for entity, count in sorted(alias_dict.items(), key=lambda x: x[1], reverse=True):
                outputfile.write(alias + "|" + str(count) + "|" + entity + "\n")


def _store_alias(alias, entity, normalize_alias=False, normalize_entity=True):
    alias = alias.strip()
    entity = entity.strip()

    # remove everything after # as this is not part of the title but refers to a specific paragraph
    if normalize_entity:
        # wikipedia titles are always capitalized
        entity = _capitalize_first(entity.split("#")[0])
    if normalize_alias:
        alias = alias.split("#")[0]

    if alias and entity:
        alias_dict = map_alias_to_link.get(alias, dict())
        entity_count = alias_dict.get(entity, 0)
        alias_dict[entity] = entity_count + 1
        map_alias_to_link[alias] = alias_dict


def get_wp_links(text):
    aliases = []
    entities = []
    normalizations = []

    matches = link_regex.findall(text)
    for match in matches:
        match = match[2:][:-2].replace("_", " ").strip()

        if ns_regex.match(match):
            pass  # ignore namespaces at the beginning of the string

        # this is a simple link, with the alias the same as the mention
        elif "|" not in match:
            aliases.append(match)
            entities.append(match)
            normalizations.append(True)

        # in wiki format, the link is written as [[entity|alias]]
        else:
            splits = match.split("|")
            entity = splits[0].strip()
            alias = splits[1].strip()
            # specific wiki format  [[alias (specification)|]]
            if len(alias) == 0 and "(" in entity:
                alias = entity.split("(")[0]
                aliases.append(alias)
                entities.append(entity)
                normalizations.append(False)
            else:
                aliases.append(alias)
                entities.append(entity)
                normalizations.append(False)

    return aliases, entities, normalizations


def _capitalize_first(text):
    if not text:
        return None
    result = text[0].capitalize()
    if len(result) > 0:
        result += text[1:]
    return result


def write_entity_counts(prior_prob_input, count_output, to_print=False):
    """ Write entity counts for quick access later  """
    entity_to_count = dict()
    total_count = 0

    with open(prior_prob_input, mode='r', encoding='utf8') as prior_file:
        # skip header
        prior_file.readline()
        line = prior_file.readline()

        while line:
            splits = line.replace('\n', "").split(sep='|')
            # alias = splits[0]
            count = int(splits[1])
            entity = splits[2]

            current_count = entity_to_count.get(entity, 0)
            entity_to_count[entity] = current_count + count

            total_count += count

            line = prior_file.readline()

    with open(count_output, mode='w', encoding='utf8') as entity_file:
        entity_file.write("entity" + "|" + "count" + "\n")
        for entity, count in entity_to_count.items():
            entity_file.write(entity + "|" + str(count) + "\n")

    if to_print:
        for entity, count in entity_to_count.items():
            print("Entity count:", entity, count)
        print("Total count:", total_count)


def get_all_frequencies(count_input):
    entity_to_count = dict()
    with open(count_input, 'r', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        # skip header
        next(csvreader)
        for row in csvreader:
            entity_to_count[row[0]] = int(row[1])

    return entity_to_count

