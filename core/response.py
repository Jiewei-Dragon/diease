from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

# 自定义响应码（对应原 Go 代码的 response.ErrXXX）
class ErrorCode:
    ErrInvalidJSON = {"code": 400, "msg": "无效的JSON格式"}
    ErrValidation = {"code": 400, "msg": "参数验证失败"}
    ErrUnknown = {"code": 500, "msg": "未知错误"}
    Success = {"code": 200, "msg": "操作成功"}

# 成功响应
def success_response(data: dict = None):
    result = {
        "code": ErrorCode.Success["code"],
        "msg": ErrorCode.Success["msg"],
        "data": data or {}
    }
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

def error_response(error_code: dict, detail: str = None):
    result = {
        "code": error_code["code"],
        "msg": detail or error_code["msg"]
    }
    return JSONResponse(content=result, status_code=status.HTTP_400_BAD_REQUEST)