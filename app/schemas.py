from pydantic import BaseModel

class ReqBody(BaseModel):
    title: str
    content: str