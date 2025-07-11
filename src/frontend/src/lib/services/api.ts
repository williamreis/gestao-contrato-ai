import axios from 'axios';
import { env } from '$env/dynamic/public';

// Usar sempre a URL completa para evitar problemas com proxy
const API_URL = 'http://127.0.0.1:8002';

console.log('API URL configurada para:', API_URL);

// Configurar o axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Aumentar o timeout para evitar falhas rápidas
  timeout: 10000
});

export interface Documento {
  arquivo: string;
  texto: string;
  score?: number;
  tipo_documento: string;
}

export interface SearchResponse {
  resultados: Documento[];
  total: number;
}

export interface LLMResponse {
  answer: string;
  sources: Array<{
    filename?: string;
    [key: string]: any;
  }>;
}

export const documentoService = {
  // Listar todos os documentos com paginação
  listarDocumentos: async (skip = 0, limit = 10): Promise<SearchResponse> => {
    try {
      console.log(`Chamando API: /document/list?skip=${skip}&limit=${limit}`);
      const response = await api.get(`/document/list?skip=${skip}&limit=${limit}`);
      console.log('Resposta da API:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro na chamada da API:', error);
      throw error;
    }
  },

  // Buscar documentos por consulta semântica
  buscarDocumentos: async (query: string, limit = 5): Promise<SearchResponse> => {
    try {
      console.log(`Chamando API: /document/search?q=${encodeURIComponent(query)}&limit=${limit}`);
      const response = await api.get(`/document/search?q=${encodeURIComponent(query)}&limit=${limit}`);
      console.log('Resposta da API:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro na chamada da API:', error);
      throw error;
    }
  },

  // Listar todos os arquivos únicos
  listarArquivos: async (): Promise<string[]> => {
    const response = await api.get('/document/files');
    return response.data.arquivos;
  },

  // Perguntar ao LLM
  askQuestion: async (question: string, maxResults = 3): Promise<LLMResponse> => {
    try {
      console.log(`Chamando API: /llm/ask com pergunta: "${question}"`);
      
      // Tratamento especial para garantir que a pergunta seja válida
      if (!question || question.trim() === '') {
        throw new Error('A pergunta não pode estar vazia');
      }
      
      // Limitar o tamanho da pergunta para evitar problemas
      const trimmedQuestion = question.trim().substring(0, 1000);
      
      // Usar uma abordagem mais robusta com timeout maior para o LLM
      const response = await api.post('/llm/ask', {
        question: trimmedQuestion,
        max_results: maxResults
      }, {
        timeout: 30000 // 30 segundos para dar tempo ao LLM processar
      });
      
      console.log('Resposta do LLM recebida com sucesso');
      return response.data;
    } catch (error: any) {
      // Tratamento de erro mais informativo
      if (error.response) {
        // O servidor respondeu com um status de erro
        console.error(`Erro ${error.response.status} na chamada do LLM:`, error.response.data);
        throw new Error(error.response.data.detail || 'Erro ao processar a pergunta');
      } else if (error.request) {
        // A requisição foi feita mas não houve resposta
        console.error('Timeout ou erro de rede na chamada do LLM');
        throw new Error('Não foi possível obter resposta do servidor. Verifique sua conexão.');
      } else {
        // Erro na configuração da requisição
        console.error('Erro na configuração da chamada do LLM:', error.message);
        throw new Error('Erro ao preparar a consulta: ' + error.message);
      }
    }
  }
};

export default api;
