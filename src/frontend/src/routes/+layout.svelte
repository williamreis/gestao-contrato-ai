<script>
  import '../app.css';
  import { writable } from 'svelte/store';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  
  // Store global para controlar a visibilidade do status da API
  export const showApiStatus = writable(false);
  
  // Store para controlar o tema atual
  export const currentTheme = writable('layout_light');
  
  // Função para alternar o tema entre claro e escuro
  function toggleTheme() {
    currentTheme.update(theme => {
      const newTheme = theme === 'layout_dark' ? 'layout_light' : 'layout_dark';
      localStorage.setItem('layout_-theme', newTheme);
      document.documentElement.setAttribute('data-theme', newTheme);
      return newTheme;
    });
  }
  
  // Carregar o tema salvo no localStorage ao montar o componente
  onMount(() => {
    const savedTheme = localStorage.getItem('layout_-theme') || 'layout_light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    currentTheme.set(savedTheme);
  });
  
  function toggleApiStatus() {
    showApiStatus.update(value => {
      const newValue = !value;
      console.log('Toggle API Status:', newValue);
      return newValue;
    });
  }
</script>

<div class="min-h-screen flex flex-col bg-base-100 animate-fade-in">
  <header class="sticky top-0 z-50">
    <div class="navbar bg-blue-700 text-primary-content shadow-lg">
      <div class="navbar-start">
        <div class="dropdown">
          <label class="btn btn-ghost lg:hidden hover:bg-primary/20 transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </label>
          <ul class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-base-100 rounded-xl w-52 text-base-content">
            <li>
              <a href="/" class="font-medium flex items-center gap-2 hover:text-primary transition-colors duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
                  </svg>
                  Início
              </a>
            </li>
            <li>
              <a href="/search" class="font-medium flex items-center gap-2 hover:text-primary transition-colors duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Pesquisa
              </a>
            </li>
            <li>
              <a href="/upload" class="font-medium flex items-center gap-2 hover:text-primary transition-colors duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10C8 7.79086 9.79086 6 12 6C14.2091 6 16 7.79086 16 10V11H17C18.933 11 20.5 12.567 20.5 14.5C20.5 16.433 18.933 18 17 18H16C15.4477 18 15 18.4477 15 19C15 19.5523 15.4477 20 16 20H17C20.0376 20 22.5 17.5376 22.5 14.5C22.5 11.7793 20.5245 9.51997 17.9296 9.07824C17.4862 6.20213 15.0003 4 12 4C8.99974 4 6.51381 6.20213 6.07036 9.07824C3.47551 9.51997 1.5 11.7793 1.5 14.5C1.5 17.5376 3.96243 20 7 20H8C8.55228 20 9 19.5523 9 19C9 18.4477 8.55228 18 8 18H7C5.067 18 3.5 16.433 3.5 14.5C3.5 12.567 5.067 11 7 11H8V10ZM15.7071 13.2929L12.7071 10.2929C12.3166 9.90237 11.6834 9.90237 11.2929 10.2929L8.29289 13.2929C7.90237 13.6834 7.90237 14.3166 8.29289 14.7071C8.68342 15.0976 9.31658 15.0976 9.70711 14.7071L11 13.4142V19C11 19.5523 11.4477 20 12 20C12.5523 20 13 19.5523 13 19V13.4142L14.2929 14.7071C14.6834 15.0976 15.3166 15.0976 15.7071 14.7071C16.0976 14.3166 16.0976 13.6834 15.7071 13.2929Z" />
                  </svg>
                  Upload
              </a>
            </li>
            <li>
              <a href="/files" class="font-medium flex items-center gap-2 hover:text-primary transition-colors duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Documentos
              </a>
            </li>
          </ul>
        </div>
        <a href="/" class="btn btn-ghost normal-case text-xl font-bold tracking-tight hover:bg-primary/20 transition-all duration-300">
          <span class="text-white">Gestão de Documento | RAG</span>
        </a>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li>
            <a href="/" class="font-medium flex items-center gap-2 hover:bg-primary/20 transition-colors duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
              </svg>
              Início
            </a>
          </li>
          <li>
            <a href="/search" class="font-medium flex items-center gap-2 hover:bg-primary/20 transition-colors duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Pesquisa
            </a>
          </li>
          <li>
            <a href="/upload" class="font-medium flex items-center gap-2 hover:bg-primary/20 transition-colors duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M8 10C8 7.79086 9.79086 6 12 6C14.2091 6 16 7.79086 16 10V11H17C18.933 11 20.5 12.567 20.5 14.5C20.5 16.433 18.933 18 17 18H16C15.4477 18 15 18.4477 15 19C15 19.5523 15.4477 20 16 20H17C20.0376 20 22.5 17.5376 22.5 14.5C22.5 11.7793 20.5245 9.51997 17.9296 9.07824C17.4862 6.20213 15.0003 4 12 4C8.99974 4 6.51381 6.20213 6.07036 9.07824C3.47551 9.51997 1.5 11.7793 1.5 14.5C1.5 17.5376 3.96243 20 7 20H8C8.55228 20 9 19.5523 9 19C9 18.4477 8.55228 18 8 18H7C5.067 18 3.5 16.433 3.5 14.5C3.5 12.567 5.067 11 7 11H8V10ZM15.7071 13.2929L12.7071 10.2929C12.3166 9.90237 11.6834 9.90237 11.2929 10.2929L8.29289 13.2929C7.90237 13.6834 7.90237 14.3166 8.29289 14.7071C8.68342 15.0976 9.31658 15.0976 9.70711 14.7071L11 13.4142V19C11 19.5523 11.4477 20 12 20C12.5523 20 13 19.5523 13 19V13.4142L14.2929 14.7071C14.6834 15.0976 15.3166 15.0976 15.7071 14.7071C16.0976 14.3166 16.0976 13.6834 15.7071 13.2929Z" fill="#ffffff" /></svg>
              Upload
            </a>
          </li>
          <li>
            <a href="/files" class="font-medium flex items-center gap-2 hover:bg-primary/20 transition-colors duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Documentos
            </a>
          </li>
        </ul>
      </div>
    </div>
  </header>

  <main class="flex-grow container mx-auto px-4 py-8" transition:fade={{ duration: 300 }}>
    <!-- Alerta global para status da API ou mensagens -->
    {#if $showApiStatus}
      <div class="alert alert-info shadow-lg mb-6 animate-fade-in">
        <span class="font-medium">Status da API:</span> Online
        <button class="btn btn-sm btn-circle btn-ghost ml-auto" on:click={toggleApiStatus}>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
    {/if}
    <slot />
  </main>

</div>
