from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

import io
import cv2

# SETUP
# Set env variable using export OPENAI_API_KEY=<your_key>
api_key = os.environ['OPENAI_API_KEY']

# Set up the models
text_llm = OpenAI(name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
text_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a newsletter reporter. Everything you say will sound like it's meant for a newsletter. Only use the information from the video. Start by summarizing the video."),
    ("user", "{input}")
])

def generate_image(summary):
    image_url = DallEAPIWrapper().run(summary)
    return image_url

def generate_summary(youtube_url_list):
    texts = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    for url in youtube_url_list:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()

        texts.extend(text_splitter.split_documents(result))
    chain = load_summarize_chain(text_llm, chain_type="map_reduce", verbose=False)
    return chain.run(texts)

youtube_url_list = ["https://www.youtube.com/watch?v=ytdIjfGuHZQ"]
summary = generate_summary(youtube_url_list)
print("Text summary:")
print(summary)
image_url = generate_image(summary)
print("Image URL:")
print(image_url)
