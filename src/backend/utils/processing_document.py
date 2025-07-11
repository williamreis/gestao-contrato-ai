import os
import sys
import time
import hashlib
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Obtém o caminho absoluto do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Carrega as variáveis de ambiente do arquivo .env no diretório atual
env_path = os.path.join(diretorio_atual, '.env')
load_dotenv(dotenv_path=env_path)

# Configurações do Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "documento-rag")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

# Verifica se as chaves estão configuradas
if not PINECONE_API_KEY:
    print("ERRO: PINECONE_API_KEY não encontrada no arquivo .env")
    sys.exit(1)

if not PINECONE_HOST:
    print("ERRO: PINECONE_HOST não encontrado no arquivo .env")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("ERRO: OPENAI_API_KEY não encontrada no arquivo .env")
    sys.exit(1)


def gerar_embedding(texto):
    """Gera um embedding usando o modelo da OpenAI."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            input=texto,
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        raise


def init_pinecone():
    """Inicializa a conexão com o Pinecone e retorna o índice."""
    try:
        # Inicializa o cliente Pinecone com a API V2
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Conecta ao índice com o host específico
        index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)

        # Verifica se o índice está acessível obtendo suas estatísticas
        stats = index.describe_index_stats()
        print(f"Conexão com o índice '{PINECONE_INDEX_NAME}' estabelecida com sucesso!")
        print(f"Total de vetores no índice: {stats.get('total_vector_count', 0)}")

        return index

    except Exception as e:
        print(f"Erro ao inicializar Pinecone: {e}")
        sys.exit(1)


def processing_document(caminho_pdf):
    """
    Processa um único documento PDF e o indexa no Pinecone.
    
    Args:
        caminho_pdf: Caminho completo para o arquivo PDF
        
    Returns:
        int: Número de chunks processados
    """
    if not os.path.exists(caminho_pdf):
        print(f"ERRO: Arquivo {caminho_pdf} não encontrado!")
        return 0

    if not caminho_pdf.lower().endswith('.pdf'):
        print(f"ERRO: Arquivo {caminho_pdf} não é um PDF!")
        return 0

    nome_arquivo = os.path.basename(caminho_pdf)
    print(f"Processando documento: {nome_arquivo}")

    # Inicializa o Pinecone
    index = init_pinecone()

    try:
        # Carrega o PDF
        loader = PyPDFLoader(caminho_pdf)
        dados = loader.load()

        # Separadores mais abrangentes para diferentes tipos de documentos
        separators = [
            "\n\n", "\n",
            "CLÁUSULA", "Cláusula",
            "ARTIGO", "Artigo",
            "SEÇÃO", "Seção",
            "TÍTULO", "Título",
            ". ", " ", ""
        ]

        # Divide em chunks de forma mais inteligente usando separadores específicos para documentos
        splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=500,  # Chunks um pouco maiores para capturar mais contexto
            chunk_overlap=50  # Maior sobreposição para manter a coerência entre chunks
        )
        documentos = splitter.split_documents(dados)

        print(f"Documento dividido em {len(documentos)} chunks usando chunking semântico")

        # Identificação inteligente de seções para diversos tipos de documentos
        def identificar_secao(texto):
            texto_lower = texto.lower()

            if any(term in texto_lower for term in
                   ["locador", "proprietário", "senhorio", "contratante", "empregador"]):
                return "Parte Contratante / Responsável"
            elif any(term in texto_lower for term in
                     ["locatário", "inquilino", "arrendatário", "contratado", "empregado"]):
                return "Parte Contratada / Envolvido"
            elif any(term in texto_lower for term in
                     ["objeto", "finalidade", "escopo", "atribuições", "descrição do serviço"]):
                return "Objeto / Finalidade do Documento"
            elif any(term in texto_lower for term in
                     ["valor", "pagamento", "preço", "remuneração", "salário", "indenização"]):
                return "Condições Financeiras / Pagamento"
            elif any(term in texto_lower for term in ["prazo", "vigência", "duração", "início", "término", "validade"]):
                return "Prazos e Vigência"
            elif any(term in texto_lower for term in ["rescisão", "multa", "penalidade", "quebra", "sanção"]):
                return "Rescisão / Penalidades"
            elif any(term in texto_lower for term in ["garantia", "seguro", "caução", "responsabilidade", "fiador"]):
                return "Garantias / Responsabilidades"
            elif any(term in texto_lower for term in ["confidencialidade", "sigilo", "proteção de dados", "lgpd"]):
                return "Confidencialidade e Proteção de Dados"
            elif any(term in texto_lower for term in ["foro", "jurisdição", "legislação aplicável", "competência"]):
                return "Disposições Legais"
            elif any(term in texto_lower for term in ["assinatura", "aceite", "validade legal"]):
                return "Assinaturas / Formalização"
            else:
                return "Outras Disposições"

        def identificar_tipo_documento(texto):
            texto_lower = texto.lower()

            if any(term in texto_lower for term in ["cláusula", "contratante", "contratado", "rescisão", "vigência"]):
                return "contrato"
            elif any(term in texto_lower for term in ["norma", "conduta", "política interna", "compliance"]):
                return "política"
            elif any(term in texto_lower for term in ["artigo", "inciso", "capítulo", "regulamento", "regra geral"]):
                return "regulamento"
            elif any(term in texto_lower for term in ["laudo", "perícia", "análise técnica", "conclusão pericial"]):
                return "laudo"
            elif any(term in texto_lower for term in
                     ["fatura", "boleto", "demonstrativo", "valor total", "pagamento referente"]):
                return "financeiro"
            elif any(term in texto_lower for term in
                     ["colaborador", "funcionário", "salário", "departamento pessoal", "rh"]):
                return "rh"
            elif any(term in texto_lower for term in
                     ["procuração", "certidão", "petição", "jurídico", "advogado", "ação judicial"]):
                return "documento jurídico"
            elif any(term in texto_lower for term in
                     ["currículo", "experiência profissional", "formação acadêmica", "objetivo profissional"]):
                return "currículo"
            elif any(term in texto_lower for term in
                     ["resumo", "abstract", "introdução", "metodologia", "referências", "revisão de literatura",
                      "doi"]):
                return "artigo científico"
            elif any(term in texto_lower for term in
                     ["revista", "edição", "editorial", "coluna", "publicação periódica"]):
                return "revista"
            elif any(term in texto_lower for term in ["jornal", "notícia", "reportagem", "colunista", "imprensa"]):
                return "jornal"
            else:
                return "desconhecido"

        # Processa cada chunk
        for i, doc in enumerate(documentos):
            texto = doc.page_content

            # Gera um hash para o conteúdo do chunk (útil para evitar duplicatas ou identificar conteúdo)
            chunk_hash = hashlib.md5(texto.encode("utf-8")).hexdigest()

            # Metadados enriquecidos
            metadata = {
                "arquivo": nome_arquivo,  # Nome original do arquivo
                "texto": texto,  # Conteúdo do chunk
                "pagina": doc.metadata.get("page", 0),  # Página original, se disponível
                "secao": identificar_secao(texto),  # Classificação semântica da seção
                "tamanho_chunk": len(texto),  # Número de caracteres no chunk
                "posicao": i,  # Posição sequencial do chunk no documento
                "total_chunks": len(documentos),  # Total de chunks do documento
                "data_processamento": time.strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
                "id_chunk": f"{nome_arquivo}_{i}",  # ID único do chunk
                "hash_conteudo": chunk_hash,  # Hash MD5 do texto para controle e rastreabilidade
                "tipo_documento": identificar_tipo_documento(texto),  # Ex: contrato, política etc.
                "origem": doc.metadata.get("origem", "upload_usuario"),  # Ex: upload, API, integração externa
            }

            # Gera um ID único
            id = f"{nome_arquivo.replace('.pdf', '')}_{i}"

            # Gera o embedding
            embedding = gerar_embedding(texto)

            # Upsert no Pinecone
            index.upsert(vectors=[(id, embedding, metadata)])

            print(f"  Chunk {i + 1}/{len(documentos)} processado")

        print(f"Documento {nome_arquivo} processado com sucesso!")
        return len(documentos)

    except Exception as e:
        print(f"ERRO ao processar documento {nome_arquivo}: {e}")
        return 0


def processar_pasta_documentos(pasta="../storage"):
    """
    Processa todos os PDFs na pasta de documentos.
    
    Args:
        pasta: Caminho para a pasta de documentos
        
    Returns:
        int: Número total de documentos processados
    """
    if not os.path.exists(pasta):
        print(f"ERRO: Pasta {pasta} não encontrada!")
        return 0

    print(f"Processando documentos da pasta: {pasta}")

    total_documentos = 0
    total_chunks = 0

    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.lower().endswith('.pdf'):
            caminho_completo = os.path.join(pasta, nome_arquivo)
            chunks = processing_document(caminho_completo)

            if chunks > 0:
                total_documentos += 1
                total_chunks += chunks

    print(f"\nProcessamento concluído!")
    print(f"Total de documentos processados: {total_documentos}")
    print(f"Total de chunks indexados: {total_chunks}")

    return total_documentos


if __name__ == "__main__":
    # Se um arquivo específico foi fornecido como argumento
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
        processing_document(caminho_arquivo)
    else:
        # Processa todos os documentos na pasta
        processar_pasta_documentos()
