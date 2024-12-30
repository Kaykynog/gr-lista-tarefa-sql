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
