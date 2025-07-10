import os
import time
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status
from utils.processing_document import processing_document

"""
Rota para gerenciar Upload de Documentos
"""
router = APIRouter(prefix="/storage", tags=["Upload Documentos"])

# Obtém o caminho absoluto do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Pasta para armazenar os documentos
PASTA_DOCUMENTOS = os.path.join(diretorio_atual, "../storage")

# Cria a pasta de documentos se não existir
if not os.path.exists(PASTA_DOCUMENTOS):
    os.makedirs(PASTA_DOCUMENTOS)


def processing_document_background(caminho_arquivo: str):
    """Processa um documento em segundo plano."""
    try:
        processing_document(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao processar documento em segundo plano: {e}")


@router.post("/upload")
async def upload_storage(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Faz upload de um novo documento PDF e o processa automaticamente.
    O processamento ocorre em segundo plano para não bloquear a resposta.
    """
    # Verifica se o arquivo é um PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

    try:
        # Salva o arquivo na pasta de documentos
        caminho_destino = os.path.join(PASTA_DOCUMENTOS, file.filename)

        # Se o arquivo já existir, adiciona um timestamp ao nome
        if os.path.exists(caminho_destino):
            nome_base, extensao = os.path.splitext(file.filename)
            import time
            timestamp = int(time.time())
            novo_nome = f"{nome_base}_{timestamp}{extensao}"
            caminho_destino = os.path.join(PASTA_DOCUMENTOS, novo_nome)

        # Salva o arquivo
        with open(caminho_destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Processa o documento em segundo plano
        background_tasks.add_task(processing_document_background, caminho_destino)

        return {
            "status": "success",
            "message": "Documento enviado com sucesso e está sendo processado",
            "arquivo": os.path.basename(caminho_destino)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o upload: {str(e)}")


@router.get("/list")
async def list_storage():
    """
    Lista todos os documentos disponíveis na pasta de documentos.
    """
    try:
        documentos = []

        # Lista todos os arquivos PDF na pasta de documentos
        for arquivo in os.listdir(PASTA_DOCUMENTOS):
            if arquivo.lower().endswith('.pdf'):
                caminho_completo = os.path.join(PASTA_DOCUMENTOS, arquivo)
                tamanho = os.path.getsize(caminho_completo)
                data_modificacao = os.path.getmtime(caminho_completo)

                data_formatada = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_modificacao))

                documentos.append({
                    "nome": arquivo,
                    "tamanho_bytes": tamanho,
                    "data_modificacao": data_formatada
                })

        return {"documentos": documentos, "total": len(documentos)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar documentos: {str(e)}")
