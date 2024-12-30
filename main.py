import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Banco de Dados: Inicializar
def inicializar_banco():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Verifica se a tabela tarefas já possui a coluna user_id, se não, faz a correção
    corrigir_tabela()

    conn.commit()
    conn.close()

# Função para corrigir a estrutura da tabela tarefas
def corrigir_tabela():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()

    # Verifica se a coluna user_id existe na tabela tarefas
    cursor.execute("PRAGMA table_info(tarefas)")
    colunas = [col[1] for col in cursor.fetchall()]

    if 'user_id' not in colunas:
        # Se não existir, cria uma nova tabela com a coluna user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                status TEXT CHECK(status IN ('pendente', 'concluida')) DEFAULT 'pendente',
                prazo DATE,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES usuarios(id)
            )
        ''')

        # Copiar os dados da tabela antiga para a nova
        cursor.execute('''
            INSERT INTO tarefas_temp (id, descricao, status, prazo)
            SELECT id, descricao, status, prazo FROM tarefas
        ''')

        # Excluir a tabela antiga
        cursor.execute('DROP TABLE tarefas')

        # Renomear a tabela nova
        cursor.execute('ALTER TABLE tarefas_temp RENAME TO tarefas')

        conn.commit()

    conn.close()

# Autenticação
def login(username, password):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def criar_usuario(username, password):
    try:
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Funções de Tarefa
def adicionar_tarefa(descricao, prazo, user_id):
    if descricao.strip() == "":
        return False  # Descrição não pode ser vazia

    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (descricao, prazo, user_id) VALUES (?, ?, ?)", (descricao, prazo, user_id))
    conn.commit()
    conn.close()
    return True

def listar_tarefas(user_id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE user_id = ?", (user_id,))
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

def atualizar_tarefa(tarefa_id, status, user_id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = ? WHERE id = ? AND user_id = ?", (status, tarefa_id, user_id))
    conn.commit()
    conn.close()

def excluir_tarefa(tarefa_id, user_id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ? AND user_id = ?", (tarefa_id, user_id))
    conn.commit()
    conn.close()

# Interface Gráfica: Login
def exibir_tela_login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f8ff")

    def fazer_login():
        username = username_entry.get()
        password = password_entry.get()
        user_id = login(username, password)
        if user_id:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            login_window.destroy()
            exibir_tela_tarefas(user_id)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def criar_conta():
        username = username_entry.get()
        password = password_entry.get()
        if criar_usuario(username, password):
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
        else:
            messagebox.showerror("Erro", "Usuário já existe!")

    tk.Label(login_window, text="Usuário:", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Senha:", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 14))
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Entrar", command=fazer_login, font=("Arial", 12)).pack(pady=10)
    tk.Button(login_window, text="Criar Conta", command=criar_conta, font=("Arial", 12)).pack(pady=10)

# Interface Gráfica: Tarefas
def exibir_tela_tarefas(user_id):
    tarefas_window = tk.Toplevel(root)
    tarefas_window.title("Gerenciador de Tarefas")
    tarefas_window.geometry("800x600")
    tarefas_window.configure(bg="#f0f8ff")

    def adicionar_tarefa_gui():
        descricao = descricao_entry.get()
        prazo = prazo_entry.get()
        if not adicionar_tarefa(descricao, prazo, user_id):
            messagebox.showwarning("Aviso", "A descrição não pode ser vazia!")
        atualizar_lista_tarefas()

    def atualizar_lista_tarefas():
        for item in tarefas_tree.get_children():
            tarefas_tree.delete(item)
        tarefas = listar_tarefas(user_id)
        for tarefa in tarefas:
            tarefas_tree.insert("", "end", values=tarefa)

    def atualizar_status_gui():
        try:
            selected_item = tarefas_tree.selection()[0]
            tarefa_id = tarefas_tree.item(selected_item, "values")[0]
            novo_status = "concluida" if status_var.get() == 1 else "pendente"
            atualizar_tarefa(tarefa_id, novo_status, user_id)
            atualizar_lista_tarefas()
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada!")

    def excluir_tarefa_gui():
        try:
            selected_item = tarefas_tree.selection()[0]
            tarefa_id = tarefas_tree.item(selected_item, "values")[0]
            excluir_tarefa(tarefa_id, user_id)
            atualizar_lista_tarefas()
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada!")

    tk.Label(tarefas_window, text="Descrição:", bg="#f0f8ff", font=("Arial", 14)).grid(row=0, column=0, pady=10)
    descricao_entry = tk.Entry(tarefas_window, width=30, font=("Arial", 12))
    descricao_entry.grid(row=0, column=1)

    tk.Label(tarefas_window, text="Prazo:", bg="#f0f8ff", font=("Arial", 14)).grid(row=1, column=0, pady=10)
    prazo_entry = tk.Entry(tarefas_window, width=30, font=("Arial", 12))
    prazo_entry.grid(row=1, column=1)

    tk.Button(tarefas_window, text="Adicionar Tarefa", command=adicionar_tarefa_gui, font=("Arial", 12)).grid(row=2, column=0, columnspan=2)

    tarefas_tree = ttk.Treeview(tarefas_window, columns=("ID", "Descrição", "Status", "Prazo"), show="headings")
    tarefas_tree.heading("ID", text="ID")
    tarefas_tree.heading("Descrição", text="Descrição")
    tarefas_tree.heading("Status", text="Status")
    tarefas_tree.heading("Prazo", text="Prazo")
    tarefas_tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

    status_var = tk.IntVar()
    tk.Radiobutton(tarefas_window, text="Concluída", variable=status_var, value=1, bg="#f0f8ff").grid(row=4, column=0)
    tk.Radiobutton(tarefas_window, text="Pendente", variable=status_var, value=0, bg="#f0f8ff").grid(row=4, column=1)

    tk.Button(tarefas_window, text="Atualizar Status", command=atualizar_status_gui, font=("Arial", 12)).grid(row=5, column=0, columnspan=2)
    tk.Button(tarefas_window, text="Excluir Tarefa", command=excluir_tarefa_gui, font=("Arial", 12)).grid(row=6, column=0, columnspan=2)

    atualizar_lista_tarefas()

# Inicializar Banco e Janela Principal
inicializar_banco()

root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("400x200")
root.configure(bg="#f0f8ff")

tk.Button(root, text="Login", command=exibir_tela_login, font=("Arial", 14)).pack(pady=50)

root.mainloop()
