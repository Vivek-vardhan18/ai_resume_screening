from pydantic import BaseModel

class ResumeResponse(BaseModel):
    id: int
    filename: str
    score: int

    class Config:
        orm_mode = True