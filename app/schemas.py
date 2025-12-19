from pydantic import BaseModel

#To be used to identify the input schema of request body
class ReqBody(BaseModel):
    title: str
    content: str

#To be used to identify the output schema of created post
class PostResponse(BaseModel):
    id: int
    title: str
    content: str