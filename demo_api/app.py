from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator

app = FastAPI(title="tgden Demo API")

class ErrorResponse(BaseModel):
    error: str
    field: str | None
    message: str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]

    loc = first_error.get("loc", [])
    field = loc[-1] if loc else None
    message = first_error.get("msg", "Invalid request")

    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "field": field,
            "message": message,
        },
    )

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("email", mode="before")
    @classmethod
    def email_must_not_have_spaces(cls, value):
        if isinstance(value, str) and value != value.strip():
            raise ValueError("Email must not contain leading or trailing spaces")
        return value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool


@app.post(
    "/users",
    response_model=UserResponse,
    responses={400: {"model": ErrorResponse}},
)
def create_user(payload: CreateUserRequest):
    return UserResponse(
        id=1,
        email=payload.email,
        is_active=True,
    )

