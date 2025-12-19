# 📖 INFORMAÇÕES DO REPOSITÓRIO

Este repositório contém o projeto de Trabalho de Conclusão de Curso (TCC) para a graduação em Engenharia de Computação da UNIPAMPA, cujo tema é a **Análise de Políticas Públicas de Transferência de Renda Utilizando Técnicas de Ciência de Dados**. Estão disponíveis todos os arquivos necessários para a execução dos algoritmos e análises em ambientes **Jupyter Notebook** ou **Google Colab**, conforme a preferência do usuário.

Este trabalho fundamenta-se nos pilares da Ciência de Dados — estatística, computação e conhecimento de domínio — para interpretar volumes de informações e gerar *insights* analíticos estratégicos. A metodologia emprega métricas específicas e algoritmos de Aprendizado de Máquina (*Machine Learning*) para otimizar a compreensão, modelagem e visualização dos dados.

O objetivo central da pesquisa é analisar o impacto das variações do IDESE (Índice de Desenvolvimento Socioeconômico do Rio Grande do Sul) sobre o PBF (Programa Bolsa Família), permitindo avaliar como uma política pública responde a transformações socioeconômicas históricas. É relevante destacar que este repositório documenta a evolução do projeto em sua totalidade, desde as etapas exploratórias iniciais até a consolidação e apresentação dos resultados finais.ão e de extrema relavância para todos que participaram desta jornada.

## 📁 Pastas

* **.ipynb_checkpoints**: Armazena os *checkpoints* automáticos dos arquivos Jupyter Notebook, garantindo o versionamento temporário das últimas modificações realizadas durante as sessões de desenvolvimento.
* **apendices**: Contém os arquivos e scripts utilizados na consolidação e processamento dos dados apresentados no Apêndice A do documento final.
* **bolsa-dados**: Repositório de arquivos legados referentes à fase exploratória inicial da pesquisa. Inclui scripts em Python e conjuntos de dados brutos anteriores aos processos de integração e pré-processamento.
* **graficos**: Centraliza os artefatos visuais (imagens e PDFs) gerados pelas análises. Inclui mapas de distribuição geoespacial do estado do Rio Grande do Sul, gráficos de barras para análise de séries temporais, *boxplots* para verificação de dispersão, além de uma subpasta específica detalhando a clusterização de variáveis executada via algoritmo **K-Means**.
* **logs**: Armazena registros de execução e rascunhos técnicos contendo os *outputs* (saídas) gerados durante o processamento de células específicas nos notebooks.

## 📓 Notebooks

### 🧪 Aplicacao TCC I
Este notebook corresponde à entrega do projeto de TCC I. O script Python contempla as etapas iniciais de prototipagem, integrando a geração de visualizações, a execução de métodos computacionais preliminares e algoritmos para extração de estatísticas descritivas. O ambiente de desenvolvimento e execução utilizado foi o **Google Colab**.

### 📊 Aplicacao_metricas
Desenvolvido para a etapa final (TCC II), este notebook é focado na análise pós-processamento. Contém scripts voltados exclusivamente para a extração de métricas a partir de tabelas consolidadas, gerando *outputs* em console e visualizações gráficas que sustentam a análise dos resultados.

### 🚀 Aplicação_TCC_II
Este é o notebook principal da pesquisa. Nele está implementado o *pipeline* completo de Ciência de Dados, incluindo todos os blocos de código para a construção, configuração e execução dos métodos e algoritmos computacionais que fundamentam a metodologia central do trabalho.

## 📊 Tabelas

* **Resultados_grupo_unico**: Contém as métricas de desempenho obtidas após a execução dos modelos para cada combinação de variáveis, processadas sem segmentação de grupos (aplicando apenas o tratamento e remoção de *outliers*). Este arquivo serve como um *baseline* (linha de base) para comparação com os dados segmentados.

* **Resultados_melhor_k e Resultados_segundo_melhor_k**: Apresentam os indicadores de performance dos métodos computacionais aplicados aos clusters gerados pelo algoritmo **K-Means**. Estes dados permitem analisar a correlação e o comportamento das variáveis dentro de subgrupos socioeconômicos específicos.

* **TABELA_FINAL**: É o *dataset* mestre do projeto. Esta tabela consolida e unifica variáveis provenientes do IBGE, PBF, IDESE e dados populacionais do Rio Grande do Sul. É o recurso mais crítico do repositório, pois fornece os dados agregados e estruturados em séries temporais que dão suporte a todas as análises estatísticas e ao treinamento dos modelos de Aprendizado de Máquina (*Machine Learning*).
