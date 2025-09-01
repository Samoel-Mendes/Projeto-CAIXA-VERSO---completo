# etapa2_estatisticas_filmes.py
import json
from collections import Counter
from typing import List, Dict, Tuple, Any

class EstatisticasFilmes:
    def __init__(self, arquivo_json: str = "catalogo_filmes.json"):
        self.arquivo_json = arquivo_json
        self.filmes = self.carregar_dados()
    
    def carregar_dados(self) -> List[Dict[str, Any]]:
        """Carrega os dados do arquivo JSON usando função de alta ordem"""
        try:
            with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            print(f"✅ Dados carregados: {len(dados)} filmes")
            return dados
        except FileNotFoundError:
            print(f"❌ Arquivo {self.arquivo_json} não encontrado!")
            return []
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar o arquivo JSON!")
            return []
    
    def calcular_media_avaliacao(self) -> float:
        """Calcula a média das avaliações usando funções de alta ordem (map)"""
        if not self.filmes:
            return 0.0
        
        # Usando map para extrair as avaliações
        avaliacoes = list(map(lambda filme: filme['avaliacao'], self.filmes))
        return sum(avaliacoes) / len(avaliacoes)
    
    def calcular_mediana_avaliacao(self) -> float:
        """Calcula a mediana das avaliações usando funções de alta ordem (sorted, map)"""
        if not self.filmes:
            return 0.0
        
        # Usando sorted e map para ordenar as avaliações
        avaliacoes = sorted(map(lambda filme: filme['avaliacao'], self.filmes))
        n = len(avaliacoes)
        
        # Mediana para lista par ou ímpar
        return (avaliacoes[n//2 - 1] + avaliacoes[n//2]) / 2 if n % 2 == 0 else avaliacoes[n//2]
    
    def filmes_acima_avaliacao(self, limite: float = 6.0, ordenar: bool = True) -> List[str]:
        """
        Retorna filmes com avaliação acima do limite usando função própria com parâmetros default
        Parâmetros:
        - limite: float = 6.0 (valor default)
        - ordenar: bool = True (valor default)
        """
        if not self.filmes:
            return []
        
        # Filtra filmes acima do limite
        filmes_filtrados = [
            filme for filme in self.filmes 
            if filme['avaliacao'] > limite
        ]
        
        # Ordena por avaliação (decrescente) se solicitado
        if ordenar:
            filmes_filtrados.sort(key=lambda x: x['avaliacao'], reverse=True)
        
        return [filme['nome'] for filme in filmes_filtrados]
    
    def filmes_em_streaming(self) -> List[str]:
        """Retorna filmes disponíveis em streaming usando list comprehension"""
        return [
            filme['nome'] for filme in self.filmes 
            if filme['streaming']
        ]
    
    def duracao_em_minutos(self, duracao_tuple: Tuple[int, int]) -> int:
        """Converte tupla (horas, minutos) para minutos totais"""
        return duracao_tuple[0] * 60 + duracao_tuple[1]
    
    def extremos_duracao(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Retorna o filme com maior e menor duração
        Usa funções de alta ordem (max, min, lambda)
        """
        if not self.filmes:
            return {}, {}
        
        # Encontra filmes com maior e menor duração usando lambda
        mais_longo = max(self.filmes, key=lambda x: self.duracao_em_minutos(x['duracao']))
        mais_curto = min(self.filmes, key=lambda x: self.duracao_em_minutos(x['duracao']))
        
        return mais_longo, mais_curto
    
    def moda_diretores(self) -> List[Tuple[str, int]]:
        """Retorna a moda dos diretores (os que mais dirigiram filmes) usando Counter"""
        if not self.filmes:
            return []
        
        # Usando list comprehension para extrair diretores
        diretores = [filme['diretor'] for filme in self.filmes]
        
        # Usando Counter para contar ocorrências
        contador = Counter(diretores)
        
        if not contador:
            return []
        
        # Encontra a contagem máxima
        max_contagem = max(contador.values())
        
        # Retorna todos os diretores com a contagem máxima
        return [
            (diretor, contagem) for diretor, contagem in contador.items() 
            if contagem == max_contagem
        ]
    
    def formatar_duracao(self, duracao_tuple: Tuple[int, int]) -> str:
        """Formata a duração para exibição amigável"""
        horas, minutos = duracao_tuple
        return f"{horas}h{minutos:02d}min"
    
    def exibir_estatisticas_completas(self):
        """Exibe todas as estatísticas do catálogo"""
        if not self.filmes:
            print("❌ Nenhum dado disponível para análise!")
            return
        
        print("\n" + "="*70)
        print("📊 ANÁLISE ESTATÍSTICA DO CATÁLOGO DE FILMES")
        print("="*70)
        
        # Estatísticas básicas
        print(f"🎬 Total de filmes analisados: {len(self.filmes)}")
        print(f"⭐ Média de avaliações: {self.calcular_media_avaliacao():.2f}/10")
        print(f"📈 Mediana de avaliações: {self.calcular_mediana_avaliacao():.2f}/10")
        
        # Filmes com avaliação > 6 (usando função com parâmetros default)
        filmes_acima_6 = self.filmes_acima_avaliacao()
        print(f"\n🏆 Filmes com avaliação > 6.0: {len(filmes_acima_6)}")
        for i, filme in enumerate(filmes_acima_6, 1):
            # Encontra a avaliação do filme para exibir
            avaliacao = next((f['avaliacao'] for f in self.filmes if f['nome'] == filme), "N/A")
            print(f"   {i:2d}. {filme} ⭐ {avaliacao}")
        
        # Filmes em streaming (usando list comprehension)
        filmes_streaming = self.filmes_em_streaming()
        print(f"\n📺 Filmes disponíveis em streaming: {len(filmes_streaming)}")
        for i, filme in enumerate(filmes_streaming, 1):
            print(f"   {i:2d}. {filme}")
        
        # Extremos de duração
        mais_longo, mais_curto = self.extremos_duracao()
        if mais_longo and mais_curto:
            print(f"\n⏰ Filme mais longo: {mais_longo['nome']}")
            print(f"   👨‍💼 Diretor: {mais_longo['diretor']}")
            print(f"   ⏱️  Duração: {self.formatar_duracao(mais_longo['duracao'])}")
            
            print(f"\n⏱️  Filme mais curto: {mais_curto['nome']}")
            print(f"   👨‍💼 Diretor: {mais_curto['diretor']}")
            print(f"   ⏰ Duração: {self.formatar_duracao(mais_curto['duracao'])}")
        
        # Moda dos diretores
        moda_diretores = self.moda_diretores()
        if moda_diretores:
            print(f"\n🎭 Diretor(es) mais frequente(s):")
            for diretor, contagem in moda_diretores:
                print(f"   👨‍💼 {diretor}: {contagem} filme(s)")
                
                # Lista filmes desse diretor
                filmes_diretor = [f['nome'] for f in self.filmes if f['diretor'] == diretor]
                for filme in filmes_diretor:
                    print(f"      🎬 {filme}")
        
        # Estatísticas adicionais
        self.exibir_estatisticas_adicionais()
    
    def exibir_estatisticas_adicionais(self):
        """Exibe estatísticas adicionais interessantes"""
        print(f"\n" + "="*70)
        print("📈 ESTATÍSTICAS ADICIONAIS")
        print("="*70)
        
        # Porcentagem em streaming
        total_streaming = len(self.filmes_em_streaming())
        porcentagem = (total_streaming / len(self.filmes)) * 100
        print(f"📊 Porcentagem em streaming: {porcentagem:.1f}%")
        
        # Filme melhor avaliado
        melhor_avaliado = max(self.filmes, key=lambda x: x['avaliacao'])
        print(f"🏅 Melhor avaliado: {melhor_avaliado['nome']} ⭐ {melhor_avaliado['avaliacao']}")
        
        # Filme pior avaliado
        pior_avaliado = min(self.filmes, key=lambda x: x['avaliacao'])
        print(f"⚫ Pior avaliado: {pior_avaliado['nome']} ⭐ {pior_avaliado['avaliacao']}")
        
        # Duração média
        duracoes = [self.duracao_em_minutos(f['duracao']) for f in self.filmes]
        duracao_media_min = sum(duracoes) / len(duracoes)
        horas = int(duracao_media_min // 60)
        minutos = int(duracao_media_min % 60)
        print(f"⏰ Duração média: {horas}h{minutos:02d}min")

    def demonstrar_funcoes_avaliacao(self):
        """Demonstra o uso da função com parâmetros default"""
        print(f"\n" + "="*70)
        print("🔧 DEMONSTRAÇÃO DA FUNÇÃO filmes_acima_avaliacao()")
        print("="*70)
        
        # Com parâmetros default (limite=6.0, ordenar=True)
        print("📋 Com parâmetros default (limite=6.0, ordenar=True):")
        filmes_default = self.filmes_acima_avaliacao()
        print(f"   Encontrados: {len(filmes_default)} filmes")
        
        # Com limite personalizado
        print("\n📋 Com limite=7.5, ordenar=True:")
        filmes_75 = self.filmes_acima_avaliacao(limite=7.5)
        print(f"   Encontrados: {len(filmes_75)} filmes")
        for filme in filmes_75:
            print(f"      🎬 {filme}")
        
        # Sem ordenação
        print("\n📋 Com limite=6.0, ordenar=False:")
        filmes_nao_ordenados = self.filmes_acima_avaliacao(ordenar=False)
        print(f"   Encontrados: {len(filmes_nao_ordenados)} filmes (ordem original)")

# Execução da Etapa 2
def main():
    print("🎬 ETAPA 2: ANÁLISE ESTATÍSTICA DE FILMES")
    print("="*55)
    print("📊 Gerando estatísticas a partir do arquivo JSON...")
    
    # Carregar dados e analisar
    estatisticas = EstatisticasFilmes("catalogo_filmes.json")
    
    if estatisticas.filmes:
        # Exibir estatísticas completas
        estatisticas.exibir_estatisticas_completas()
        
        # Demonstrar função com parâmetros default
        estatisticas.demonstrar_funcoes_avaliacao()
        
        print(f"\n" + "="*70)
        print("✅ ETAPA 2 CONCLUÍDA COM SUCESSO!")
        print("="*70)
    else:
        print("❌ Não foi possível carregar dados para análise.")

if __name__ == "__main__":
    main()