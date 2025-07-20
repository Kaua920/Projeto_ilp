import random
import os
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Configurações da Loteria ---
QUANTIDADE_NUMEROS_LOTERIA = 6
NUMERO_MINIMO_LOTERIA = 1
NUMERO_MAXIMO_LOTERIA = 60
ARQUIVO_APOSTAS = "apostas_loteria.txt"
ARQUIVO_SORTEIOS = "sorteios_loteria.txt"

# --- Funções Lógicas do Simulador (as mesmas que você já tinha) ---

def gerar_numeros_sorteio(quantidade=QUANTIDADE_NUMEROS_LOTERIA, min_num=NUMERO_MINIMO_LOTERIA, max_num=NUMERO_MAXIMO_LOTERIA):
    if quantidade > (max_num - min_num + 1):
        return [] # Retorna vazio ou trata o erro de outra forma
    numeros_sorteados = set()
    while len(numeros_sorteados) < quantidade:
        numeros_sorteados.add(random.randint(min_num, max_num))
    return sorted(list(numeros_sorteados))

def comparar_numeros(numeros_sorteados, aposta_usuario):
    numeros_acertados = set(numeros_sorteados).intersection(set(aposta_usuario))
    acertos = len(numeros_acertados)
    return acertos, sorted(list(numeros_acertados))

def registrar_dados_em_arquivo(caminho_arquivo, dados):
    try:
        with open(caminho_arquivo, 'a', encoding='utf-8') as arquivo:
            arquivo.write(dados + '\n')
    except IOError as e:
        messagebox.showerror("Erro de Arquivo", f"Erro ao registrar dados no arquivo '{caminho_arquivo}': {e}")

def ler_dados_do_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.readlines()
    except IOError as e:
        messagebox.showerror("Erro de Arquivo", f"Erro ao ler dados do arquivo '{caminho_arquivo}': {e}")
        return []

# --- Funções da Interface Gráfica ---

class LoteriaApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Loteria")
        master.geometry("500x700") # Define o tamanho inicial da janela
        master.resizable(False, False) # Impede redimensionamento

        self.setup_ui()

    def setup_ui(self):
        # Frame para entrada dos números da aposta
        self.frame_aposta = tk.LabelFrame(self.master, text="Sua Aposta", padx=10, pady=10)
        self.frame_aposta.pack(pady=10, padx=10, fill="x")

        self.entry_numeros = []
        for i in range(QUANTIDADE_NUMEROS_LOTERIA):
            label = tk.Label(self.frame_aposta, text=f"Número {i+1}:")
            label.grid(row=i // 3, column=(i % 3) * 2, padx=5, pady=2, sticky="w")
            entry = tk.Entry(self.frame_aposta, width=5)
            entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=2, sticky="ew")
            self.entry_numeros.append(entry)

        # Botão para sortear e verificar
        self.btn_sortear = tk.Button(self.master, text="Fazer Aposta e Sortear", command=self.fazer_aposta_e_sortear)
        self.btn_sortear.pack(pady=10)

        # Frame para resultados
        self.frame_resultados = tk.LabelFrame(self.master, text="Resultados do Sorteio", padx=10, pady=10)
        self.frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

        self.label_sorteados = tk.Label(self.frame_resultados, text="Números Sorteados: ", wraplength=450, justify="left")
        self.label_sorteados.pack(pady=5, anchor="w")

        self.label_sua_aposta = tk.Label(self.frame_resultados, text="Sua Aposta: ", wraplength=450, justify="left")
        self.label_sua_aposta.pack(pady=5, anchor="w")

        self.label_acertos = tk.Label(self.frame_resultados, text="Acertos: ")
        self.label_acertos.pack(pady=5, anchor="w")

        self.label_numeros_acertados = tk.Label(self.frame_resultados, text="Números Acertados: ", wraplength=450, justify="left")
        self.label_numeros_acertados.pack(pady=5, anchor="w")

        # Frame para histórico
        self.frame_historico = tk.LabelFrame(self.master, text="Histórico", padx=10, pady=10)
        self.frame_historico.pack(pady=10, padx=10, fill="x")

        self.btn_ver_apostas = tk.Button(self.frame_historico, text="Ver Histórico de Apostas", command=lambda: self.exibir_historico_gui(ARQUIVO_APOSTAS, "Histórico de Apostas"))
        self.btn_ver_apostas.pack(side="left", expand=True, padx=5, pady=5)

        self.btn_ver_sorteios = tk.Button(self.frame_historico, text="Ver Histórico de Sorteios", command=lambda: self.exibir_historico_gui(ARQUIVO_SORTEIOS, "Histórico de Sorteios"))
        self.btn_ver_sorteios.pack(side="right", expand=True, padx=5, pady=5)

    def fazer_aposta_e_sortear(self):
        aposta_usuario = set()
        for i, entry in enumerate(self.entry_numeros):
            try:
                numero = int(entry.get())
                if NUMERO_MINIMO_LOTERIA <= numero <= NUMERO_MAXIMO_LOTERIA and numero not in aposta_usuario:
                    aposta_usuario.add(numero)
                elif numero in aposta_usuario:
                    messagebox.showwarning("Aposta Inválida", f"O número {numero} já foi escolhido. Números devem ser únicos.")
                    return
                else:
                    messagebox.showwarning("Aposta Inválida", f"O número {numero} está fora do intervalo permitido ({NUMERO_MINIMO_LOTERIA}-{NUMERO_MAXIMO_LOTERIA}).")
                    return
            except ValueError:
                messagebox.showwarning("Aposta Inválida", f"Por favor, digite um número inteiro válido no campo {i+1}.")
                return

        if len(aposta_usuario) != QUANTIDADE_NUMEROS_LOTERIA:
            messagebox.showwarning("Aposta Inválida", f"Você deve digitar exatamente {QUANTIDADE_NUMEROS_LOTERIA} números.")
            return

        aposta_do_usuario_lista = sorted(list(aposta_usuario))
        numeros_do_sorteio = gerar_numeros_sorteio()

        acertos, numeros_acertados = comparar_numeros(numeros_do_sorteio, aposta_do_usuario_lista)

        # Atualiza os labels com os resultados
        self.label_sorteados.config(text=f"Números Sorteados: {numeros_do_sorteio}")
        self.label_sua_aposta.config(text=f"Sua Aposta:        {aposta_do_usuario_lista}")
        self.label_acertos.config(text=f"Você acertou {acertos} número(s)!")
        if acertos > 0:
            self.label_numeros_acertados.config(text=f"Números Acertados: {numeros_acertados}")
        else:
            self.label_numeros_acertados.config(text="Números Acertados: Nenhum")

        # Registrar dados
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro_aposta = f"DATA/HORA: {data_hora} | Aposta: {aposta_do_usuario_lista} | Acertos: {acertos} | Números Acertados: {numeros_acertados}"
        registrar_dados_em_arquivo(ARQUIVO_APOSTAS, registro_aposta)

        registro_sorteio = f"DATA/HORA: {data_hora} | Sorteio: {numeros_do_sorteio}"
        registrar_dados_em_arquivo(ARQUIVO_SORTEIOS, registro_sorteio)

        messagebox.showinfo("Sorteio Realizado", "Verifique os resultados na janela principal!")

    def exibir_historico_gui(self, caminho_arquivo, titulo):
        historico_window = tk.Toplevel(self.master) # Cria uma nova janela
        historico_window.title(titulo)
        historico_window.geometry("600x400")

        # Widget ScrolledText para exibir o conteúdo (permite rolagem)
        text_area = scrolledtext.ScrolledText(historico_window, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
        text_area.pack(padx=10, pady=10, fill="both", expand=True)

        linhas = ler_dados_do_arquivo(caminho_arquivo)
        if not linhas:
            text_area.insert(tk.END, f"Nenhum registro encontrado em '{caminho_arquivo}'.")
        else:
            for linha in linhas:
                text_area.insert(tk.END, linha) # Insere a linha no widget de texto

        text_area.config(state=tk.DISABLED) # Torna o texto não editável

# --- Inicia a Aplicação ---
if __name__ == "__main__":
    root = tk.Tk() # Cria a janela principal do Tkinter
    app = LoteriaApp(root) # Instancia a aplicação
    root.mainloop() # Inicia o loop de eventos do Tkinter (mantém a janela aberta)