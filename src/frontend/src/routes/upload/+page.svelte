<script>
  // Página Sobre - Documento AI
  let file = null;
  let uploading = false;
  let uploadSuccess = false;
  let uploadError = '';

  async function uploadFile() {
    if (!file) return;
    uploading = true;
    uploadSuccess = false;
    uploadError = '';
    const formData = new FormData();
    formData.append('file', file);
    try {
    // Usar sempre a URL completa para evitar problemas com proxy
      const UPLOAD_API_URL = 'http://localhost:8002';
      const res = await fetch(`${UPLOAD_API_URL}/storage/upload`, {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        uploadSuccess = true;
      } else {
        uploadError = 'Falha ao enviar o arquivo.';
      }
    } catch (e) {
      uploadError = 'Erro de conexão.';
    } finally {
      uploading = false;
    }
  }
</script>

<div class="prose max-w-none">
  <h1>Upload do Documento</h1>
  
  <!-- Formulário de upload -->
  <div class="card bg-base-100 shadow-xl mb-8">
    <div class="card-body">
      <h2 class="card-title">Envie seu documento</h2>
      <form on:submit|preventDefault={uploadFile} class="flex flex-col gap-4">
        <input type="file" on:change={e => file = e.target.files[0]} accept="application/pdf,.doc,.docx,.txt" class="file-input file-input-bordered w-full max-w-xs" />
        <button type="submit" class="btn btn-primary" disabled={uploading || !file}>
          {uploading ? 'Enviando...' : 'Enviar'}
        </button>
        {#if uploadSuccess}
          <div class="alert alert-success">Arquivo enviado com sucesso!</div>
        {/if}
        {#if uploadError}
          <div class="alert alert-error">{uploadError}</div>
        {/if}
      </form>
    </div>
  </div>

  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">Como Funciona</h2>
      
      <div class="steps steps-vertical lg:steps-horizontal">
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Upload</h3>
            <p class="text-sm">Os documentos são enviados e armazenados de forma segura no sistema</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Indexação</h3>
            <p class="text-sm">Geramos embeddings e índices vetoriais para habilitar a busca semântica avançada</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Consulta</h3>
            <p class="text-sm">Você realiza perguntas em linguagem natural, sem necessidade de termos técnicos</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Resultados</h3>
            <p class="text-sm">O sistema localiza e exibe as informações mais relevantes encontradas nos documentos</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
