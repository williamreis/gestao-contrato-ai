#  Gestão de Documento com RAG

Modelo de sistema para processamento e consulta semântica de documentos, baseado em IA generativa. Desenvolvido com Python, LangChain, Pinecone e SvelteKit, integra o MCP (Model Context Protocol) e utiliza técnicas de embeddings e RAG (Retrieval-Augmented Generation) para permitir buscas contextuais e perguntas em linguagem natural.

> **Atenção:** O objetivo deste projeto é apoiar estudos sobre IA generativa e a aplicação de RAG em sistemas de recuperação de informação. Sinta-se à vontade para explorar, adaptar e evoluir o código. Espero que seja útil nos seus aprendizados!

## Requisitos

- Conta no Pinecone (https://www.pinecone.io/)
- Chave de API da OpenAI (https://platform.openai.com/)


## Configuração do .env

Antes de executar o projeto, é necessário configurar as variáveis de ambiente. Um arquivo de exemplo chamado `.env-sample` está disponível no repositório.

Renomeie o arquivo `.env-sample` para `.env` e preencha com suas credenciais:

```bash
cp .env-sample .env
```

Edite o arquivo `.env` conforme necessário para incluir suas chaves da OpenAI, Pinecone, etc.

```dotenv
# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Pinecone
PINECONE_API_KEY=
PINECONE_HOST=
PINECONE_INDEX_NAME=documento-rag

```

## Executando com Docker Compose

Para facilitar a execução do projeto, você pode utilizar o Docker Compose. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

```bash
docker-compose up -d --build
```

Isso irá construir e iniciar todos os serviços necessários (backend e frontend) definidos no arquivo `docker-compose.yml`.

- Acesse o frontend em: http://localhost:3000
- Acesse a API backend em: http://localhost:8002
- URL do servidor MCP: http://localhost:8002/mcp

## Conectando com Model Context Protocol (MCP)

Para integrar o cliente com o Model Context Protocol (MCP), você deve configurar em seu cliente a URL do servidor MCP:

```bash
{
  "mcpServers": {
    "documento-rag-mcp": {
      "url": "http://localhost:8002/mcp"
    }
  }
}
```

> **Obs:** O MCP permite que você interaja com o sistema de forma padronizada, facilitando a consulta e o processamento de documentos.
## Tecnologias

- **Backend**:
  - Python
  - FastAPI
  - FastAPI-MCP
  - Uvicorn (servidor ASGI)
  - Pinecone (banco de dados vetorial)
  - OpenAI Embeddings (modelo text-embedding-3-small)
  - OpenAI Chat Completions (modelo gpt-4o-mini padrão)
  - LangChain (processamento de documentos)
  
- **Frontend**:
  - SvelteKit
  - Tailwind CSS
  - DaisyUI

## Estrutura do Projeto

```
├── docker-compose.yml           # Orquestração dos serviços backend e frontend
├── LICENSE                      # Licença do projeto
├── README.md                    # Documentação principal
├── src/
│   ├── backend/
│   │   ├── Dockerfile           # Dockerfile do backend
│   │   ├── main.py              # Ponto de entrada do backend FastAPI
│   │   ├── requirements.txt     # Dependências Python
│   │   ├── routes/              # Rotas da API (document, llm, storage, upload)
│   │   ├── schemas/             # Schemas Pydantic para validação
│   │   ├── storage/             # Contratos PDF armazenados
│   │   └── utils/               # Utilitários (ex: processing_document.py, pinecone.py)
│   └── frontend/
│       ├── Dockerfile           # Dockerfile do frontend
│       ├── package.json         # Dependências do frontend
│       ├── svelte.config.js     # Configuração do SvelteKit
│       ├── tailwind.config.js   # Configuração do Tailwind CSS
│       ├── src/                 # Código-fonte do frontend
```

## Documentação das APIs

**Base URL**: http://localhost:8002

**Porta**: 8002

| Endpoint                  | Método  | Descrição                                                        | Parâmetros                                                                                  |
|---------------------------|---------|------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `/docs`                   | GET     | Swagger                                                          | Documentação da API                                                                         | - |
| `/health`                 | GET     | Verifica o status da API e a conexão com o Pinecone              | -                                                                                           |
| `/document/list`          | GET     | Lista todos os documentos disponíveis                            | `skip`: número de registros para pular<br>`limit`: número máximo de registros para retornar |
| `/document/search`        | GET     | Realiza uma busca semântica nos documentos                       | `q`: consulta para busca<br>`limit`: número máximo de resultados                            |
| `/document/files`         | GET     | Lista todos os nomes de arquivos únicos no índice                | -                                                                                           |
| `/document/delete/{filename}` | DELETE  | Remove o registro do documento do Pinecone e deleta o arquivo    | `filename`: nome do arquivo                                                                 |
| `/llm/ask`                | POST    | Responde a perguntas sobre documentos usando o LLM              | Body JSON: `{"question": "string", "max_results": int}`                                     |
| `/storage/list`           | GET     | Lista todos os documentos disponíveis na pasta de documentos     | -                                                                                           |
| `/storage/upload`         | POST    | Faz upload de um novo documento PDF e o processa automaticamente | Form Data: `filename`: arquivo PDF                                                          |
| `/storage/download/{filename}`       | GET     | Permitir o download do arquivo armazenado                        | -                                                                                           |


> **Licença:** Este projeto está licenciado sob a [Licença MIT](LICENSE). Você pode usar, modificar e distribuir este código livremente, inclusive para fins pessoais e comerciais, desde que mantenha a atribuição de autoria original.
> Autoria: William Reis
