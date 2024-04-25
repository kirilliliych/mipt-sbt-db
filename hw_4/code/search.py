import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_wcs(
    cluster_url="https://mipt-sbt-db-5bhod7yu.weaviate.network",
    auth_credentials=weaviate.auth.AuthApiKey("gJ0sD5gCiFyPKTUdCjPmkS2984c6ZKrbWFI9"),
    headers={
        "X-OpenAI-Api-Key": "sk-proj-pWYMnmCAq3dWzm8PddM8T3BlbkFJ0NDY1ucxbbSo3XZZBGVt"
    }
)

try:
    # semantic search for vector which are most similar to that of "biology"
    questions = client.collections.get("Question")
    response = questions.query.near_text(
        query="biology",
        limit=2
    )
    print(response.objects[0].properties) # getting only first object

    # the same semantic search, but bounded to ANIMALS category
    response = questions.query.near_text(
        query="biology",
        limit=2,
        filters=wvc.query.Filter.by_property("category").equal("ANIMALS")
    )
    print(response.objects[0].properties)

    # generative search (single prompt), using query results to perform task that is based on our prompt
    response = questions.generate.near_text(
        query="biology",
        limit=2,
        single_prompt="Explain {answer} as you might to a five-year-old."
    )
    print(response.objects[0].generated)

    # generative search (group prompt), search results are combined and sent to LLM with a prompt
    response = questions.generate.near_text(
        query="Cute animals",
        limit=3,
        grouped_task="What do these animals have in common, if anything?"
    )
    print(response.generated)

finally:
    client.close()  # closing client