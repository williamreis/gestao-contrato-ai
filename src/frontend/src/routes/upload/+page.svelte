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
  <h1>Sobre o Documento AI</h1>
  
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

  <div class="card bg-base-100 shadow-xl mb-8">
    <div class="card-body">
      <h2 class="card-title">Nossa Solução</h2>
      <p>
        A plataforma avançada de consulta de documentos que utiliza
        tecnologia de busca semântica para facilitar o acesso e a compreensão de documentos jurídicos.
      </p>
      <p>
        Nosso sistema permite que você encontre informações específicas em documentos usando linguagem natural,
        sem precisar conhecer os termos exatos ou navegar manualmente pelos documentos.
      </p>
    </div>
  </div>
  
  <div class="card bg-base-100 shadow-xl mb-8">
    <div class="card-body">
      <h2 class="card-title">Tecnologia</h2>
      <p>Nossa plataforma é construída com tecnologias modernas:</p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div>
          <h3 class="text-lg font-bold">Backend</h3>
          <ul>
            <li>Python com FastAPI</li>
            <li>MongoDB para armazenamento de dados</li>
            <li>Índice vetorial para busca semântica</li>
            <li>Modelo de embeddings Nomic para processamento de linguagem natural</li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-bold">Frontend</h3>
          <ul>
            <li>SvelteKit para uma interface rápida e responsiva</li>
            <li>Tailwind CSS e DaisyUI para design moderno</li>
            <li>Interface intuitiva e amigável</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">Como Funciona</h2>
      
      <div class="steps steps-vertical lg:steps-horizontal">
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Upload</h3>
            <p class="text-sm">Os documentos são processados e armazenados no sistema</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Indexação</h3>
            <p class="text-sm">Criamos embeddings e índices vetoriais para busca semântica</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Consulta</h3>
            <p class="text-sm">Você faz perguntas em linguagem natural</p>
          </div>
        </div>
        <div class="step step-primary">
          <div class="text-left ml-2">
            <h3 class="font-bold">Resultados</h3>
            <p class="text-sm">O sistema encontra as informações mais relevantes nos documentos</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
