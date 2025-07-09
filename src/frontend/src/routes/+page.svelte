<script lang="ts">
  import SearchBar from '$lib/components/SearchBar.svelte';
  import { goto } from '$app/navigation';
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';
  
  let searchQuery = '';
  let isVisible = false;
  
  onMount(() => {
    // Pequeno atraso para a animação de entrada
    setTimeout(() => {
      isVisible = true;
    }, 100);
  });
  
  function handleSearch(event: CustomEvent<string>) {
    const query = event.detail;
    if (query) {
      goto(`/documentos?q=${encodeURIComponent(query)}`);
    }
  }
</script>

<div class="min-h-[85vh] py-12 px-4">
  {#if isVisible}
    <div class="max-w-9xl mx-auto" in:fade={{ duration: 800, delay: 200 }}>
      <!-- Hero Section com Gradiente Animado -->
      <div class="hero rounded-2xl overflow-hidden bg-gradient-to-br from-primary/5 to-secondary/5 backdrop-blur-sm shadow-lg mb-16">
        <div class="hero-content flex-col lg:flex-row py-12 px-8">
          <!-- Texto Principal -->
          <div class="lg:w-2/2 text-center lg:text-left" in:fly={{ y: 20, duration: 800, delay: 300 }}>
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">
              <span class="text-primary">Gestão de Documento Inteligente</span>
            </h1>
            <p class="text-lg opacity-90 mb-8 leading-relaxed">
              Explore documentos de forma inteligente com busca semântica avançada. Encontre cláusulas, termos, informações relevantes ou respostas para perguntas em linguagem natural — seja em contratos, políticas, laudos, regulamentos, documentos jurídicos, financeiros, de RH e muito mais.
            </p>
            
            <!-- Barra de Pesquisa -->
            <div class="w-full max-w-x10 mx-auto lg:mx-0">
              <SearchBar 
                bind:value={searchQuery} 
                placeholder="Ex: Qual é o documento que trata do seguinte assunto e quais cláusulas contratuais estão relacionadas a ele?"
                on:search={handleSearch}
              />
            </div>
          </div>
          

        </div>
      </div>
      
      <!-- Features Cards -->
      <h2 class="text-2xl font-bold text-center mb-8" in:fade={{ duration: 800, delay: 600 }}>Recursos Poderosos</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8" in:fade={{ duration: 800, delay: 700 }}>
        <!-- Card 1 -->
        <div class="card bg-base-100 hover:shadow-xl transition-all duration-300 border border-base-200 hover:border-primary/20">
          <div class="card-body items-center text-center">
            <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h2 class="card-title font-bold">Busca Semântica</h2>
            <p class="opacity-75">Encontre informações usando linguagem natural, sem precisar de palavras-chave exatas.</p>
          </div>
        </div>
        
        <!-- Card 2 -->
        <div class="card bg-base-100 hover:shadow-xl transition-all duration-300 border border-base-200 hover:border-primary/20">
          <div class="card-body items-center text-center">
            <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h2 class="card-title font-bold">Documentos Digitalizados</h2>
            <p class="opacity-75">Acesse rapidamente todos os seus documentos e contratos em um só lugar, com organização e praticidade para diversos segmentos.</p>
          </div>
        </div>
        
        <!-- Card 3 -->
        <div class="card bg-base-100 hover:shadow-xl transition-all duration-300 border border-base-200 hover:border-primary/20">
          <div class="card-body items-center text-center">
            <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h2 class="card-title font-bold">Resultados Instantâneos</h2>
            <p class="opacity-75">Obtenha respostas rápidas e precisas sobre cláusulas e condições contratuais.</p>
          </div>
        </div>
      </div>

    </div>
  {/if}
</div>
