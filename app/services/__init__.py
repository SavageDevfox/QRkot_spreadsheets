ROW_COUNT = 100

SPREADSHEET_BODY = {
        'properties': {
            'title': 'Отчет от {date}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': 3
                    }
                }
            }
        ]
}
