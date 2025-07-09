import os
import time
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status
from utils.processar_contrato import processar_contrato

"""
Rota para gerenciar Upload de Contratos
"""
router = APIRouter(prefix="/storage", tags=["Upload Contratos"])

# Obtém o caminho absoluto do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Pasta para armazenar os contratos
PASTA_CONTRATOS = os.path.join(diretorio_atual, "../storage")

# Cria a pasta de contratos se não existir
if not os.path.exists(PASTA_CONTRATOS):
    os.makedirs(PASTA_CONTRATOS)


def processar_contrato_background(caminho_arquivo: str):
    """Processa um contrato em segundo plano."""
    try:
        processar_contrato(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao processar contrato em segundo plano: {e}")


@router.post("/upload")
async def upload_storage(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Faz upload de um novo contrato PDF e o processa automaticamente.
    O processamento ocorre em segundo plano para não bloquear a resposta.
    """
    # Verifica se o arquivo é um PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

    try:
        # Salva o arquivo na pasta de contratos
        caminho_destino = os.path.join(PASTA_CONTRATOS, file.filename)

        # Se o arquivo já existir, adiciona um timestamp ao nome
        if os.path.exists(caminho_destino):
            nome_base, extensao = os.path.splitext(file.filename)
            import time
            timestamp = int(time.time())
            novo_nome = f"{nome_base}_{timestamp}{extensao}"
            caminho_destino = os.path.join(PASTA_CONTRATOS, novo_nome)

        # Salva o arquivo
        with open(caminho_destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Processa o contrato em segundo plano
        background_tasks.add_task(processar_contrato_background, caminho_destino)

        return {
            "status": "success",
            "message": "Contrato enviado com sucesso e está sendo processado",
            "arquivo": os.path.basename(caminho_destino)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o upload: {str(e)}")


@router.get("/list")
async def listar_storage():
    """
    Lista todos os contratos disponíveis na pasta de contratos.
    """
    try:
        contratos = []

        # Lista todos os arquivos PDF na pasta de contratos
        for arquivo in os.listdir(PASTA_CONTRATOS):
            if arquivo.lower().endswith('.pdf'):
                caminho_completo = os.path.join(PASTA_CONTRATOS, arquivo)
                tamanho = os.path.getsize(caminho_completo)
                data_modificacao = os.path.getmtime(caminho_completo)

                data_formatada = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_modificacao))

                contratos.append({
                    "nome": arquivo,
                    "tamanho_bytes": tamanho,
                    "data_modificacao": data_formatada
                })

        return {"contratos": contratos, "total": len(contratos)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar contratos: {str(e)}")
