🧠 Configuração do Pinecone (Índice Vetorial)
Antes de utilizar a busca semântica, é necessário criar um índice vetorial no Pinecone:

## Criando conta no Pinecone
Acesse https://app.pinecone.io e crie uma conta.

### Configuração do Pinecone
Copie sua API Key e Environment nas configurações do projeto.


## Crie um índice no Pinecone:

Acesse o painel do Pinecone e clique em "Create Index".

### Crie um índice com as seguintes configurações:

Nome: documento-rag (ou outro nome que preferir)
Dimension: 1536 (para embeddings da OpenAI)
Metric: cosine
Cloud: aws ou gcp
Region: us-east-1 ou similar