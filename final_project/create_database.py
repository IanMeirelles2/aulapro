from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os

langchain_tracing = os.getenv('LANGCHAIN_TRACING_V2')
langchain_key = os.getenv('LANGCHAIN_KEY')
openai_key = os.getenv('OPENAI_KEY')


DATA_PATH = 'data'
CHROMA_PATH = 'chroma'


def main():
    documents = load_documents()
    chunks = split_text(documents)
    save_chroma(chunks)

def load_documents():
    #carregando os documentos, somente aqueles que sao markdown
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    #criando chunks de 1000 caracteres com overlap de 500, dividindo meus textos em pedaços menores
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        lenght_funciton=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    return chuncks

def save_chroma(chunks: list[Document]):
    #exclíndo o bd antigo com o mesmo nome (CHROMA_PATH)
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    #criando um novo bd
    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(),
        persist_directory = CHROMA_PATH
    )
    db.persist()

if __name__ == '__main__':
    main() 
