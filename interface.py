import tkinter as tk
from tkinter import messagebox, ttk

from banco import atualizar_produto, cadastrar_produto, excluir_produto, listar_produtos, registrar_log


produto_selecionado = None


def formatar_preco(preco):
    return f"{preco:.2f}".replace(".", ",")


def ler_formulario():
    nome = entry_nome.get().strip()
    quantidade_texto = entry_quantidade.get().strip()
    preco_texto = entry_preco.get().strip()

    if not nome:
        messagebox.showerror("Erro", "Informe o nome do produto.")
        return None

    try:
        quantidade = int(quantidade_texto)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
        return None

    if quantidade < 0:
        messagebox.showerror("Erro", "A quantidade não pode ser negativa.")
        return None

    partes_preco = preco_texto.split(",")
    preco_valido = (
        preco_texto
        and "." not in preco_texto
        and len(partes_preco) <= 2
        and partes_preco[0].isdigit()
        and (len(partes_preco) == 1 or (partes_preco[1].isdigit() and len(partes_preco[1]) <= 2))
    )

    if not preco_valido:
        messagebox.showerror(
            "Erro",
            "Preço inválido. Use somente números e vírgula, sem ponto, sem negativo e com até 2 casas decimais.",
        )
        return None

    preco = float(preco_texto.replace(",", "."))

    return nome, quantidade, preco


def limpar_formulario():
    global produto_selecionado
    produto_selecionado = None
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    botao_cadastrar.config(state=tk.NORMAL)


def cancelar_edicao():
    limpar_formulario()
    for item in tabela.selection():
        tabela.selection_remove(item)


def carregar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    for produto in listar_produtos():
        tabela.insert("", tk.END, values=(produto[0], produto[1], produto[2], formatar_preco(produto[3])))


def cadastrar():
    dados = ler_formulario()
    if dados is None:
        return

    nome, quantidade, preco = dados
    cadastrar_produto(nome, quantidade, preco)
    registrar_log(f'INSERÇÃO - Produto "{nome}" (Qtd: {quantidade}) cadastrado com sucesso.')
    limpar_formulario()
    carregar_tabela()


def selecionar_produto(event):
    global produto_selecionado
    selecionado = tabela.selection()
    if not selecionado:
        return

    valores = tabela.item(selecionado[0], "values")
    produto_selecionado = valores[0]

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[1])
    entry_quantidade.delete(0, tk.END)
    entry_quantidade.insert(0, valores[2])
    entry_preco.delete(0, tk.END)
    entry_preco.insert(0, valores[3])
    botao_cadastrar.config(state=tk.DISABLED)


def atualizar():
    if produto_selecionado is None:
        messagebox.showerror("Erro", "Selecione um produto na tabela.")
        return

    dados = ler_formulario()
    if dados is None:
        return

    nome, quantidade, preco = dados
    atualizar_produto(produto_selecionado, nome, quantidade, preco)
    registrar_log(f'ATUALIZAÇÃO - Produto "{nome}" alterado (Nova Qtd: {quantidade}, Novo Preço: {preco:.2f}).')
    limpar_formulario()
    carregar_tabela()


def excluir():
    if produto_selecionado is None:
        messagebox.showerror("Erro", "Selecione um produto na tabela.")
        return

    nome = entry_nome.get().strip()
    confirmar = messagebox.askyesno("Confirmar exclusão", "Deseja remover o produto selecionado?")
    if not confirmar:
        return

    excluir_produto(produto_selecionado)
    registrar_log(f'EXCLUSÃO - Produto "{nome}" removido do sistema.')
    limpar_formulario()
    carregar_tabela()


def iniciar_interface():
    global janela, entry_nome, entry_quantidade, entry_preco, tabela, botao_cadastrar

    janela = tk.Tk()
    janela.title("Mini Sistema de Controle de Estoque")
    janela.geometry("720x430")

    frame_formulario = tk.Frame(janela)
    frame_formulario.pack(padx=10, pady=10, fill="x")

    tk.Label(frame_formulario, text="Nome:").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(frame_formulario, width=35)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Quantidade:").grid(row=1, column=0, sticky="w")
    entry_quantidade = tk.Entry(frame_formulario, width=15)
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_formulario, text="Preço:").grid(row=2, column=0, sticky="w")
    entry_preco = tk.Entry(frame_formulario, width=15)
    entry_preco.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(padx=10, pady=5, fill="x")

    botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar)
    botao_cadastrar.pack(side="left", padx=3)
    tk.Button(frame_botoes, text="Salvar Alteração", command=atualizar).pack(side="left", padx=3)
    tk.Button(frame_botoes, text="Excluir", command=excluir).pack(side="left", padx=3)
    tk.Button(frame_botoes, text="Cancelar edição", command=cancelar_edicao).pack(side="left", padx=3)

    colunas = ("id", "nome", "quantidade", "preco")
    tabela = ttk.Treeview(janela, columns=colunas, show="headings")
    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("quantidade", text="Quantidade")
    tabela.heading("preco", text="Preço")
    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=320)
    tabela.column("quantidade", width=120, anchor="center")
    tabela.column("preco", width=120, anchor="center")
    tabela.pack(padx=10, pady=10, fill="both", expand=True)
    tabela.bind("<<TreeviewSelect>>", selecionar_produto)

    carregar_tabela()
    janela.mainloop()
