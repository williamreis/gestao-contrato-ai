import os
import time
from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from schemas.llm import QuestionRequest, QuestionResponse
from utils.pinecone import search_documents

# Env
OPENAI_MODELO = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente Langchain
llm = ChatOpenAI(model_name=OPENAI_MODELO, api_key=OPENAI_API_KEY, temperature=0.0)

# Prompt com instruções especializadas
prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Você é um assistente especializado na análise e interpretação de documentos diversos, como contratos, políticas, laudos, regulamentos, documentos jurídicos, financeiros, de recursos humanos (RH) e muitos outros. Seu papel é fornecer respostas baseadas nas informações presentes na base documental à qual você tem acesso.
        
        Suas respostas devem ser:
        1. DETALHADAS – Forneça informações completas e abrangentes sobre o que foi perguntado, sem omitir aspectos relevantes.
        2. ESPECÍFICAS – Quando a pergunta envolver pessoas, entidades, cláusulas, valores, prazos ou obrigações, inclua TODOS os detalhes disponíveis nos documentos.
        3. ESTRUTURADAS – Organize a resposta de forma clara e lógica, utilizando listas, seções ou subtópicos quando necessário para facilitar a compreensão.
        4. BASEADAS EM EVIDÊNCIAS – Sempre que possível, cite explicitamente de qual documento a informação foi extraída, mencionando o título, seção, número da cláusula ou outro identificador relevante.
        5. PRECISAS EM DADOS DE COBRANÇA – Caso a pergunta envolva boletos de cobrança, destaque claramente o código de barras e demais informações financeiras pertinentes.
        
        {history}
        Usuário: {input}
        Assistente:
        """
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

session_histories: dict[str, ChatMessageHistory] = {}

def get_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

# Combinação do prompt e modelo
runnable = prompt | llm

# Adiciona memória com histórico
chain = RunnableWithMessageHistory(
    runnable=runnable,
    get_session_history=get_history,
    input_messages_key="input",
    history_messages_key="history"
)

"""
Rota para gerenciar LLM
"""
router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/ask", response_model=QuestionResponse, operation_id='ask_question')
async def ask_question(request: QuestionRequest):
    start = time.time()

    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia")

        print(f"[LLM] Recebida pergunta: '{request.question}' (max_results={request.max_results})")

        # Busca no Pinecone
        print(f"[LLM] Realizando busca semântica...")
        documentos = search_documents(request.question, request.max_results)

        if not documentos:
            raise HTTPException(status_code=404, detail="Nenhum documento relevante encontrado.")

        print(f"[LLM] Encontrados {len(documentos)} documentos.")

        # Monta o contexto
        context = "\n\n".join(
            f"[Documento {i + 1} – {doc['arquivo']}]\n{doc['texto']}"
            for i, doc in enumerate(documentos)
        )

        session_id = "user_session_local"
        payload = {"input": f"Documentos:\n{context}\n\nPergunta: {request.question}"}
        config = {"configurable": {"session_id": session_id}}

        result = await chain.ainvoke(payload, config=config)
        answer = result.content if hasattr(result, "content") else str(result)

        elapsed = time.time() - start
        print(f"[LLM] Respondido em {elapsed:.2f}s (session={session_id})")

        return QuestionResponse(
            answer=answer,
            sources=[{"filename": d["arquivo"], "text": d["texto"]} for d in documentos]
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[LLM] Erro ao processar pergunta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {str(e)}")
