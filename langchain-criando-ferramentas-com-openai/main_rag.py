from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

modelo = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=api_key
)

embeddings = OpenAIEmbeddings()
documento = TextLoader(
    "documentos/GTB_gold_Nov23.txt",
    encoding="utf-8"
).load()

chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
).split_documents(documento)

dados_recuperados = FAISS.from_documents(
    chunks, embeddings
).as_retriever(search_kwargs={"k": 2})

prompt_consulta_seguro = ChatPromptTemplate.from_messages([
    ("system", "Responda usando exclusivamente o conteúdo do documento fornecido."),
    ("human", "{query}\n\nContexto: \n{contexto}\n\nResposta:")
])

cadeia = prompt_consulta_seguro | modelo | StrOutputParser()

def responder(pergunta: str):
    trechos = dados_recuperados.invoke(pergunta) # recupera os trechos mais relevantes do documento com base na pergunta
    contexto = "\n\n".join([trecho.page_content for trecho in trechos]) # junta os trechos recuperados em uma única string
    resposta = cadeia.invoke({"query": pergunta, "contexto": contexto}) # gera a resposta usando o modelo e o contexto recuperado
    return resposta

print(responder("Como devo proceder caso tenha um item roubado?")) # exemplo de pergunta