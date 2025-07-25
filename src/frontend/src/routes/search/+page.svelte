<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import SearchBar from '$lib/components/SearchBar.svelte';
  import DocumentoCard from '$lib/components/DocumentoCard.svelte';
  import { documentoService, type Documento, type SearchResponse } from '$lib/services/api';
  
  let searchQuery = '';
  let isLoading = false;
  let error = '';
  let resultados: Documento[] = [];
  let total = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let useLLM = false;
  let llmResponse: any = null;
  
  // Atualiza a query com base nos parâmetros da URL
  $: {
    const urlQuery = $page.url.searchParams.get('q');
    if (urlQuery) {
      searchQuery = urlQuery;
      performSearch(searchQuery);
    }
    //} else {
     // loadDocumentos();
   // }
  }

  //onMount(() => {
    //if (!searchQuery) {
    //  loadDocumentos();
  //  }
 // });

  async function loadDocumentos(page = 1) {
    isLoading = true;
    error = '';
    
    try {
      const skip = (page - 1) * itemsPerPage;
      const response = await documentoService.listarDocumentos(skip, itemsPerPage);
      resultados = response.resultados;
      total = response.total;
      currentPage = page;
    } catch (err) {
      console.error('Erro ao carregar documentos:', err);
      error = 'Não foi possível carregar os documentos. Por favor, tente novamente.';
    } finally {
      isLoading = false;
    }
  }
  
  async function performSearch(query: string) {
    if (!query) return;
    
    isLoading = true;
    error = '';
    llmResponse = null;
    
    try {
      if (useLLM) {
        llmResponse = await documentoService.askQuestion(query);
        resultados = llmResponse.sources.map(source => ({
          arquivo: source.filename || 'Documento',
          texto: '',
          score: 0
        }));
        total = resultados.length;
      } else {
        const response = await documentoService.buscarDocumentos(query);
        resultados = response.resultados;
        total = response.total;
      }
    } catch (err) {
      console.error('Erro na busca:', err);
      error = 'Não foi possível realizar a busca. Por favor, tente novamente.';
    } finally {
      isLoading = false;
    }
  }
  
  function handleSearch(event: CustomEvent<string>) {
    const query = event.detail;
    if (query) {
      // Atualiza a URL com a query
      const url = new URL(window.location.href);
      url.searchParams.set('q', query);
      history.pushState({}, '', url);
      
      performSearch(query);
    }
  }
  
  function handlePageChange(page: number) {
    if (!searchQuery) {
      loadDocumentos(page);
    }
  }

  function limparBusca() {
    searchQuery = '';
    resultados = [];
    total = 0;
    error = '';
    llmResponse = null;
    // Remove o parâmetro da URL
    const url = new URL(window.location.href);
    url.searchParams.delete('q');
    history.pushState({}, '', url);
  }
</script>

<div class="mb-8">
  <h1 class="text-3xl font-bold mb-6">
    {searchQuery ? 'Resultados da Busca' : 'Lista de Todos os Documentos'}
  </h1>
  
  <div class="flex items-center gap-4">
    <SearchBar 
      bind:value={searchQuery} 
      placeholder={useLLM ? "Faça uma pergunta sobre algum documento..." : "Buscar em documentos..."}
      on:search={handleSearch}
    />
    <button
      class="btn btn-outline btn-md"
      on:click={() => limparBusca()}
      aria-label="Limpar busca"
      type="button"
      disabled={searchQuery.length === 0}
    >
      Limpar
    </button>
  </div>
  <div class="flex items-center gap-12">
    <label class="cursor-pointer label">
      <span class="label-text mr-3">Utilizar Assistência de IA?</span><br>
      <input
        type="checkbox"
        class="toggle toggle-primary"
        bind:checked={useLLM}
      />
    </label>
  </div>
</div>

{#if isLoading}
  <div class="flex justify-center my-12">
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>
{:else if error}
  <div class="alert alert-error shadow-lg my-6">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <span>{error}</span>
  </div>
{:else if resultados.length === 0 && searchQuery > 0}
  <div class="alert shadow-lg my-6">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info flex-shrink-0 w-6 h-6">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>
    <span>
      {searchQuery
        ? `Nenhum resultado encontrado para "${searchQuery}". Tente uma busca diferente.`
        : ''}
    </span>
  </div>
{:else}
  <div class="mb-4">
    <p class="text-sm text-gray-500">
      {searchQuery 
        ? `Encontrados ${total} resultados para "${searchQuery}"` 
        : `Mostrando ${(currentPage - 1) * itemsPerPage + 1}-${Math.min(currentPage * itemsPerPage, total)} de ${total} documentos`}
    </p>
  </div>
  
  {#if llmResponse}
    <div class="chat chat-start">
      <div class="chat-bubble chat-bubble-primary">
        <div class="prose max-w-none">
          {@html llmResponse.answer.replace(/\n/g, '<br>')}
        </div>
        {#if llmResponse.sources.length > 0}
          <div class="mt-4">
            <h3 class="font-bold">Documentos encontrados:</h3>
            <ul class="list-disc pl-5">
              {#each llmResponse.sources as source}
                <li>{source.filename || 'Documento'}</li>
              {/each}
            </ul>
          </div>
        {/if}
      </div>
    </div>
  {/if}
  
  <div class="space-y-6">
    {#each resultados as documento}
      <DocumentoCard {documento} />
    {/each}
  </div>
  
  {#if !searchQuery && total > itemsPerPage}
    <div class="flex justify-center mt-8">
      <div class="join">
        {#each Array(Math.ceil(total / itemsPerPage)) as _, i}
          <button 
            class="join-item btn {currentPage === i + 1 ? 'btn-active' : ''}"
            on:click={() => handlePageChange(i + 1)}
          >
            {i + 1}
          </button>
        {/each}
      </div>
    </div>
  {/if}
{/if}
