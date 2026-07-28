import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama-3.1-8b-instant")

prompt_template = 'Generate 5 interesting facts about {topic}'
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=['topic']
)

parser = StrOutputParser()

# Simple Sequential Chain
chain = prompt | model | parser

user_input = input()
print(prompt)
result = chain.invoke({"topic": user_input})

print(result)

chain.get_graph().print_ascii()
