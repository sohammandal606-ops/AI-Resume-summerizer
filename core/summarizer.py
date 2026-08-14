from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os
import time


def get_llm():
    return ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
        max_retries=5,
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
    )
    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    llm = get_llm()
    chunks = split_transcript(transcript)

    if len(chunks) == 1:
        direct_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert meeting summarizer. Generate a professional, comprehensive "
                "meeting summary in organized bullet points.",
            ),
            ("human", "{text}"),
        ])
        chain = direct_prompt | llm | StrOutputParser()
        return chain.invoke({"text": chunks[0]})

    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a meeting transcript concisely."),
        ("human", "{text}"),
    ])
    map_chain = map_prompt | llm | StrOutputParser()

    chunk_summaries = []
    for chunk in chunks:
        chunk_summaries.append(map_chain.invoke({"text": chunk}))
        time.sleep(1.0)  # Gentle rate-limit pause between chunks

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",
        ),
        ("human", "{text}"),
    ])

    time.sleep(1.0)
    combined_chain = combined_prompt | llm | StrOutputParser()
    return combined_chain.invoke({"text": combined})

def generate_title(transcipt : str) -> str:
    llm = get_llm()

    

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    return title_chain.invoke(transcipt[:2000])