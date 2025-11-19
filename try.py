"""from langchain_openai import ChatOpenAI
#import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict, Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI



import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
print(model.invoke("hi"))"""
from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types    

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly glazed tea bowl. The setting is his rustic, sun-drenched workshop with pottery wheels and shelves of clay pots in the background. The scene is illuminated by soft, golden hour light streaming through a window, highlighting the fine texture of the clay and the fabric of his apron. Captured with an 85mm portrait lens, resulting in a soft, blurred background (bokeh). The overall mood is serene and masterful.",
)

image_parts = [part for part in response.parts if part.inline_data]

if image_parts:
    image = image_parts[0].as_image()
    print(image)
    image.save('photorealistic_example.png')
    image.show()