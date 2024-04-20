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

urls = {"Tech": ["https://www.youtube.com/watch?v=vQChW_jgMMM&pp=ygUEdGVjaA%3D%3D",
                 "https://www.youtube.com/watch?v=vyQv563Y-fk&pp=ygUKdGVjaG5vbG9neQ%3D%3D",
                 "https://www.youtube.com/watch?v=PtVOpxeqTkA",
                 "https://www.youtube.com/watch?v=Ay1yDyc8Rok",
                 "https://www.youtube.com/watch?v=SjfW3rmlDEw"
                 ],
        "AI": [
            "https://www.youtube.com/watch?v=vQChW_jgMMM&pp=ygUEdGVjaA%3D%3D",
            "https://www.youtube.com/watch?v=OTYP896o9m0",
            "https://www.youtube.com/watch?v=cEHFzvU-pzk",
            "https://www.youtube.com/watch?v=5aOkIauvsow",
            "https://www.youtube.com/watch?v=8B68a936GBg"
        ],
        "Politics": [
            "https://www.youtube.com/watch?v=qaMySmraCOk",
            "https://www.youtube.com/watch?v=q5wyOIzGuuc",
            "https://www.youtube.com/watch?v=q9nJPImwE9g&list=RDNSq9nJPImwE9g&start_radio=1",
            "https://www.youtube.com/watch?v=hswXYD8lZxM",
            "https://www.youtube.com/watch?v=uN1Tss13gzc&list=RDNSuN1Tss13gzc&start_radio=1"
        ]}
youtube_url_list = []


def generate_image(topic):
    image_url = DallEAPIWrapper().run("Generate an image for the topic: " + topic)
    return image_url

def generate_summary(topics):
    for topic in topics:
        print(urls.get(topic))
    for url in urls.get(topic):
        youtube_url_list.append(url)
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