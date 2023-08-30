from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name':'Sarthak'}}

@app.get('/about')
def about():
    return{'data':'about page'}

@app.get('/blog')
def index(limit,pub:bool=True):
    if pub:
        return{'data':f'{limit} blogs from db which are {pub}'}
    else:
        return{"data":"only unpublished "}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id }

@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': {1,2}}

class Blog(BaseModel):
    title:str
    body: str
    publish: Optional[bool]


@app.post('/blog')
def create_blog(blog:Blog):
    return {'data' :f'this is the {blog.title} from {blog.body} and {blog.publish} '}

# if __name__=="__main__":
#   uvicorn.run(app, host="127.0.0.1",port=9000)