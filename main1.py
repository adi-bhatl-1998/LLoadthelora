from fastapi import FastAPI, HTTPException, File, UploadFile ,Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from pydantic import BaseModel,validators

app=FastAPI()
templates=Jinja2Templates(directory="Templates")
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context={'request':request}
    return templates.TemplateResponse("index.html",context)

class model_data(BaseModel):
    text_prompt:str
    inference_steps:int
    guidance_scale:float
    strength:float

@app.post("/submit",response_model=model_data)
async def submit(text_prompt:str=Form(...) , inference_steps:int=Form(...), guidance_scale:float=Form(...),
                 strength:float=Form(...)):
    return model_data(text_prompt=text_prompt,inference_steps=inference_steps,guidance_scale=guidance_scale,strength=strength)
    