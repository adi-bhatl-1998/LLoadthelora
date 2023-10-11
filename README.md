# LLoadthelora
Web server that does text to image and LOra model finetuning 
API design :
This project contains 2 API’s
1. Get
2. Post
The @app.get API is requested when the http://localhost:8000 receives an incoming request for
connection .
It returns a simple html Form which is used to get image generation parameters from the user .
The parameters collected are
modelid:str
total_nm_img_prompt:int
negative_prompt:Optional[str]
text_prompt:str
inference_steps:int
guidance_scale:float
strength:float
manual_seed:int
lora_hugging_face_1:Optional[str]---->this is the link or path
to the lora model
weight_name_1:Optional[str]----------->name of the lora weight
If its named anything
Other than the default
Value
LORA_WEIGHT_NAME = "pytorch_lora_weights.bin"
LORA_WEIGHT_NAME_SAFE="pytorch_lora_weights.safetensors"
weight_name_2:Optional[str]
lora_hugging_face_2:Optional[str]
cross_attention_kwargs:Optional[float]=1.0
On submitting the form a post method , another api called @app.post(“/submit”) is triggered
which collects all the data passed to the html from the user
2. API for image generation is
“@app.post("/submit",response_class=FileResponse)”
On submitting the form the api with the path parameters (“/submit”) will be called .
The process of image generation is divided into 2 function calls .
generate_without_lora
|||
|—----------------|-------------------|
| 1 create pipe |
| 2 create image |
|_______________________|
2 .
create_with_lora
||
|--------------------------|--------------------------------|
| 1 create pipe |
| 2 incorplora_safetenso |
| 2.1load_lora_weights |
| 3 create image |
|___________________________________|
def create_pipe(modelid):
pipe =
StableDiffusionPipeline.from_pretrained(modelid,use_safetensors=True)
.to("mps")
return pipe
Creates a stable diffusion pipeline with modelid that is a text to
image generation model here which by default is
"runwayml/stable-diffusion-v1-5"
2.If the link and and the weight name is provided then
pipe.load_lora_weights(lora_model_path,weight_name=weight_name) will
be called . My observation has shown that not all the lora models
have been given the default name of
LORA_WEIGHT_NAME = "pytorch_lora_weights.bin"
LORA_WEIGHT_NAME_SAFE = "pytorch_lora_weights.safetensors"
def incorplora_safetensor(pipe,lora_model_path,weight_name):
print("pipe inside incorplora_safetensors")
if weight_name=="null":
pipe.load_lora_weights(lora_model_path)
else:
pipe.load_lora_weights(lora_model_path,weight_name=weight_name)
return pipe
Insightful rationale behind your design decisions
:
(html)
( fastapi )
( uvicorn )
Selection of web framework:
It was either fastapi or flask .
On doing a small poc on both the frameworks found flask to be
time consuming to implement when compared to fastapi as fastapi was
direct and easy to implement and also had easier syntax to deal with
.
Fastapi allows usage of uvicorn which is a asgi server which if
needed can permit the usage of parallelism and concurrency and is an
upgrade to wsgi.
On further research comparing the fastapi and flask , the project I
intended to do did not have much front end deployment and my finding
suggested fast api to be a better use case .
Fastapi vs Flask
Speed : fastapi
data validation : fastapi
Ease of use and learning curve: fastapi
Simplicity : fastapi
Have used asynchronous functions like async def and await .
@app.post("/submit", response_class=FileResponse)
async def submit(modelid:str=Form("runwayml/stable-diffusion-v1-5")
,text_prompt:str=Form(...),total_nm_img_prompt:int=Form(1),
inference_steps:int=Form(30),
guidance_scale:float=Form(7.5),manual_seed:int=Form(...),negative_pro
mpt:Optional[str]=Form(None),
strength:float=Form(1.0),lora_hugging_face_1:Optional[str]=Form("null
") ,lora_hugging_face_2:Optional[str]=Form("null"),
weight_name_2:Optional[str]=Form("null"),weight_name_1:Optional[str]=
Form("null") ,cross_attention_kwargs:Optional[float]=Form(1)
):
model_data.modelid=modelid
model_data.total_nm_img_prompt=total_nm_img_prompt
model_data.negative_prompt=negative_prompt
if negative_prompt=="null":
model_data.negative_prompt=""
else :
model_data.negative_prompt = negative_prompt
model_data.text_prompt=text_prompt
model_data.inference_steps=inference_steps
model_data.guidance_scale=guidance_scale
model_data.strength=strength
model_data.manual_seed=manual_seed
model_data.lora_hugging_face_1=lora_hugging_face_1
model_data.lora_hugging_face_2=lora_hugging_face_2
model_data.weight_name_1=weight_name_1
model_data.weight_name_2=weight_name_2
model_data.cross_attention_kwargs=cross_attention_kwargs
images=0
if model_data.lora_hugging_face_1=="null" and
model_data.lora_hugging_face_2=="null":
print("entering generate_without_lora")
images=await generate_without_lora(model_data)
print("image address returned")
return images
else:
print("entering create_with_lora\n\n ")
images=await create_with_lora(model_data)
print("out of create_with_lora\n\n ")
while(images==0):
print("print check images for 0")
return images
# if __name__=="__main__":
# uvicorn.run("main:app",port=8000,reload=True)
Computation
So the await keyword frees the server to execute other tasks , although in my code i dont have
lot of other tasks if i have not used multiple workers to handle requests .
When multiple workers are used they handle multiple requests which can be computed at the
same time without any memory accessing issues .
  
