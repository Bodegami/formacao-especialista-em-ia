from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import Field, BaseModel
from dotenv import load_dotenv
from langchain.globals import set_debug
import os

set_debug(True)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class Destino(BaseModel):
    cidade: str = Field("A cidade recomendada para visitar")
    motivo: str = Field("O motivo pelo qual é interessante visitar essa cidade")

class Restaurantes(BaseModel):
    cidade: str = Field("A cidade recomendada para visitar")
    restaurantes: str = Field("Restaurantes recomendados na cidade")

parseador_destino = JsonOutputParser(pydantic_object=Destino)    
parseador_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

prompt_cidade = PromptTemplate(
    template="""
    Sugira uma cidade dado o meu interesse por {interesse}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
)

modelo = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=api_key,
    temperature=0.5
)

prompt_restaurantes = PromptTemplate(
    template="""
    Sugira restaurantes na cidade {cidade}.
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_restaurantes.get_format_instructions()}
)

prompt_cultura = PromptTemplate(
    template="Sugira atividades culturais na cidade {cidade}.",
)

cadeia_destino = prompt_cidade | modelo | parseador_destino
cadeia_restaurantes = prompt_restaurantes | modelo | parseador_restaurantes
cadeia_cultura = prompt_cultura | modelo | StrOutputParser()

cadeia = (cadeia_destino | cadeia_restaurantes | cadeia_cultura)

resposta = cadeia.invoke({"interesse": "praias"})
print(resposta)