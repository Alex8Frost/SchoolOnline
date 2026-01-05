from pydantic import BaseModel
from typing import Dict, Any, Optional

class ExecutionRequest(BaseModel):
    variables: Dict[str, Any]

class ExecutionResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None