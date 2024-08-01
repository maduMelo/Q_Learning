# Q_Learning

Esse é um projeto desenvolvido para aplicar o algoritmo de aprendizado de máquina Q-learning, com o objetivo de treinar um agente a percorrer um ambiente e encontrar o caminho ideal até uma recompensa.

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Bibliotecas**:
  - `numpy`: Para manipulação da `q_table`
  - `pyautogui`: Para simular o pressionamento das teclas do teclado, controlando o agente no ambiente
  - `time`: Para gerenciar intervalos de tempo entre as ações do agente

## Estrutura do Projeto

```
Q_Learning/
│── windows/
│── .gitignore
│── client.py
│── connection.py
│── instrucoes.pdf
|── q_agent.py
│── README.md
│── resultado.txt
│── strategy.py
```

- [**.gitignore**](.gitignore): Define arquivos e diretórios a serem ignorados pelo Git, incluindo `__pycache__/`.
- [**connection.py**](connection.py): Estabelece a conexão via sockets com o servidor do ambiente simulado.
- [**q_agent.py**](q_agent.py): Contém a classe do agente Q Learning, incluindo métodos para atualização da `q_table`, cálculo de taxas de aprendizado e exploração.
- [**strategy.py**](strategy.py): Define a estratégia de movimentação do agente, incluindo a sequência de comandos do teclado e a lógica para seleção de plataformas iniciais.
- [**client.py**](client.py): Principal script de execução, configurando variáveis de treinamento e iniciando o loop de aprendizado.
- [**resultado.txt**](resultado.txt): Armazena a `q_table` resultante do processo de aprendizado.
- [**instrucoes.pdf**](instrucoes.pdf): Documentação detalhada dos requisitos e especificações do projeto.

**OBS.:** Os arquivos `connection.py` e `instrucoes.pdf` e o conteúdo do diretório `windows/` não são de autoria desse repositório e foram disponibilizados para aplicação do algoritmo de aprendizado de máquina.

## Instruções para Execução

1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/maduMelo/Q_Learning.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd Q_Learning
   ```
3. No terminal, instale as dependências necessárias:
   ```bash
   pip install numpy pyautogui
   ```
2. Navegue até a pasta "windows" no repositório e execute o arquivo "Aprendizado por reforço".
4. Execute o projeto:
   ```bash
   python client.py
   ```

## Personalização

Para personalizar o comportamento do agente ou o processo de aprendizado, edite as variáveis no arquivo [client.py](client.py).