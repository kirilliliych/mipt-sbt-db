import weaviate
import weaviate.classes as wvc
import os
import requests
import json

client = weaviate.connect_to_wcs(
    cluster_url="https://mipt-sbt-db-5bhod7yu.weaviate.network",
    auth_credentials=weaviate.auth.AuthApiKey("gJ0sD5gCiFyPKTUdCjPmkS2984c6ZKrbWFI9"),
    headers={
        "X-OpenAI-Api-Key": "sk-proj-pWYMnmCAq3dWzm8PddM8T3BlbkFJ0NDY1ucxbbSo3XZZBGVt"
    }
)

try:
    # creating collection "Question"
    questions = client.collections.create(
        name="Question",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.config.Configure.Generative.openai()
    )

    # importing data
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # loading data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)


finally:
    client.close()  # closing client