from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from openai import OpenAI
from llm.functions.support_logic import SupportAgent

def init_app():
    """
    This function initalises the Llm and Router classes and returns them when called
    """
    load_dotenv()

    router = Router()
    llm = Llm()
    
    return llm, router

class Llm():
    """
    This class initalises the OpenAI api and provides a method to query the api
    """
    def __init__(self):
        self.llm = OpenAI()
        self.history = []

    def store_history(self, query, response):
        self.history.append({
            "role": "user",
            "content": query
        })
        self.history.append({
            "role": "agent",
            "content": response
        })

    def show_history(self):
        print(self.history.items())

    def query(self, prompt, query):
        completion = self.llm.chat.completions.create(
            messages=[
                self.history.items(),
                {
                    "role": "system",
                    "content": prompt
                },
                {
                "role": "user",
                "content": query
                }
            ],
            model="gpt-3.5-turbo"
        )

        response = completion.choices[0].message.content

        self.store_history(
            query=query, 
            response=response
            )

        return response
    
class Router:
    """
    This class initalises a semantic router, allowing to easily
    > add a route
    > identify the route a query matches
    """
    def __init__(self):
        self.routes = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_route(self, route, examples):
        """
        This method adds a route and embeddings of its examples to the router
        """
        embeddings = []
        for example in examples:
            example_embedding = self.model.encode(example)
            embeddings.append(example_embedding)
        route_with_embeddings = { route : embeddings }
        self.routes.append(route_with_embeddings)

    def identify_route(self, query):
        """
        This method identifies the route a query matches if there is over 80% similarity
        """
        query_embedding = self.model.encode(query)
        route_match = []
        for route in self.routes:
            for route_name, embeddings in route.items():
                similarities = cosine_similarity([query_embedding], embeddings)
                average_similarities = round(np.mean(similarities) * 100, 0)
                route_match.append({ route_name : average_similarities })
        for route in route_match:
            for route, similarity in route.items():
                if similarity > 80:
                    return route

class style:
    BOLD = '\033[1m'
    END = '\033[0m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    RED = '\033[31m'
