from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# SETUP
# Set env variable using export OPENAI_API_KEY=<your_key>
api_key = os.environ['OPENAI_API_KEY']

# Set up the models
text_llm = OpenAI(name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
text_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a newsletter reporter. Everything you say will sound like it's meant for a newsletter. Only use the information from the video. Start by summarizing the video."),
    ("user", "{input}")
])

def generate_image(topic):
    image_url = DallEAPIWrapper().run("Generate an image for the topic: " + topic)
    return image_url

def generate_summary(youtube_url_list):
    texts = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    for url in youtube_url_list:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()
        # print(result)

        texts.extend(text_splitter.split_documents(result))
    chain = load_summarize_chain(text_llm, chain_type="map_reduce")
    summary = chain.run(texts)

    chain = text_prompt | text_llm
    newsletter_content = chain.invoke({"input": "You are a newsletter reporter. Everything you say will sound like it's meant for a newsletter. Now change the following content to sound like a newsletter." + summary})
    topic = chain.invoke({"input": "Give me a one or two word title for the following content: " + summary})
    return newsletter_content, topic

youtube_url_list = ["https://www.youtube.com/watch?v=ytdIjfGuHZQ"]
summary, topic = generate_summary(youtube_url_list)
print("Text summary:")
print(topic)
print(summary)
image_url = generate_image(topic)
print("Image URL:")
print(image_url)
