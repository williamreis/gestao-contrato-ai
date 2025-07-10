<script>
  // Página Sobre - Documento RAG
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
</div>
