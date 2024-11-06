import streamlit as st
from utils.auth import check_login

check_login()

# Título da página
st.title("Documentação do Tratamento de Dados de Web Scraping - HUBBI")

# Texto em Markdown
markdown_text = """

## Objetivo
O objetivo dessa documentação é descrever como deve ficar o documento ao final do tratamento dos dados, bem como servir como um norte para entender o que precisa ser feito caso ocorra algum erro durante o processo de validação dos dados.

## Nomeação das colunas ao final do tratamento dos dados
- É fortemente recomendado que o nome das colunas no seu documento seja o mesmo nome dos campos do modelo;
- Dito isso, os nomes recomendados seriam:
- `manufacturer_ref` para o código do produto (OBRIGATÓRIO);
- `name` para o nome do produto (OBRIGATÓRIO);
- `application` para os carros onde a peça pode ser usada (OBRIGATÓRIO);
- `brand` nome da marca do fabricante da peça (OBRIGATÓRIO);
- `ncm` para o código do produto usado no Mercosul;
- `barcode` para o código de barras;
- `gross_weight`, `net_weight` para o peso bruto e peso líquido respectivamente;
- `width`, `depth`, `height` para largura, comprimento e altura respectivamente;
- `ipi` para imposto sobre importação;
- `born_at`, `deprecated_at` para os anos que uma peça começa a ser usada e termina de ser usada respectivamente;
- `search_ref` para o código que a peça terá para pesquisa interna;
- `notes` para as informações que não foram ditas como colunas, informações de dimensão precisam estar em notes;

### Observações
Algumas informações que não foram citadas como códigos de peças similares a que está sendo tratada devem ter sua coluna própria para uso futuro.
Além disso, será necessária uma coluna para o links das imagens do produto.
A partir dos campos obrigatórios para subir uma peça, outros campos estarão presentes na peça ao colocar a peça no banco de dados. Esses campos são `born_at`, `deprecated_at` e `search_ref`.

## Formatação e verificações nas colunas por tipos

Para que os dados sejam carregados no banco de dados, é necessário que as informações estejam padronizadas. 

### Colunas do tipo string

Para as colunas do tipo string, caso alguma informação não esteja presente em algum registro, deve ser usado `df.column_name.fillna('')`.

Nessas colunas as informações não devem conter letras minúsculas.
Para esse caso, pode-se rodar o seguinte código para verificar essa possibilidade:
- `df.column_name.apply(lambda string: bool(re.findall(pattern=r'[a-z], string)))`;
- O código irá retornar quais linhas possuem algum caractere que esteja minúsculo;
- Para resolver, basta executar `df.column_name.apply(lambda string: string.upper() if isinstance(string, str) else string`.
- É interessante que, para as colunas do tipo string, seja verificado se existe algum erro de codificação. Como uma sugestão de verificação, mas que não existe a garantia de encontrar todos os erros de codificação, seria passar a string para a seguinte função usando a função auxiliar para checar se existe erro de codificação de latin1:
```python
def has_invalid_latin1(string):
    # Define the regex pattern to match valid Latin-1 characters
    latin1_pattern = re.compile(r'[\x00-\xFF]')
    
    # Find all matches of valid Latin-1 characters
    valid_characters = re.findall(latin1_pattern, string)
    
    # Reconstruct the string from the matches
    valid_latin1_string = ''.join(valid_characters)
    
    # Find invalid characters by comparing the original string to the valid one
    invalid_characters = [c for c in string if c not in valid_latin1_string]
    
    # Check if there are any invalid characters
    has_invalid = bool(invalid_characters)
    
    return has_invalid, invalid_characters


def has_invalid_utf8(string):
    utf8_pattern =  re.compile(r'[\x00-\x7F]|[\xC2-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF4][\x80-\xBF]{3}')
    invalid_characters = list(filter(lambda c: len(c) > 1, re.findall(utf8_pattern, string)))
    invalid_latin1 = has_invalid_latin1(string)
    if invalid_latin1[0]:
        invalid_latin1[1].extend(invalid_characters)
        return invalid_latin1[0], invalid_latin1[1]
    return (bool(invalid_characters), invalid_characters)
```
Essa função verifica se existe algum caractere na string que está fora do range do UTF-8. Se for o caso, retorna uma tupla onde o primeiro elemento é true e o segundo é a lista dos caracteres invalidos. Caso contrário, o primeiro elemento é false e o segundo uma lista vazia.

### Colunas do tipo float

As colunas que devem ser do tipo float, como dimensões e pesos, devem estar no padrão internacional de medidas. Nesse caso, as medidas devem estar em metros e o peso deve estar em quilos.

Note que, mesmo que a quantidade majoritária dos valores estejam em alguma medida, medidas em cm por exemplo, pode ser o caso de pelo menos um produto tenha alguma medida em mm.
Isso pode ser identificado pelo processo natural do tratamento onde precisa converter os dados para float.
O float tem que ter a separação de decimal como ponto e os 0, `1.0` deve ser descartado.
Se as dimensões não estejam identificadas como `height`, `width` ou `depth`, as atribuições, do maior para o menor, seria `depth`, `width` e `height`.
**Observação**: É importante checar se `gross_weight` é maior do que `net_weight`.

### Colunas do tipo int

Sendo apenas `born_at` e `deprecated_at`, a verificação necessária seria apenas se o primeiro é menor do que o segundo e se algum deles não é maior do que o ano atual.

## Formatação e verificação individuais

### Manufacturer_ref

Existir o valor para essa coluna é imprescindível. Caso não exista, a peça não irá ser colocada no banco de dados.

### Brand

A marca deve estar em maiúsculo e sem acentos ou 'ç'.

**Observação**: É extremamente necessário que as marcas estejam padronizadas para que uma mesma marca, já presente no banco de dados, não seja considerada outra por alguma variação no nome.

### Name

--

### NCM

No NCM é necessário que esteja no seguinte padrão:
- Se NCM já for string, checar se está no padrão `r'\d{4}\.\d{2}\.\d{2}'`;
- Se não estiver nesse padrão, verificar os casos que não estão nesse padrão;
- Se NCM não for string, tentar converter para o padrão descrito no primeiro ponto caso a quantidade de digitos seja igual a 8.

### Barcode

Checar se o barcode tem um limite de 13 caracteres, seguindo o padrão brasileiro EAN-13.
Em algumas instâncias no banco de dados o barcode está com um sufixo ".0". Esse sufixo deve ser retirado.

### Gross weight e net weight

Se a peça que está sendo tratada possui apenas um peso, o peso deve ser gross_weight e o net_weight vai ser considerado 0.
Caso contrário, o maior irá ficar como gross_weight e o menor o net_weight.

### Width, depth, height

--

### IPI

O IPI deve ser um valor entre 0 e 1.

### Application

Verificar pela existência de substrings como 'NAO VEICULAR', 'UNIVERSAL' e 'FORA DA FROTA BRASILEIRA'.Essas substrings não devem estar presente no application.
A partir da coluna application que as colunas born_at e deprecated_at são criadas.

### Notes

Checar pela existência de None literal e 'None'.

## Observações

### Informações de certas colunas presentes em outras colunas

Seria importante checar se as informações estão em algum padrão para que sejam identificadas informações em locais incorretos.

## Boas Práticas para o Tratamento de Dados

Ao realizar o tratamento de dados, é importante seguir algumas boas práticas para garantir a qualidade e eficiência do processo. Algumas delas incluem:

- **Nomear as Colunas Tratadas**: Caso a coluna possua mais de um item, como img_link com várias imagens, deixar o nome no plural. É obrigatório que o nome das colunas no final do tratamento fique igual ao nome das colunas no banco de dados.

- **Extração de Informações**: Quando temos uma coluna com várias informações, podemos usar técnicas como expressões regulares (regex), dicionários ou até mesmo a biblioteca Beautiful Soup para extrair os dados e criar novas colunas com informações específicas.

## Exemplo


```python
import pandas as pd

dados = {
    'description': ['nan'],
    'name': ['CABO RCA'],
    'manufacturer_ref': ['78'],
    'brand': ['PERMAK'],
    'link': ['/78/p'],
    'img_link': [['https://tezmnnsk2.vtexassets.com/arquivos/ids/337336/78_1.jpg?v=638393321819070000', 'https://tezmnnsk2.vtexassets.com/arquivos/ids/307481/CABO-RCA.jpg?v=638173555407000000']],
    'barcode': ['7898253495987'],
    'ncm': ['8708.99.90'],
    'posicao': ['DIANTEIRO'],
    'applications': ['MERCEDES BENZ-710-4.0 L 8V SOHV L4 1995/2019\nMERCEDES BENZ-914 C-4.3 L 12V SOHV L4 1999/2004\nMERCEDES BENZ-LO 712-4.0 L 8V SOHV L4 2003/2012\nMERCEDES BENZ-L 610 A-3.8 L 8V SOHC L4 1984/1985\nMERCEDES BENZ-712 C-4.3 L 12V SOHV L4 1999/2004\nMERCEDES BENZ-LO 812-4.0 L 8V SOHV L4 1988/2012\nMERCEDES BENZ-712-4.0 L 8V SOHV L4 1996/1999\nMERCEDES BENZ-LO 914-4.3 L 12V SOHV L4 1999/2006\nMERCEDES BENZ-LO 610-4.0 L 8V SOHV L4 2001/2003\nMERCEDES BENZ-912-4.0 L 8V SOHV L4 1988/1996\nMERCEDES BENZ-914-4.0 L 8V SOHV L4 1994/1999\nMERCEDES BENZ-OF 809-4.0 L 8V SOHV L4 1996/1996\nMERCEDES BENZ-L 608 D-3.8 L 8V SOHV L4 1972/1987'],
    'born_at': [1972.0],
    'deprecated_at': [2019.0],
    'gross_weight': [0.42],
    'net_weight': ['nan'],
    'depth': [0.068],
    'height': [0.133],
    'width': [0.068],
    'notes': ['INFORMAÇÕES ADICIONAIS: COM PINO\nPRAZO GARANTIA: 3\n'],
    'search_ref': ['78']
}

df = pd.DataFrame(dados)

df

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>description</th>
      <th>productName</th>
      <th>productReference</th>
      <th>brand</th>
      <th>link</th>
      <th>img_link</th>
      <th>ean</th>
      <th>ncm</th>
      <th>posicao</th>
      <th>aplicacoes_ok</th>
      <th>menor_ano</th>
      <th>maior_ano</th>
      <th>peso_bruto</th>
      <th>peso_liquido</th>
      <th>comprimento</th>
      <th>altura</th>
      <th>largura</th>
      <th>notes</th>
      <th>search_ref</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nan</td>
      <td>CABO RCA</td>
      <td>78</td>
      <td>PERMAK</td>
      <td>/78/p</td>
      <td>[https://tezmnnsk2.vtexassets.com/arquivos/ids...</td>
      <td>7898253495987</td>
      <td>8708.99.90</td>
      <td>DIANTEIRO</td>
      <td>MERCEDES BENZ-710-4.0 L 8V SOHV L4 1995/2019\n...</td>
      <td>1972.0</td>
      <td>2019.0</td>
      <td>0.42</td>
      <td>nan</td>
      <td>0.068</td>
      <td>0.133</td>
      <td>0.068</td>
      <td>INFORMAÇÕES ADICIONAIS: COM PINO\nPRAZO GARANT...</td>
      <td>78</td>
    </tr>
  </tbody>
</table>
</div>




## Códigos e Funções Úteis para o Tratamento de Dados

Nesta seção, apresentaremos alguns códigos e funções que podem ser úteis durante o tratamento de dados com Pandas.


#### Extrair Anos

```python
import re

def extrair_anos(info):
    anos = re.findall(r'\b\d{4}\b', info)
    anos = [int(ano) for ano in anos if 1900 <= int(ano) <= 2100]
    if len(anos) == 0:
        return None, None
    elif len(anos) == 1:
        return anos[0], anos[0]
    return min(anos), max(anos)

df[['menor_ano', 'maior_ano']] = df['aplicacoes'].apply(lambda x: pd.Series(extrair_anos(str(x))))
```

#### SEARCH_REF A PARTIR DO PRODUCT_REF

```python
df['search_ref'] = df['productReference'].map(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x))
```

#### FUNÇÃO PARA COMPRIMIR TODAS AS COLUNAS EM EXCESSO PARA UMA ÚNICA COLUNA (NOTES)

```python
colunas_notes = [col for col in df.columns if col not in colunas]

def generate_notes(row,colunas_notes):
    notes = ""

    for coluna in colunas_notes:
        dados = row[coluna]
        if str(dados) == 'nan':
            continue
        
        tipo_dado = coluna.replace('_', ' ')
        notes += f"{tipo_dado}: {dados}\n"

    return notes.rstrip('\n')

df['NOTES'] = df.apply(lambda row: generate_notes(row, colunas_notes), axis=1)
```

### Funções do Pandas mais utilizadas no nosso tratamento

#### Ler Arquivo
```python
df = pd.read_csv('arquivo.csv')
```

#### Drop Duplicates
```python
df = df.drop_duplicates(subset=['coluna'])
```

#### Salvar Arquivo
```python
df.to_csv('novo_arquivo.csv', index=False)
```

#### Columns to List
```python
lista_colunas = df.columns.tolist()
```

### Outras Funções Úteis

#### Renomear Colunas
```python
df.rename(columns={'coluna_antiga': 'coluna_nova'}, inplace=True)
```

#### Filtrar Linhas com Base em uma Condição
```python
df_filtrado = df[df['coluna'] > 10]
```

#### Adicionar Nova Coluna com Base em Outras Colunas
```python
df['nova_coluna'] = df['coluna1'] + df['coluna2']
```

#### Transformar dicionário para string

```python
def dict_to_string(dictionary, separator='\n'):
    if isinstance(dictionary, float) or dictionary == None: return ''
    return f'{separator}'.join([f'{key}: {value}' for key, value in dictionary.items()])
```


#### Construir dicionário a partir de uma string separada por \n onde chaves terminam em :

```python
def construct_dict(data):
    if data == None or isinstance(data, float): return ''
    result = {}
    current_key = None
    current_value = []

    for line in data:
        # Its key of the dict
        if line.endswith(':'):
            # First key encounter
            if current_key is not None:
                result[current_key] = current_value
                current_value = []
            elif current_key is None and current_value != []:
                result['dummy'] = current_value
                current_value = []
            current_key = unidecode(line.rstrip(':').lower().replace(' ', '_'))
        # The following elements not ended with : are values to the current key
        else:
            value = line.strip(';.- ')
            current_value.append(value)

    # Last list of values
    if current_key is not None:
        result[current_key] = current_value

    if current_key == None and current_value != []:
        result['dummy'] = current_value

    return result
```

#### Ajuste da coluna posições.

```python
def map_values(posicao:str):
    posicao_tratada = ""
    posicao = posicao.upper().strip() if pd.notna(posicao) else ""
    if 'DIANTEIRO' in posicao:
        posicao_tratada += " "+'DIANTEIRO'
    if 'TRASEIRO' in posicao:
        posicao_tratada += " "+'TRASEIRO'
    if 'INFERIOR' in posicao:
        posicao_tratada += " "+'INFERIOR'
    if 'SUPERIOR' in posicao:
        posicao_tratada += " "+'SUPERIOR'
    if 'ESQUERDO' in posicao:
        posicao_tratada += " "+'LADO ESQUERDO'
    if 'DIREITO' in posicao:
        posicao_tratada += " "+'LADO DIREITO'

    return posicao_tratada.strip() if posicao_tratada else None
```

## Considerações Finais
Esta documentação fornece uma visão geral do processo de tratamento de dados de web scraping para inserção em um banco de dados. É importante seguir as melhores práticas de manipulação de dados e garantir a integridade e precisão dos dados em todas as etapas do processo.

"""

# Exibindo o texto em Markdown
st.markdown(markdown_text)
