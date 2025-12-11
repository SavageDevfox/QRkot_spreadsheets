from datetime import datetime

from aiogoogle import Aiogoogle

FORMAT = '%Y/%m/%d %H:%M:%S'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    return '1huc9h8xEvI1naf527RPknyCtgTyz4mykFPK2aTzyALU'


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    return None


async def update_spreadsheets_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    # Базовая структура таблицы
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    # Добавление строк по проектам
    for proj in projects:
        duration = proj.close_date - proj.create_date
        duration_str = str(duration)  # timedelta -> строка

        new_row = [
            proj.name,
            duration_str,
            proj.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E200',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
