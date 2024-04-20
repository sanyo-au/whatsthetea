from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key = os.environ['OPENAI_API_KEY']
llm = OpenAI(temperature=0, openai_api_key=api_key)

youtube_url_list = ["https://www.youtube.com/watch?v=AXq0QHUwmh8", "https://www.youtube.com/watch?v=EwHrjZxAT7g"]

texts = []

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

for url in youtube_url_list:
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    result = loader.load()

    texts.extend(text_splitter.split_documents(result))
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)
print(chain.run(texts))