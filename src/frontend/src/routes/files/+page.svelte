<script lang="ts">
import { onMount } from 'svelte';
let arquivos: string[] = [];
let loading = true;
let error = '';

async function deletarArquivo(nome: string) {
  if (!confirm(`Deseja realmente deletar o arquivo "${nome}"?`)) return;
  try {
    const res = await fetch(`http://localhost:8002/document/delete/${encodeURIComponent(nome)}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Erro ao deletar arquivo');
    arquivos = arquivos.filter(a => a.nome !== nome);
  } catch (e) {
    error = e.message || 'Erro desconhecido';
  }
}

onMount(async () => {
  try {
    const UPLOAD_API_URL = 'http://localhost:8002';
    const res = await fetch(`${UPLOAD_API_URL}/storage/list`);
    if (!res.ok) throw new Error('Erro ao buscar arquivos');
    const data = await res.json();
    arquivos = Array.isArray(data.documentos) ? data.documentos : [];
  } catch (e) {
    error = e.message || 'Erro desconhecido';
  } finally {
    loading = false;
  }
});
</script>

<div class="max-w-2xl mx-auto p-6">
  <h1 class="text-2xl font-bold mb-4">Documentos</h1>
  {#if loading}
    <div class="text-gray-500">Carregando...</div>
  {:else if error}
    <div class="text-red-500">{error}</div>
  {:else if arquivos.length === 0}
    <div class="text-gray-500">Nenhum arquivo encontrado.</div>
  {:else}
    <ul class="divide-y divide-gray-200 bg-white rounded shadow">
      {#each arquivos as arquivo}
        <li class="p-3 flex items-center justify-between">
          <span class="truncate">{arquivo.nome}</span>
          <a class="btn btn-sm btn-primary" href={`http://localhost:8002${arquivo.url}`} target="_blank">Baixar</a>
          <button class="btn btn-sm btn-danger ml-2" on:click={() => deletarArquivo(arquivo.nome)}>
            Deletar
          </button>
        </li>
      {/each}
    </ul>
  {/if}
</div>
