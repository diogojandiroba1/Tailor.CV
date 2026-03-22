"use client";

import { useState } from "react";
import { Upload, FileText, Shield, Zap, CheckCircle, Download, Layout } from "lucide-react"; 

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [vaga, setVaga] = useState("");
  const [modo, setModo] = useState("Gaps");
  const [template, setTemplate] = useState("Template Recomendado");
  const [loading, setLoading] = useState(false);
  const [sucesso, setSucesso] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !vaga) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    setLoading(true);
    setSucesso(false);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("vaga", vaga);
    formData.append("modo", modo);
    formData.append("template", template);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Erro na geração");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `TailorCV_${template}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      setSucesso(true);
    } catch (error) {
      alert("Erro ao conectar com o servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8FAFC] text-slate-900 pb-20">
      {/* Navbar Minimalista */}
      <nav className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-2 rounded-lg">
              <Zap className="text-white w-5 h-5" />
            </div>
            <span className="text-xl font-bold tracking-tight">Tailor.CV</span>
          </div>
          <span className="text-xs font-medium bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full uppercase">Beta Gratuito</span>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto mt-12 px-6">
        <header className="mb-12 text-center">
          <h2 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">
            Consiga mais entrevistas.
          </h2>
          <p className="mt-4 text-lg text-slate-600 max-w-2xl mx-auto">
            Nossa IA ajusta seu currículo para os termos específicos de cada vaga em segundos. Escolha um modo e brilhe no processo seletivo.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-8">
            {/* Seção de Upload */}
            <section className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="flex items-center gap-2 font-bold text-lg mb-6">
                <FileText className="w-5 h-5 text-indigo-500" />
                Dados do Currículo
              </h3>
              
              <div className="space-y-6">
                <div 
                  className={`relative border-2 border-dashed rounded-xl p-8 transition-all text-center ${file ? 'border-green-400 bg-green-50' : 'border-slate-300 hover:border-indigo-400'}`}
                >
                  <input 
                    type="file" 
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <Upload className={`mx-auto mb-4 w-10 h-10 ${file ? 'text-green-500' : 'text-slate-400'}`} />
                  <p className="font-medium">{file ? file.name : "Arraste seu PDF aqui ou clique para buscar"}</p>
                  <p className="text-xs text-slate-500 mt-2">Apenas arquivos PDF (Máx. 5MB)</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Descrição da Vaga</label>
                  <textarea 
                    rows={6}
                    value={vaga}
                    onChange={(e) => setVaga(e.target.value)}
                    placeholder="Dica: Cole o texto do anúncio do LinkedIn ou Indeed aqui..."
                    className="w-full border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all p-4 text-sm"
                  />
                </div>
              </div>
            </section>

            {/* Modos de Operação (Cards) */}
            <section className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="font-bold text-lg mb-6">Configuração da IA</h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {[
                  { id: 'Gaps', label: 'Gap Analysis', icon: <FileText className="w-5 h-5"/>, color: 'blue' },
                  { id: 'Seguro', label: 'Otimização', icon: <Shield className="w-5 h-5"/>, color: 'indigo' },
                  { id: 'Inclusao', label: 'Full Match', icon: <Zap className="w-5 h-5"/>, color: 'orange' },
                ].map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setModo(item.id)}
                    className={`flex flex-col items-center p-4 rounded-xl border-2 transition-all ${
                      modo === item.id 
                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700 shadow-sm' 
                        : 'border-slate-100 hover:border-slate-300'
                    }`}
                  >
                    {item.icon}
                    <span className="text-xs font-bold mt-2">{item.label}</span>
                  </button>
                ))}
              </div>
            </section>
          </div>

          {/* Lateral: Templates e Finalização */}
          <div className="space-y-6">
            <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <h3 className="flex items-center gap-2 font-bold text-md mb-4">
                <Layout className="w-4 h-4 text-slate-500" />
                Template
              </h3>
              <div className="space-y-3">
                {['Template Recomendado'].map((t) => (
                  <label key={t} className="flex items-center gap-3 p-3 border-2 border-indigo-200 rounded-lg cursor-pointer bg-indigo-50 transition-colors">
                    <input 
                      type="radio" 
                      name="template" 
                      checked={template === t}
                      onChange={() => setTemplate(t)}
                      className="text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="text-sm font-medium text-indigo-900">{t}</span>
                  </label>
                ))}
              </div>
            </section>

            <button 
              onClick={handleSubmit}
              disabled={loading}
              className="w-full bg-slate-900 text-white font-bold py-4 rounded-2xl hover:bg-indigo-600 transition-all shadow-lg hover:shadow-indigo-200 flex items-center justify-center gap-2 disabled:bg-slate-300"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
                  <span>Processando...</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  <span>Gerar Currículo</span>
                </>
              )}
            </button>

            {sucesso && (
              <div className="flex items-center gap-3 bg-green-50 border border-green-200 p-4 rounded-xl text-green-700 animate-in fade-in zoom-in duration-300">
                <CheckCircle className="w-5 h-5 flex-shrink-0" />
                <p className="text-xs font-semibold">Tudo pronto! O download iniciou.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}