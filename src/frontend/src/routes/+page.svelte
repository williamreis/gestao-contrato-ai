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
      <div class="hero rounded-1xl overflow-hidden bg-gradient-to-br from-primary/5 to-secondary/5 backdrop-blur-sm shadow-lg mb-16">
        <div class="hero-content flex-col lg:flex-row py-12 px-8">
          <!-- Texto Principal -->
          <div class="lg:w-2/2 text-center lg:text-left" in:fly={{ y: 20, duration: 800, delay: 300 }}>
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">
              <span class="text-primary1">Gestão de Documento Inteligente</span>
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

    </div>
  {/if}
</div>
