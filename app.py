#libraries to build graph
from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

#library for gemini
from langchain_google_genai import ChatGoogleGenerativeAI

#other libraries
from dotenv import load_dotenv
load_dotenv()
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

#to generate list of sections given a topic based on user's competence
def generate_plan(state):
    concept=state["concept"]
    level=state["level"]    
    
    class Section(BaseModel):
        section: str

    class Sections(BaseModel):
        sections: List[Section] = Field(
            description=f"List of sections",
        )

    with open(os.path.join(BASE_DIR,"prompts/generate_sections.txt"), "r", encoding="utf-8") as f:
        generate_sections_prompt = f.read()

    structured_llm = model.with_structured_output(Sections)
    result = structured_llm.invoke(generate_sections_prompt.format(concept=concept, level=level))
    sections_list = [section.section for section in result.sections]

    return {"sections":sections_list}


#to write each section based on user's competence
def write_sections(state):        
    with open(os.path.join(BASE_DIR,"prompts/write_sections.txt"), "r", encoding="utf-8") as f:
        write_sections_prompt = f.read()
        
    response=model.invoke(write_sections_prompt.format(level=state["level"], chapter=state["concept"], section=state["sections"][state["counter"]]))
    
    return {"messages": response, "counter": state["counter"]+1}


def router(state):
    if state["counter"] == len(state["sections"]):
        return "final_draft"
    else:
        return "write_sections"


#to generate a cohesive article using the sections already written
def final_draft(state):
    report=state["concept"]+"\n\n"
    for i in range(len(state["sections"])):
        report=report+state["sections"][i]+"\n"
        report=report+state["messages"][i].content+"\n\n"
    
    with open(os.path.join(BASE_DIR,"prompts/write_chapter.txt"), "r", encoding="utf-8") as f:
        write_chapter_prompt = f.read()
    
    response=model.invoke([SystemMessage(content=write_chapter_prompt.format(level=state["level"])),
                                             HumanMessage(content=report)])

    return{"report": response.content}


#to rewrite the article in user's desired language if it is not english
def desired_language(state):
    
    with open(os.path.join(BASE_DIR,"prompts/language_change.txt"), "r", encoding="utf-8") as f:
        language_change_prompt = f.read()
    
    response=model.invoke([SystemMessage(content=language_change_prompt.format(language=state["language"], level=state["level"])),
                                             HumanMessage(content=state["report"])])

    return{"report": response.content}

def language_check(state):
    if state["language"] == "English":
        return "end"
    else:
        return "desired_language"

def build_graph():
    class SectionState(TypedDict):
        messages: Annotated[list, add_messages]
        concept:str
        sections: List
        level: str
        counter: int
        report: str
        language: str

    builder = StateGraph(SectionState)
    builder.add_node("generate_plan", generate_plan)
    builder.add_node("write_sections", write_sections)
    builder.add_node("final_draft", final_draft)
    builder.add_node("desired_language", desired_language)

    builder.add_edge(START, "generate_plan")
    builder.add_edge("generate_plan", "write_sections")
    builder.add_conditional_edges("write_sections", router, {"final_draft": "final_draft",
                                                            "write_sections": "write_sections"})
    
    builder.add_conditional_edges("final_draft", language_check, {"end": END,
                                                            "desired_language": "desired_language"})

    builder.add_edge("desired_language", END)

    return(builder.compile())
            

def run_graph(topic, level, language):
    graph=build_graph()
    stream=graph.invoke({"concept": topic, "level":level, "counter": 0, "language": language})
    return(stream) 


# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------

import streamlit as st

st.title("Curiosity AI - Democratizing Learning")
st.markdown("""
Generate a comprehensive educational article on any concept, tailored to your skill level and language.
""")
st.divider()

with st.form("input_form"):
    concept = st.text_input("What concept do you want to learn?", placeholder="e.g. Quantum Physics, How Blockchains Work...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_level = st.selectbox(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Expert"],
            index=0
        )
    
    with col2:
        user_language = st.selectbox(
            "Output Language",
            options=["English", "German", "Hindi", "Spanish", "French"],
            index=0
        )

    submitted = st.form_submit_button("Generate Article", use_container_width=True)


if submitted:
    
    try:

        with st.spinner(f"Researching and writing about **{concept}** ({user_level} level). This may take a couple of minutes..."):        
        
            result_state = run_graph(concept, user_level, user_language)
            response_text = result_state["report"]
            
        st.success("Content generated successfully!")

        st.markdown(response_text)
        
    except Exception as e:
        st.error("Sorry, an error occurred most probably due to an API limit. Please try contacting provider or try again after a day.")