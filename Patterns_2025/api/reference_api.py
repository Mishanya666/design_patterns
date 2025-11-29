from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any
from Src.Services.reference_service import reference_service

router = APIRouter()
service = reference_service()

# Допустимые типы справочников
VALID_TYPES = {"nomenclature", "range", "category", "storage"}


@router.get("/api/{ref_type}")
async def get_all(ref_type: str = Path(..., description="Тип справочника")):
    if ref_type not in VALID_TYPES:
        raise HTTPException(status_code=404, detail="Справочник не найден")

    data = service.get_all(ref_type)
    return {"data": data}


# получить один
@router.get("/api/{ref_type}/{item_id}")
async def get_one(
        ref_type: str = Path(..., description="Тип справочника"),
        item_id: str = Path(..., description="ID элемента")
):
    if ref_type not in VALID_TYPES:
        raise HTTPException(status_code=404, detail="Справочник не найден")

    item = service.get_by_id(ref_type, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Элемент не найден")

    return {"data": item}


# добавить новый
@router.put("/api/{ref_type}")
async def add_item(
        ref_type: str = Path(..., description="Тип справочника"),
        item: Dict[str, Any] = None
):
    if ref_type not in VALID_TYPES:
        raise HTTPException(status_code=404, detail="Справочник не найден")

    result = service.add(ref_type, item or {})
    if service.is_error:
        raise HTTPException(status_code=400, detail=service.error_text)

    return {"data": result, "message": "Элемент успешно добавлен"}


# изменить
@router.patch("/api/{ref_type}/{item_id}")
async def update_item(
        ref_type: str = Path(...),
        item_id: str = Path(...),
        item: Dict[str, Any] = None
):
    if ref_type not in VALID_TYPES:
        raise HTTPException(status_code=404, detail="Справочник не найден")

    result = service.update(ref_type, item_id, item or {})
    if service.is_error:
        raise HTTPException(status_code=400, detail=service.error_text)

    return {"data": result, "message": "Элемент успешно обновлён"}


# удалить
@router.delete("/api/{ref_type}/{item_id}")
async def delete_item(
        ref_type: str = Path(...),
        item_id: str = Path(...)
):
    if ref_type not in VALID_TYPES:
        raise HTTPException(status_code=404, detail="Справочник не найден")

    success = service.delete(ref_type, item_id)
    if service.is_error:
        raise HTTPException(status_code=400, detail=service.error_text)

    return {"deleted": success, "message": "Элемент успешно удалён" if success else "Удаление не выполнено"}