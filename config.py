CONFIG = {
    "search_query":  "%22smart%20home*%22%20%22energy%20efficien*%22",
    "replace": {
        "%22smart%20home*%22%20%22energy%20efficien*%22",
        '%22smart%20home*%22%20%22energy%22'
    },
    "scopus_search_queries" : [
        '"smart home*" AND "energy efficien*"',
        '"smart home*" AND "energy" AND "efficien*"',
        '"smart home*"',
        '"energy" AND "efficien*"',
        '"energy efficien*"',
    ],
    "science_direct_search_queries": [
        'efficien',
        # 'energy',
        # '"smart home"',
        # '"energy efficien"',
    ],


    "rebound_terms": ['rebound effect', 'jevons paradox', 'khazzoom-brookes postulate'],
    "heuristic" : {"rebound", "jevons", "khazzoom-brookes"}
}

OUTPUT_FILES = "output_files"