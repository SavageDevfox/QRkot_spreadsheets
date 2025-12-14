from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services import SPREADSHEET_BODY

FORMAT = '%Y/%m/%d %H:%M:%S'

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}


async def create_spreadsheets(
        wrapper_services: Aiogoogle,
        spreadsheet_body: dict = SPREADSHEET_BODY,
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(spreadsheet_body)
    spreadsheet_body['properties']['title'] = spreadsheet_body['properties'][
        'title'].format(date=datetime.now().strftime(FORMAT))
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId'] # noqa
    return '1huc9h8xEvI1naf527RPknyCtgTyz4mykFPK2aTzyALU'


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields='id'
        ))


async def update_spreadsheets_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for proj in projects:
        duration = proj.close_date - proj.create_date
        duration_str = str(duration)

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
