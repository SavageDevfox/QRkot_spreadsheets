from urllib.parse import urljoin

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.project import project_crud
from app.services.google_service import (
    create_spreadsheets, set_user_permissions, update_spreadsheets_value
)

TABLE_BASE_URL = 'https://docs.google.com/spreadsheets/d/'
router = APIRouter()


@router.post("/update_tables_data/")
async def update_tables_data(
        session=Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await project_crud.get_projects_by_completion_rate(session)
    spreadsheet_id = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(spreadsheet_id, projects, wrapper_services)
    return {
        "status": "success",
        "report_url": urljoin(TABLE_BASE_URL, spreadsheet_id)
    }
