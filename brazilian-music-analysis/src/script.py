import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from deep_translator import GoogleTranslator
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re
import json
import time
import numpy as np

class AnalisadorMusicas:
    def __init__(self):
        model_name = "SamLowe/roberta-base-go_emotions"
        print("Carregando modelo de análise de sentimentos...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("text-classification",
                                   model=self.model,
                                   tokenizer=self.tokenizer,
                                   top_k=None)
        print("Modelo carregado com sucesso!")
        self.traducao_sentimentos = {
            "admiration": "admiração",
            "amusement": "diversão",
            "anger": "raiva",
            "annoyance": "irritação",
            "approval": "aprovação",
            "caring": "cuidado",
            "confusion": "confusão",
            "curiosity": "curiosidade",
            "desire": "desejo",
            "disappointment": "decepção",
            "disapproval": "desaprovação",
            "disgust": "nojo",
            "embarrassment": "vergonha",
            "excitement": "empolgação",
            "fear": "medo",
            "gratitude": "gratidão",
            "grief": "luto",
            "joy": "alegria",
            "love": "amor",
            "nervousness": "nervosismo",
            "optimism": "otimismo",
            "pride": "orgulho",
            "realization": "percepção",
            "relief": "alívio",
            "remorse": "remorso",
            "sadness": "tristeza",
            "surprise": "surpresa",
            "neutral": "neutro"
        }
        self.translation_cache = {}

    def _limpar_texto(self, texto):
        texto = re.sub(r"[^\w\s]", "", texto)
        texto = texto.lower()
        return texto

    def _contar_frequencia_palavras(self, texto, max_palavras=30):
        self.stopwords_personalizadas = {
            "a", "ao", "aos", "aquela", "aquele", "aquilo", "as", "até", "com", "como", "da", "das", "de", "dessa",
            "desse", "disso", "do", "dos", "dum", "duma", "e", "em", "entre", "era", "eram", "essa", "esse", "esta",
            "este", "estou", "foi", "for", "fui", "havia", "hei", "isso", "isto", "já", "la", "lá", "lhe", "lhes",
            "lo", "mas", "me", "mais", "muito", "na", "nas", "nem", "no", "o", "os", "ou", "para", "pela", "pelas",
            "pelo", "pelos", "per", "pero", "pode", "por", "porque", "pois", "qual", "quando", "que", "quem", "se",
            "si", "sido", "tal", "tambem", "te", "tem", "tive", "um", "uma", "umas", "uns", "tá", "tô", "vou", "vem",
            "oh", "ah", "ai", "ui", "ei", "opa", "eh", "ta", "né", "num", "pra", "pro", "pô", "ó", "ué", "hey", "yo", "é"
        }
        palavras = [
            p for p in self._limpar_texto(texto).split()
            if p not in self.stopwords_personalizadas
        ]
        total = len(palavras)
        if total == 0:
            return {}
        frequencias = Counter(palavras)
        frequencias_norm = {palavra: freq / total for palavra, freq in frequencias.items()}
        frequencias_norm = dict(Counter(frequencias_norm).most_common(max_palavras))
        return frequencias_norm

    def _converter_para_porcentagem(self, dados):
        if not dados:
            return {}
        total = sum(dados.values())
        if total == 0:
            return {}
        return {k: round(v / total * 100, 2) for k, v in dados.items()}

    def _exibir_histograma(self, dados, titulo, xlabel):
        if not dados:
            print(f"Sem dados para exibir no histograma: {titulo}")
            return
        
        if all(0 <= v <= 1 for v in dados.values()):
            dados_plot = {k: v * 100 for k, v in dados.items()}
        else:
            dados_plot = dados

        palavras = list(dados_plot.keys())
        frequencias = list(dados_plot.values())
        
        # Aumentar significativamente o tamanho da figura
        plt.figure(figsize=(18, 12))
        
        # Barras mais grossas
        bars = plt.bar(palavras, frequencias, color='skyblue', width=0.8, edgecolor='navy', linewidth=2)
        
        # Título removido conforme solicitado
        
        # Labels maiores
        plt.xlabel(xlabel, fontsize=18, fontweight='bold')
        plt.ylabel('Frequência (%)', fontsize=18, fontweight='bold')
        
        # Tick labels maiores
        plt.xticks(rotation=45, ha='right', fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        
        # Removido: Valores nas barras para apresentação mais limpa
        
        # Adicionar grid sutil
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()

    def _exibir_wordcloud(self, dados, titulo):
        if not dados:
            print(f"Sem dados para exibir na wordcloud: {titulo}")
            return
        wordcloud = WordCloud(width=1200, height=600, background_color='white', max_font_size=100).generate_from_frequencies(dados)
        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        # Título removido conforme solicitado
        plt.tight_layout()
        plt.show()

    def _traduzir_texto_grande(self, texto_pt, limite=4500):
        if texto_pt in self.translation_cache:
            return self.translation_cache[texto_pt]

        texto_pt = ' '.join(texto_pt.split())
        partes = []
        atual = ""
        palavras = texto_pt.split()
        for palavra in palavras:
            if len(atual) + len(palavra) + 1 > limite:
                if atual:
                    partes.append(atual.strip())
                atual = palavra
            else:
                atual += " " + palavra
        if atual:
            partes.append(atual.strip())
        if not partes:
            return ""
        print(f"Dividindo texto em {len(partes)} partes para tradução...")
        try:
            traducoes = []
            for i, parte in enumerate(partes):
                print(f"Traduzindo parte {i+1}/{len(partes)}...")
                traducao = GoogleTranslator(source='pt', target='en').translate(parte)
                traducoes.append(traducao)
                time.sleep(0.5)
            full_translation = " ".join(traducoes)
            self.translation_cache[texto_pt] = full_translation
            return full_translation
        except Exception as e:
            print(f"Erro na tradução: {e}")
            print("Continuando análise sem tradução...")
            return ""

    def _analisar_sentimentos(self, texto_en):
        if not texto_en.strip():
            print("Texto vazio para análise de sentimentos")
            return {}
        sentencas = []
        raw_sentences = re.split(r'(?<=[.!?])\s+', texto_en)
        
        for frase in raw_sentences:
            frase = frase.strip()
            if not frase:
                continue
            
            if len(frase) > 400:
                sub_frases = re.split(r'(?<=[,;])\s*', frase)
                temp_segment = ""
                for sub in sub_frases:
                    if len(temp_segment) + len(sub) + 1 < 400:
                        temp_segment += sub + ", "
                    else:
                        if temp_segment:
                            sentencas.append(temp_segment.strip().rstrip(','))
                        temp_segment = sub + ", "
                if temp_segment:
                    sentencas.append(temp_segment.strip().rstrip(','))
            else:
                sentencas.append(frase)
        
        sentencas_filtradas = [s for s in sentencas if len(s) > 10 and len(s.split()) <= 100]

        if not sentencas_filtradas:
            print("Nenhuma sentença válida encontrada após filtragem")
            return {}

        print(f"Analisando sentimentos em {len(sentencas_filtradas)} segmentos...")
        acumulador = Counter()
        processadas = 0
        try:
            for i, sentenca in enumerate(sentencas_filtradas):
                try:
                    resultado = self.classifier(sentenca)[0]
                    for r in resultado:
                        label = r["label"]
                        score = r["score"]
                        acumulador[label] += score
                    processadas += 1
                    if (i + 1) % 50 == 0:
                        print(f"Processadas {i + 1}/{len(sentencas_filtradas)} sentenças...")
                except Exception as e:
                    print(f"Erro ao processar sentença {i+1} ('{sentenca[:50]}...'): {str(e)[:100]}...")
                    continue
        except Exception as e:
            print(f"Erro geral na análise de sentimentos: {e}")
            return {}

        print(f"Total de sentenças processadas com sucesso: {processadas}")
        if not acumulador:
            return {}
        
        total_score = sum(acumulador.values())
        if total_score > 0:
            sentimentos = {k: round(v / total_score, 6) 
                           for k, v in acumulador.items() 
                           if v / total_score > 0.01}
            return sentimentos
        return {}

    def _exibir_histograma_top_por_ano(self, dados_por_ano, titulo, xlabel, top_n=6):
        """
        Gera um histograma sofisticado mostrando os elementos mais frequentes agrupados por palavra,
        com barras lado a lado coloridas por ano. Melhorado para apresentações.
        """
        if not dados_por_ano:
            print(f"Sem dados para exibir no histograma por ano: {titulo}")
            return

        # Coletar todas as palavras/sentimentos únicos dos top N de cada ano
        todos_elementos = set()
        dados_organizados = {}
        
        anos_ordenados = sorted(dados_por_ano.keys())
        
        # Primeiro, coletar todos os elementos únicos
        for ano in anos_ordenados:
            if dados_por_ano[ano]:
                top_items = Counter(dados_por_ano[ano]).most_common(top_n)
                dados_organizados[ano] = dict(top_items)
                todos_elementos.update([item[0] for item in top_items])
        
        if not todos_elementos:
            print(f"Nenhum elemento encontrado para plotar: {titulo}")
            return
            
        # Ordenar elementos por frequência total (soma de todos os anos)
        freq_total = {}
        for elemento in todos_elementos:
            freq_total[elemento] = sum(
                dados_organizados[ano].get(elemento, 0) for ano in anos_ordenados
            )
        
        # Pegar apenas os top 12 elementos mais frequentes no geral
        elementos_ordenados = sorted(freq_total.items(), key=lambda x: x[1], reverse=True)[:12]
        elementos_finais = [elem[0] for elem in elementos_ordenados]
        
        # Configurar o gráfico com tamanho maior
        fig, ax = plt.subplots(figsize=(22, 14))
        
        num_elementos = len(elementos_finais)
        num_anos = len(anos_ordenados)
        
        # Largura das barras aumentada
        bar_width = 0.9 / num_anos
        positions = np.arange(num_elementos)
        
        # Mapa de cores para anos
        cmap = plt.cm.get_cmap('tab10', num_anos)
        year_colors = {ano: cmap(i) for i, ano in enumerate(anos_ordenados)}
        
        # Plotar barras para cada ano
        max_valor = 0
        for i, ano in enumerate(anos_ordenados):
            valores = []
            for elemento in elementos_finais:
                valor = dados_organizados.get(ano, {}).get(elemento, 0)
                # Converter para porcentagem se necessário
                if isinstance(valor, float) and 0 <= valor <= 1:
                    valor = valor * 100
                valores.append(valor)
                max_valor = max(max_valor, valor)
            
            # Calcular posição das barras para este ano
            bar_positions = positions + (i - (num_anos-1)/2) * bar_width
            
            bars = ax.bar(bar_positions, valores, bar_width, 
                         label=str(ano), color=year_colors[ano], alpha=0.8,
                         edgecolor='black', linewidth=1.5)
            
        
        # Configurar labels e título com fontes maiores
        ax.set_xlabel(xlabel, fontsize=20, fontweight='bold')
        ax.set_ylabel('Frequência (%)', fontsize=20, fontweight='bold')
        # Título removido conforme solicitado
        
        # Configurar eixo X com fonte maior
        ax.set_xticks(positions)
        ax.set_xticklabels(elementos_finais, rotation=45, ha='right', fontsize=16, fontweight='bold')
        ax.tick_params(axis='y', labelsize=16)
        
        # Configurar legenda DENTRO do gráfico
        legend = ax.legend(title='Ano', title_fontsize=16, fontsize=14, 
                          loc='upper right', bbox_to_anchor=(0.98, 0.98),
                          framealpha=0.9, fancybox=True, shadow=True)
        legend.get_title().set_fontweight('bold')
        
        # Adicionar grid sutil
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_axisbelow(True)
        
        # Melhorar o layout
        plt.tight_layout()
        plt.show()

    def _exibir_histograma_consolidado(self, dados_por_ano, titulo, xlabel):
        """
        Gera um histograma consolidado dos elementos mais frequentes ao longo dos anos.
        Melhorado para apresentações com elementos visuais maiores.
        """
        if not dados_por_ano:
            print(f"Sem dados para exibir no histograma consolidado: {titulo}")
            return

        # Agregação dos dados de todos os anos
        dados_agregados = Counter()
        for ano, dados in dados_por_ano.items():
            for item, freq in dados.items():
                dados_agregados[item] += freq

        if not dados_agregados:
            print(f"Nenhum dado agregado para plotar no histograma consolidado: {titulo}")
            return

        # Normalizar os dados agregados para porcentagem, se necessário
        total_agregado = sum(dados_agregados.values())
        if total_agregado == 0:
            print(f"Total agregado é zero para o histograma consolidado: {titulo}")
            return {}

        # Pegar os top 15 elementos mais frequentes no geral
        top_items_geral = Counter(dados_agregados).most_common(15)
        
        labels = [item[0] for item in top_items_geral]
        values = [item[1] for item in top_items_geral]

        # Se os valores são scores normalizados (0-1), multiplique por 100 para %
        if all(0 <= v <= 1 for v in values):
             values_plot = [v * 100 for v in values]
        else:
            values_plot = [(v / total_agregado) * 100 for v in values]

        # Criar figura maior
        plt.figure(figsize=(20, 12))
        
        # Barras mais grossas e com bordas
        bars = plt.bar(labels, values_plot, color='lightcoral', width=0.8, 
                      edgecolor='darkred', linewidth=2, alpha=0.8)
        
        # Título removido conforme solicitado
        plt.xlabel(xlabel, fontsize=20, fontweight='bold')
        plt.ylabel('Frequência (%)', fontsize=20, fontweight='bold')
        
        # Tick labels maiores
        plt.xticks(rotation=45, ha='right', fontsize=16, fontweight='bold')
        plt.yticks(fontsize=16, fontweight='bold')
        
        
        # Adicionar informações na legenda interna
        textstr = f'Total de elementos analisados: {len(dados_agregados)}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=14,
                verticalalignment='top', bbox=props, fontweight='bold')
        
        # Grid
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()

    def analisar_colecao_musicas(self, musicas_data):
        print("=== INICIANDO ANÁLISE DA COLEÇÃO DE MÚSICAS ===\n")
        print(f"Total de músicas na coleção: {len(musicas_data)}")
        
        letras_por_ano = Counter()
        palavras_freq_por_ano = {}
        sentimentos_por_ano = {}
        
        musicas_processadas = 0
        
        for musica in musicas_data:
            if 'lyrics' in musica and musica['lyrics'] and 'year' in musica and musica['year']:
                ano = int(musica['year'])
                if ano not in letras_por_ano:
                    letras_por_ano[ano] = ""
                letras_por_ano[ano] += " " + musica['lyrics']
                musicas_processadas += 1
            elif 'lyrics' in musica and musica['lyrics']:
                print(f"Aviso: Música '{musica.get('title', 'Sem Título')}' não possui ano. Ignorando para análise anual.")

        print(f"Músicas com letras e ano processadas: {musicas_processadas}")
        if not letras_por_ano:
            print("Erro: Nenhuma letra com ano encontrada para análise!")
            return

        print("\n=== INICIANDO ANÁLISE POR ANO ===")
        for ano, letras_do_ano in sorted(letras_por_ano.items()):
            print(f"\n--- Processando ano: {ano} ---")
            
            print(f"Analisando frequência de palavras para {ano}...")
            palavras_freq = self._contar_frequencia_palavras(letras_do_ano, max_palavras=40)
            palavras_freq_por_ano[ano] = palavras_freq
            
            print(f"Iniciando tradução para {ano}...")
            texto_en = self._traduzir_texto_grande(letras_do_ano)
            
            if texto_en.strip():
                print(f"Tradução para {ano} concluída. Analisando sentimentos...")
                sentimentos = self._analisar_sentimentos(texto_en)
                if sentimentos:
                    sentimentos_traduzidos = {
                        self.traducao_sentimentos.get(k, k): v for k, v in sentimentos.items()
                    }
                    sentimentos_por_ano[ano] = sentimentos_traduzidos
                else:
                    print(f"Não foi possível analisar sentimentos para o ano {ano}.")
            else:
                print(f"Pulando análise de sentimentos para {ano} devido a problemas na tradução.")
                sentimentos_por_ano[ano] = {}

        print("\n=== GERANDO VISUALIZAÇÕES GERAIS ===")
        todas_letras_geral = " ".join(letras_por_ano.values())
        palavras_freq_geral = self._contar_frequencia_palavras(todas_letras_geral, max_palavras=40)
        self._exibir_histograma(palavras_freq_geral, "Frequência das Palavras - Coleção Completa", "Palavras")
        self._exibir_wordcloud(palavras_freq_geral, "Nuvem de Palavras - Coleção Completa")

        texto_en_geral = self._traduzir_texto_grande(todas_letras_geral)
        sentimentos_geral = {}
        if texto_en_geral.strip():
            sentimentos_geral = self._analisar_sentimentos(texto_en_geral)
            if sentimentos_geral:
                sentimentos_traduzidos_geral = {
                    self.traducao_sentimentos.get(k, k): v for k, v in sentimentos_geral.items()
                }
                self._exibir_histograma(sentimentos_traduzidos_geral, "Frequência dos Sentimentos - Coleção Completa", "Sentimentos (PT-BR)")
                self._exibir_wordcloud(sentimentos_traduzidos_geral, "Nuvem de Sentimentos - Coleção Completa")
            else:
                print("Não foi possível gerar análise de sentimentos geral.")
        else:
            print("Pulando análise de sentimentos geral devido a problemas na tradução.")

        print("\n=== GERANDO VISUALIZAÇÕES POR ANO (TOP 6) ===")
        self._exibir_histograma_top_por_ano(
            palavras_freq_por_ano,
            "Palavras",
            "Palavras",  # Fixed: Added missing xlabel parameter
            top_n=6
        )

        self._exibir_histograma_top_por_ano(
            sentimentos_por_ano,
            "Sentimentos",
            "Sentimentos (PT-BR)",  # Fixed: Added missing xlabel parameter
            top_n=6
        )
        
        print("\n=== GERANDO VISUALIZAÇÕES CONSOLIDADAS ===")
        self._exibir_histograma_consolidado(
            palavras_freq_por_ano,
            "Palavras Mais Frequentes (Consolidado por Ano)",
            "Palavras"
        )
        
        self._exibir_histograma_consolidado(
            sentimentos_por_ano,
            "Sentimentos Mais Frequentes (Consolidado por Ano)",
            "Sentimentos"
        )

        print("\n=== ANÁLISE CONCLUÍDA ===")
        return {
            "palavras_geral": palavras_freq_geral,
            "sentimentos_geral": sentimentos_geral,
            "palavras_por_ano": palavras_freq_por_ano,
            "sentimentos_por_ano": sentimentos_por_ano,
            "total_musicas": len(musicas_data),
            "musicas_processadas": musicas_processadas
        }
        
if __name__ == "__main__":
    try:
        with open('musicas.json', 'r', encoding='utf-8') as file:
            musicas = json.load(file)
        print("Arquivo musicas.json carregado com sucesso!")
        analisador = AnalisadorMusicas()
        resultado = analisador.analisar_colecao_musicas(musicas)
        if resultado:
            print(f"\nRESUMO FINAL:")
            print(f"- Palavras mais frequentes (geral): {len(resultado['palavras_geral'])} encontradas")
            print(f"- Sentimentos detectados (geral): {len(resultado['sentimentos_geral'])} encontrados")
            print(f"- Músicas processadas: {resultado['musicas_processadas']}/{resultado['total_musicas']}")
            print(f"- Análise por ano concluída para {len(resultado['palavras_por_ano'])} anos.")
    except FileNotFoundError:
        print("Erro: Arquivo 'musicas.json' não encontrado!")
    except json.JSONDecodeError:
        print("Erro: Formato inválido no arquivo 'musicas.json'!")
    except Exception as e:
        print(f"Erro inesperado: {e}")