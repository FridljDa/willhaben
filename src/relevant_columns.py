relevant_keys = [
        'ADDITIONAL_COST/DEPOSIT',
        'ADDITIONAL_COST/FEE',
        'AVAILABLE_DATE',
        'BUILDING_CONDITION',
        'BUILDING_TYPE',
        'Befristung',
        'DESCRIPTION',
        'DURATION/HASTERMLIMIT',
        'DURATION/TERMLIMITTEXT',
        'ESTATE_PREFERENCE',
        'ESTATE_SIZE',
        'FLOOR',
        'FLOOR_SURFACE',
        'GENERAL_TEXT_ADVERT/Lage',
        'GENERAL_TEXT_ADVERT/Sonstiges',
        'HEATING',
        'LOCATION/ADDRESS_1',
        'NO_OF_ROOMS',
        'OWNAGETYPE',
        'PROPERTY_TYPE',
        'RENTAL_PRICE/ADDITIONAL_COST_GROSS',
        'RENTAL_PRICE/PER_MONTH',
        'RENTAL_PRICE/TOTAL_ENCUMBRANCE',
        'Verfuegbarkeit',
        'available_date',
        'url'
    ]

dtypes_columns = {
    'ADDITIONAL_COST/DEPOSIT': 'string',  # Example: '1000', '3 BMM'
    'ADDITIONAL_COST/FEE': 'string',     # Example: '', ''
    'AVAILABLE_DATE': 'datetime',       # Example: '01.06.2025'
    'BUILDING_CONDITION': 'string',     # Example: 'Neuwertig', 'Sehr gut/gut'
    'BUILDING_TYPE': 'string',          # Example: 'Altbau', 'Neubau'
    'Befristung': 'string',             # Example: 'unbefristet', 'befristet'
    'DESCRIPTION': 'string',            # Example: HTML content
    'DURATION/HASTERMLIMIT': 'bool',    # Example: '', ''
    'DURATION/TERMLIMITTEXT': 'string', # Example: '', '5 Jahre'
    'ESTATE_PREFERENCE': 'string',      # Example: '', ''
    'ESTATE_SIZE': 'float',             # Example: '75', '42'
    'FLOOR': 'int',                     # Example: '', '1', '2'
    'FLOOR_SURFACE': 'float',           # Example: '', ''
    'GENERAL_TEXT_ADVERT/Lage': 'string', # Example: HTML content
    'GENERAL_TEXT_ADVERT/Sonstiges': 'string', # Example: HTML content
    'HEATING': 'string',                # Example: '', 'Holz', 'Zentralheizung'
    'LOCATION/ADDRESS_1': 'string',     # Example: 'Hamburgerstraße', 'Schütterstr. 23-25'
    'NO_OF_ROOMS': 'float',             # Example: '1', '1.5'
    'OWNAGETYPE': 'string',             # Example: 'Miete'
    'PROPERTY_TYPE': 'string',          # Example: 'Zimmer/WG', 'Garconniere'
    'RENTAL_PRICE/ADDITIONAL_COST_GROSS': 'float', # Example: '', '126.19'
    'RENTAL_PRICE/PER_MONTH': 'float',  # Example: '', '694.22', '876.19'
    'RENTAL_PRICE/TOTAL_ENCUMBRANCE': 'float', # Example: '', '876.19'
    'Verfuegbarkeit': 'string',         # Example: '', ''
    'available_date': 'datetime',       # Example: '01.06.2025'
    'url': 'string'                     # Example: URLs
}
