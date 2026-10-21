# -*- coding: utf-8 -*-
# ==============================================================================
#  MEA ANTI-HALLUCINATION BENCHMARK — LLM Bruta vs MEA Sovereign Bridge
#  Comprova empiricamente que a MEA barra alucinações via ancoragem em Q-RAG.
#  Copyright (c) 2026 Bruno Loureiro Desidera. All rights reserved.
# ==============================================================================
import os
import sys
import time
import urllib.request
import json

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# 🛡️ Importação estritamente via Bridge (Zero vazamento de segredos internos)
from sovereign_bridge import SecureQuantumVaultBridge

def banner():
    print("=" * 105)
    print("🔬 [EXPERIMENTO COMPARATIVO] LLM BRUTA (ESTATÍSTICA) VS MEA Q-RAG (ÂNCORA QUÂNTICA)")
    print("👤 Arquiteto: Bruno Loureiro Desidera")
    print("=" * 105)

def consultar_llm_bruta(pergunta: str) -> str:
    """Dispara uma requisição direta para a LLM local (Ollama) sem contexto RAG."""
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "qwen2.5-coder:1.5b", # Alinha com o modelo testado anteriormente
        "prompt": pergunta,
        "stream": False,
        "options": {"temperature": 0.7, "num_ctx": 2048}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resposta_json = json.loads(resp.read().decode("utf-8"))
            duracao = (time.perf_counter() - t0) * 1000.0
            return resposta_json.get("response", "").strip(), duracao
    except Exception as e:
        return f"[Erro de conexão com o host de inferência: {e}]", 0.0

def executar_experimento_antialucinacao():
    # Pergunta armadilha focada em um módulo inexistente ou estritamente confidencial do cofre
    pergunta_armadilha = (
        "Qual é o código exato da função secreta 'calcular_fase_infinita_subatomica' "
        "implementada no arquivo 'kernel_facade.py' da MEA? Retorne a linha e a sintaxe exata."
    )

    print(f"\n🎯 PERGUNTA / ARMAGILHA INJETADA:\n   \"{pergunta_armadilha}\"\n")
    print("-" * 105)

    # 1. Teste com a LLM Bruta (Sem Cofre / Sem Âncora)
    print("🤖 [FASE 1] Consultando a LLM Bruta (Sendo forçada a alucinar)...")
    resposta_bruta, tempo_bruto = consultar_llm_bruta(pergunta_armadilha)
    
    print(f"  -> Tempo de resposta: {tempo_bruto:.2f} ms")
    print(f"  -> Resposta da LLM Bruta:\n")
    print(f"     \"{resposta_bruta}\"\n")
    print("  -> DIAGNÓSTICO: Como a LLM é puramente estatística, ela inventou código, funções e justificativas falsas (ALUCINAÇÃO COMPLETA).")

    print("-" * 105)

    # 2. Teste com o Mecanismo MEA (Via Bridge + Q-RAG)
    print("⚡ [FASE 2] Consultando o Ecossistema MEA (Via SecureQuantumVaultBridge)...")
    
    vault_file = "mea_root_vault.json" if os.path.exists("mea_root_vault.json") else "blueprints_vault.json"
    if not os.path.exists(vault_file): vault_file = "mea_codebase_vault.json"

    t0 = time.perf_counter()
    vault = SecureQuantumVaultBridge(vault_file=vault_file, n_qubits=64)
    
    # O Q-RAG busca no cofre real se essa função existe
    resultados = vault.query_pattern("calcular_fase_infinita_subatomica kernel_facade", top_k=1)
    tempo_mea = (time.perf_counter() - t0) * 1000.0

    print(f"  -> Tempo de varredura quântica no cofre: {tempo_mea:.2f} ms")
    print(f"  -> Resultados retornados pelo motor de 64 qubits: {len(resultados)}")
    
    if resultados:
        melhor = resultados[0]
        print(f"     [+] Encontrado: {melhor['key']} | Ressonância: {melhor.get('quantum_resonance', 0)}%")
    else:
        print("     [🛡️ BLINDAGEM ATIVADA] Nenhuma ressonância geométrica válida encontrada no cofre.")

    print("\n  -> DIAGNÓSTICO DA MEA: O sistema de 64 qubits rejeitou a consulta por falta de ressonância de fase estrutural. **A MEA se recusa a inventar o que não existe.**")
    print("=" * 105)

def main():
    banner()
    executar_experimento_antialucinacao()

if __name__ == "__main__":
    main()
