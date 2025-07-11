<script lang="ts">
  import type { Documento } from '$lib/services/api';
  
  export let documento: Documento;
  export let expanded = false;
</script>

<div class="card bg-base-100 shadow-xl mb-4 hover:shadow-2xl transition-shadow duration-300">
  <div class="card-body">
    <h2 class="card-title flex justify-between">
      <span>{documento.arquivo}</span>
      {#if documento.score !== undefined}
        <span class="badge badge-primary">{(documento.score * 100).toFixed(0)}% relevante</span>
      {/if}
      {#if documento.tipo_documento !== undefined}
        <span class="badge badge-primary">Tipo: {documento.tipo_documento}</span>
      {/if}
    </h2>
    
    <div class="mt-2">
      {#if expanded || documento.texto.length < 200}
        <p class="whitespace-pre-line">{documento.texto}</p>
      {:else}
        <p class="whitespace-pre-line">{documento.texto.substring(0, 200)}...</p>
      {/if}
    </div>
    
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-sm" on:click={() => expanded = !expanded}>
        {expanded ? 'Mostrar menos' : 'Mostrar mais'}
      </button>
      {#if documento.url}
        <a class="btn btn-sm btn-primary" href={documento.url} target="_blank" download>
          Baixar PDF
        </a>
      {/if}
    </div>
  </div>
</div>
