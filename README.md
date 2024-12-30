# Gerenciador de Tarefas com Autenticação

## Descrição

Este é um simples **Gerenciador de Tarefas** em Python, utilizando **SQLite** para persistência de dados e **Tkinter** para a interface gráfica. O sistema permite que usuários se autentiquem com login e senha, criem uma conta, adicionem, visualizem, atualizem o status e excluam tarefas. Cada usuário tem sua própria lista de tarefas privada.

## Funcionalidades

- **Autenticação de Usuário:**
  - O usuário pode se logar com uma conta existente ou criar uma nova conta.
  - Cada usuário tem seu próprio banco de tarefas privado.

- **Gerenciamento de Tarefas:**
  - O usuário pode adicionar novas tarefas com uma descrição e prazo.
  - O status das tarefas pode ser alterado entre "pendente" e "concluída".
  - O usuário pode excluir tarefas da sua lista.

- **Interface Gráfica:**
  - Interface construída com **Tkinter**.
  - Tela de login com opções para **entrar** ou **criar uma nova conta**.
  - Tela para visualizar, adicionar, atualizar e excluir tarefas de forma interativa.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Tkinter**: Biblioteca gráfica para a interface.
- **SQLite**: Banco de dados para persistência de dados.

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/gerenciador-de-tarefas.git
   cd gerenciador-de-tarefas

2. **Instale as dependências:** Se ainda não tiver o Python instalado, instale a versão mais recente. Este projeto não exige dependências externas além do próprio Python.
 
3. **Execute o código:**

 ```bash

  python main.py
```

4. **Uso.:**

 - Na tela de login, você pode **entrar** com um usuário já registrado ou **criar uma nova conta**
 - Após logar, será possível **adicionar tarefas, alterar o status** (de "pendente" para "concluída"), e **excluir tarefas** da sua lista.

## Estrutura do Banco de Dados

O banco de dados utiliza uma tabela para armazenar os usuários (`usuarios`) e outra para armazenar as tarefas (`tarefas`). Cada tarefa é associada a um usuário via o campo `user_id`.

### **Tabela de Usuários (`usuarios`)**

- `id` (INTEGER, PRIMARY KEY): ID único do usuário.
- `username` (TEXT, UNIQUE, NOT NULL): Nome de usuário único.
- `password` (TEXT, NOT NULL): Senha do usuário.

### **Tabela de Tarefas (`tarefas`)**

- `id` (INTEGER, PRIMARY KEY): ID único da tarefa.
- `descricao` (TEXT, NOT NULL): Descrição da tarefa.
- `status` (TEXT, CHECK(status IN ('pendente', 'concluida'))): Status da tarefa, podendo ser "pendente" ou "concluída".
- `prazo` (DATE): Data de vencimento da tarefa.
- `user_id` (INTEGER, FOREIGN KEY): ID do usuário ao qual a tarefa pertence.

## Funcionalidades Futuras

- **Adicionar categorias para tarefas**.
- **Enviar notificações para tarefas vencidas**.
- **Aprimorar a interface com mais recursos visuais**.

## Contribuição

Sinta-se à vontade para fazer um fork deste repositório e enviar suas contribuições. Se encontrar algum problema ou tiver sugestões de melhorias, abra uma **issue** ou envie um **pull request**!

