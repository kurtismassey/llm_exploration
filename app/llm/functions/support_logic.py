from pydantic import BaseModel, Field
from openai import OpenAI

class SupportAgent():
    """
    Support Agent
    """
    def __init__(self):
        self.issues = ['Password Reset', 'Account Unlock']
        self.llm = OpenAI()
        # To do implement Support Agent history
        self.history = []

    def query(self, prompt, query):
        completion = self.llm.chat.completions.create(
            messages=[
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

        self.add_history(
            query=query,
            response=response
            )

        return response

    def add_issue(self, issue):
        self.issues.append(issue)

    def add_history(self, query, response):
        self.history.append({
                "role": "user",
                "content": query
            })
        self.history.append({
                "role": "agent",
                "content": response
            })
    
    def password_reset(self, query):
        while True:
            password_reset_prompt = PASSWORD_RESET_PROMPT.format(model=ResetModel)
            response = self.query(
                prompt=password_reset_prompt, 
                query=query
                )
            print(f"SUPPORT BOT: {response}")
            
            query = input(f"USER: ")
            response = self.query(
                prompt=password_reset_prompt, 
                query=query
                )
            print(f"SUPPORT BOT: {response}")

PASSWORD_RESET_PROMPT = """
You are an expert support agent, your job is soley focused on resets. Get the relevant informationo
from the user to structure a JSON object with the structure of the below data model enclosed in the <MODEL> tags:

<MODEL>
{model}
</MODEL>
"""

class ResetModel(BaseModel):
    user_email: str = Field(description="Email address that requires reset")
    domain: str = Field(description="Domain name extracted from email address")