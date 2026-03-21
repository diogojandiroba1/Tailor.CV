"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [vaga, setVaga] = useState("");
  const [modo, setModo] = useState("Gaps");
  const [loading, setLoading] = useState(false);
  const [sucesso, setSucesso] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !vaga) {
      alert("Por favor, anexe o currículo e cole a descrição da vaga.");
      return;
    }

    setLoading(true);
    setSucesso(false);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("vaga", vaga);
    formData.append("modo", modo);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erro ao gerar o currículo");
      }

      // Transforma a resposta do backend em um arquivo binário (Blob)
      const blob = await response.blob();
      
      // Cria um link temporário na memória do navegador
      const url = window.URL.createObjectURL(blob);
      
      // Cria uma tag <a> invisível e força o clique nela para baixar o arquivo
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "TailorCV_Otimizado.pdf"); // Nome do arquivo que vai baixar
      document.body.appendChild(link);
      link.click();
      
      // Limpa a memória
      link.remove();
      window.URL.revokeObjectURL(url);
      
      setSucesso(true);
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro ao conectar com o backend. Verifique se a API está rodando.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 text-gray-800">
      <div className="max-w-3xl mx-auto space-y-8">
        
        <header className="text-center">
          <h1 className="text-4xl font-bold text-blue-600">Tailor.CV</h1>
          <p className="text-gray-500 mt-2">Otimize seu currículo com IA</p>
        </header>

        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-md space-y-6">
          
          <div>
            <label className="block font-semibold mb-2">1. Upload do Currículo (PDF)</label>
            <input 
              type="file" 
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full border p-2 rounded"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">2. Descrição da Vaga</label>
            <textarea 
              rows={5}
              value={vaga}
              onChange={(e) => setVaga(e.target.value)}
              placeholder="Cole aqui os requisitos e a descrição da vaga..."
              className="w-full border p-2 rounded"
            />
          </div>

          <div>
            <label className="block font-semibold mb-2">3. Modo de Operação</label>
            <select 
              value={modo} 
              onChange={(e) => setModo(e.target.value)}
              className="w-full border p-2 rounded"
            >
              <option value="Gaps">🔍 Analisador de Gaps</option>
              <option value="Seguro">🛡️ Otimização Segura</option>
              <option value="Inclusao">⚠️ Inclusão Forçada</option>
            </select>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 text-white font-bold py-3 rounded hover:bg-blue-700 transition disabled:bg-gray-400"
          >
            {loading ? "Processando e Gerando PDF... ⚙️" : "Gerar Novo Currículo"}
          </button>
        </form>

        {sucesso && (
          <div className="bg-green-100 text-green-800 p-4 rounded-xl text-center font-semibold">
            🎉 Currículo otimizado com sucesso! O download deve ter começado automaticamente.
          </div>
        )}

      </div>
    </main>
  );
}