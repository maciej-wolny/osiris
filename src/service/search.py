def generate_query(value):
    value = value.lower()
    return {
        "bool": {
            "should": [
                {
                    "fuzzy": {
                        "name_short": {
                            "value": value,
                            "fuzziness": "AUTO"
                        }
                    }
                },
                {
                    "prefix": {
                        "krs": value
                    }
                },
                {
                    "prefix": {
                        "nip": value
                    }
                },
            ]
        }
    }
