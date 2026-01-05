from fastapi import APIRouter
from schemas.execution import ExecutionRequest, ExecutionResponse
from services.code_executor import MagazineExecutor

router = APIRouter(prefix="/api/companies", tags=["companies"])

@router.post("/1/run")
async def run_company_1(request: ExecutionRequest):
    """
    Запускает симуляцию работы издательства с заданными переменными.
    
    Ожидает в теле запроса объект с переменными:
    - title: заголовок статьи (строка)
    - author: автор статьи (строка) 
    - year: год публикации (число 1900-2100)
    - word_count: количество слов (положительное число)
    
    Возвращает результат выполнения кода или сообщение об ошибке.
    """
    executor = MagazineExecutor()
    is_valid, error = executor.validate_variables(request.variables)
    
    if not is_valid:
        return ExecutionResponse(success=False, error=error)
    
    success, result = executor.execute(request.variables)
    return ExecutionResponse(
        success=success,
        output=result if success else None,
        error=result if not success else None
    )