# FTC - Projeto Final: Análise de Dados + Dashboard no Streamlit

![fomezero](https://github.com/ctosta/Application-Data-Analysis/assets/84297748/d6983dc1-d70d-40fb-9c86-48f7054486a5)

# 1. Problema de Negócios
# 1.1. Sobre a empresa
Com o propósito de aplicar os conhecimentos adquiridos durante o curso de Python da ComunidadeDS, o seguinte cenário aborda a busca por uma solução para um problema fictício de uma empresa.

A FomeZero é uma empresa de tecnologia que, por meio de seus serviços, permite aos usuários encontrar uma variedade de estabelecimentos gastronômicos, como restaurantes, cafeterias e bares, além de fornecer informações sobre esses locais e tipos de culinárias de todo o mundo. Os serviços da FomeZero inclui um aplicativo fácil de utilizar que possibilita aos usuários pesquisar estabelecimentos por localização, tipo de culinária, avaliações e classificações. A empresa gera uma vasta quantidade de dados relacionados a suas operações. 

O CEO, recém-contratado, está dedicado a aprofundar seu entendimento sobre o negócio. Portanto, para tomar decisões estratégicas mais fundamentadas e para impulsionar o crescimento da empresa, ele solicitou à equipe de Ciência de Dados uma análise abrangente dos dados da empresa e a criação de dashboards com base nessas análises, a fim de responder às seguintes questões-chave:"

### 1.1.1. Visão Geral
- Quantos restaurantes únicos estão registrados?
- Quantos países únicos estão registrados?
- Quantas cidades únicas estão registradas?
- Qual o total de avaliações feitas?
- Qual o total de tipos de culinária registrados?

### 1.1.2. Visão Pais
- Qual a quantidade de restaurantes por pais?
- Qual a quantidade de cidades avaliadas por pais?
- Qual é a quantidade de avaliações feitas por pais?
- Qual a média de preço por um prato para duas pessoas
- Quais são os paises que posuem as melhores médias de avaliações
- Quais são os paises que posuem os piores médias de avaliações

### 1.1.3. Visão Cidades
- Quais são as cidades que mais possuem restaurantes?
- Quais são as cidades que tem sua avaliação média acima de 4?
- Quais são as cidades que tem sua avaliação média menor que 2?
- Quais são as cidades que tem a maior quantidade de culinárias?

### 1.1.4. Visão Culinária
- Quais são os melhores restaurantes dos principais tipos de culinárias?
- Quais são os melhores restaurantes?
- Quais são os melhores tipos de culinárias?
- Quais são os piores tipos de culinárias?

## 1.2. Sobre os dados

Os dados foram obtidos no [Kaggle](https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data). As variáveis presentes no conjunto de dados são apresentas abaixo:

Variável | Descrição
---------|------------
Restaurant Id | ID exclusivo de cada restaurante em várias cidades do mundo
Restaurant Name |  nome do restaurante
Country Code | país em que o restaurante está localizado
City | cidade em que o restaurante está localizado
Address | endereço do restaurante
Locality | localização na cidade
Locality Verbose | descrição detalhada da localidade
Longitude | coordenada longitudinal da localização do restaurante
Latitude | coordenada latitude da localização do restaurante
Cuisines | cozinhas oferecidas pelo restaurante
Average Cost for two | custo para dois pessoas em moedas diferentes
Currency | moeda do país
Has Table booking | sim/não
Has Online delivery | sim/não
Is delivering | sim/não
Switch to order menu | sim/não
Price range | faixa de preço da comida
Aggregate Rating | classificação média em 5
Rating color | dependendo da cor da classificação média
Rating text | texto com base na classificação da classificação
Votes | número de classificações feitas por pessoas

# 2. Premissas de Negócios

- A empresa busca soluções de dados para compreensão de suas operações;

- O modelo de negócio assumido foi marketplace;

- Os códigos atualmente presentes na variável `country_code` serão substituídos pelos nomes dos países correspondentes;

- Dado que existem registros de estabelecimentos em todo o país, será desenvolvida uma função de conversão de moeda, para converter os valores em dólares na variável `average_cost_for_two`, considerando a cotação vigente na data da análise;

- Na variável `price_range`, que representa os diferentes níveis de faixa de preço para a comida, serão aplicados os seguintes parâmetros: 1: Cheap, 2: Nomal, 3: Expensive, 4: Gourmet.

# 3. Estratégia de Solução

 - Para apresentar as informações solicitadas na visão geral, será incorporada uma barra lateral fixa no dashboard;

- Quanto às seguintes visões: países, cidades e culinárias, cada uma delas será representada por uma aba no dashboard, contendo um conjunto de gráficos e/ou tabelas para apresentar as métricas de maneira eficaz ao CEO;

- Dado que o conjunto de dados contém informações sobre os endereços de cada estabelecimento, uma nova visão (**Restaurantes**) será adicionada ao dashboard um mapa para exibir a localização geográfica dos estabelecimentos. Além de apresentar os tops restaurantes de cada país, organizados numa tabela, de acordo com a quantidade especificada pelo usuário.

# 4. Top 3 Insights de Dados

# 5. O Produto Final do Projeto

# 6. Conclusão

# 7. Próximos Passos

