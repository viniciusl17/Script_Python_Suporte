import tkinter as tk
from tkinter import messagebox, simpledialog, font
import os
import webbrowser
import subprocess

class SuporteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Canivetão do Suporte")
        self.root.geometry("500x750")
        self.root.resizable(False, True)\

        # Paleta de cores
        self.colors = {
            "bg": "#f0f4f8",
            "card_bg": "#ffffff",
            "text": "#003d4d",
            "header": "#005f69",
            "button": "#003B99",
            "button_text": "#ffffff",
            "border": "#e0e0e0"
        }

        self.root.configure(bg=self.colors["bg"])

        # Fontes
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=10)
        self.title_font = ("Helvetica", 12, "bold")
        self.desc_font = ("Helvetica", 9)
        self.section_font = ("Helvetica", 11, "bold")
        self.header_font = ("Helvetica", 14, "bold")

        self.create_header()
        self.create_main_frame()
        self.create_menu_cards()

    def create_header(self):
        """Cria o cabeçalho superior da janela."""
        header_frame = tk.Frame(self.root, bg=self.colors["bg"])
        header_frame.pack(fill="x", padx=25, pady=(15, 10))

        tk.Label(
            header_frame,
            text="Menu Suporte Técnico",
            font=self.header_font,
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(side="left")

        tk.Label(
            header_frame,
            text="v1.0",
            font=("Helvetica", 9),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(side="right")

    def create_main_frame(self):
        """Cria a área principal com uma barra de rolagem."""
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.columnconfigure(0, weight=1)
        
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Controla o scroll do mouse na área de canvas."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_menu_cards(self):
        """Cria e posiciona todos os cards de menu."""
        # Seção GERAL
        self.add_section("GERAL", 0)
        self.add_card("Reiniciar computador", "⏻", "Reinicia o computador imediatamente", self.reiniciar_computador, 1)
        self.add_card("Otimizar sistema", "🧹", "Limpeza e otimização do sistema", self.otimizar_sistema, 2)
        self.add_card("Flush DNS", "🌐", "Limpar cache DNS", self.flush_dns, 3)
        self.add_card("Informações de rede", "📶", "Mostra configurações de rede", self.info_rede, 4)
        self.add_card("Ping Servidor", "💻", "Testar conexão com servidor", self.ping_servidor, 5)
        self.add_card("Central de rede", "🔌", "Abrir configurações de rede", self.central_rede, 6)
        self.add_card("Gerenciador de Tarefas", "🔧", "Abrir Gerenciador de tarefas", self.gerenciador_tarefa, 7)
        self.add_card("Atividade Porta", "🚪", "Ver atividades nas Portas do Sistema", self.gerenciador_porta, 8)

        # Seção IMPRESSORAS
        self.add_section("IMPRESSORAS", 9)
        self.add_card("Instalador Universal", "📥", "Baixar programa das impressoras", self.baixar_universal, 10)
        self.add_card("Fix erro 0x0000011b", "🪛", "Corrigir erro de impressão", self.fix_erro_11b, 11)
        self.add_card("Fix erro 0x00000bcb", "🪛", "Corrigir erro de impressão", self.fix_erro_bcb, 12)
        self.add_card("Fix erro 0x00000709", "🪛", "Corrigir erro de impressão padrão", self.fix_erro_709, 13)
        self.add_card("Reiniciar spooler", "🔄", "Reinicia o serviço de impressão", self.reiniciar_spooler, 14)
        self.add_card("Dispositivos e impressoras", "💻", "Abrir gerenciador de impressoras", self.abrir_impressoras, 15)

        # Seção TESTE DE CONEXÃO
        self.add_section("TESTE DE CONEXÃO", 16)
        self.add_card("Teste de conexão", "🌐", "Abrir speedtest.net", self.teste_conexao, 17)

        # Seção SOFTWARES
        self.add_section("SOFTWARES", 18)
        self.add_card("Anota AI Desktop", "📥", "Baixar versão atualizada", self.baixar_anota_ai, 19)
        self.add_card("Impressora Anota AI", "📥", "Baixar programa de impressora", self.baixar_impressora_ai, 20)

    def add_section(self, title, row):
        """Adiciona um cabeçalho de seção."""
        section_label = tk.Label(
            self.scrollable_frame,
            text=title.upper(),
            font=self.section_font,
            fg=self.colors["header"],
            bg=self.colors["bg"],
            anchor="w"
        )
        section_label.grid(row=row, column=0, sticky="ew", padx=25, pady=(15, 5))

    def add_card(self, title, icon, description, command, row):
        """Adiciona um card de menu formatado e alinhado."""
        card = tk.Frame(
            self.scrollable_frame,
            bg=self.colors["card_bg"],
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["border"],
            highlightthickness=1
        )
        card.grid(row=row, column=0, sticky="ew", padx=25, pady=4)

        # --- Configuração do Grid do Card ---
        card.grid_columnconfigure(1, weight=1) # Permite que a coluna do texto (coluna 1) se expanda

        # Ícone (Coluna 0)
        icon_label = tk.Label(
            card, text=icon, font=("Arial", 22),
            bg=self.colors["card_bg"], fg=self.colors["text"], anchor="center"
        )
        # **CORREÇÃO APLICADA AQUI**: `sticky="n"` alinha o ícone ao TOPO (Norte) de sua célula.
        icon_label.grid(row=0, column=0, rowspan=2, padx=(15, 12), pady=10, sticky="n")

        # Frame para Título e Descrição (Coluna 1)
        text_frame = tk.Frame(card, bg=self.colors["card_bg"])
        # **CORREÇÃO APLICADA AQUI**: `sticky="ewns"` faz o frame de texto se esticar e se alinhar
        # ao topo (Norte) junto com o ícone, enquanto preenche o espaço horizontal.
        text_frame.grid(row=0, column=1, rowspan=2, sticky="ewns", pady=(10, 10))

        # Título
        title_label = tk.Label(
            text_frame, text=title, font=self.title_font,
            bg=self.colors["card_bg"], fg=self.colors["text"], anchor="w"
        )
        title_label.pack(fill='x')

        # Descrição
        desc_label = tk.Label(
            text_frame, text=description, font=self.desc_font,
            bg=self.colors["card_bg"], fg=self.colors["text"], anchor="w"
        )
        desc_label.pack(fill='x')
        
        # Linha separadora vertical (Coluna 2)
        separator = tk.Frame(card, bg=self.colors["border"], width=1)
        separator.grid(row=0, column=2, rowspan=2, sticky='ns', padx=5, pady=8)

        # Botão (Coluna 3)
        btn = tk.Button(
            card, text="Executar", command=command,
            bg=self.colors["button"], fg=self.colors["button_text"],
            relief="flat", font=("Helvetica", 9, "bold"),
            width=10, padx=10, pady=5
        )
        btn.grid(row=0, column=3, rowspan=2, padx=(5, 15), pady=10)

    # --- Métodos para as ações ---
    def reiniciar_computador(self):
        if messagebox.askyesno("Confirmar", "Deseja reiniciar o computador agora?"):
            os.system("shutdown /r /t 0")

    def otimizar_sistema(self):
        messagebox.showinfo("Otimização", "Iniciando limpeza e otimização do sistema...")
        try:
            os.system("del /s /f /q %temp%\\* >nul 2>&1")
            os.system("cleanmgr /sagerun:1")
            messagebox.showinfo("Otimização", "Desfragmentando disco (pode demorar)...")
            os.system("defrag C: /U /V")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a otimização:\n{e}")
        else:
            messagebox.showinfo("Concluído", "Otimização completa!")

    def flush_dns(self):
        os.system("ipconfig /flushdns")
        messagebox.showinfo("Sucesso", "Cache DNS limpo com sucesso!")

    def info_rede(self):
        try:
            result = subprocess.run(
                ["ipconfig", "/all"], capture_output=True, text=True, 
                encoding='cp850', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.show_output("Informações de Rede", result.stdout)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Comando 'ipconfig' não encontrado.")

    def ping_servidor(self):
        ip = simpledialog.askstring("Ping", "Digite o IP ou domínio do servidor:")
        if ip:
            try:
                command = ["ping", "-n", "10", ip]
                result = subprocess.run(
                    command, capture_output=True, text=True, 
                    encoding='cp850', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
                )
                self.show_output(f"Resultado do Ping para {ip}", result.stdout)
            except FileNotFoundError:
                messagebox.showerror("Erro", "Comando 'ping' não encontrado.")

    def central_rede(self):
        os.system("start ncpa.cpl")        
        
    def gerenciador_tarefa(self):        
        os.system("start taskmgr")
        
    def gerenciador_porta(self):
       porta = simpledialog.askstring("Verificar Porta", "Digite o número da porta que deseja verificar:")
       if porta:
        try:
            p1 = subprocess.Popen(
                ['netstat', '-aon'],
                stdout=subprocess.PIPE, text=True, encoding='cp850',
                errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            p2 = subprocess.Popen(
                ['findstr', f":{porta}"],
                stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='cp850', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            p1.stdout.close()
            output, errors = p2.communicate()

            if errors:
                output_text = f"Ocorreu um erro ao filtrar os resultados:\n{errors}"
            elif output:
                output_text = output
            else:
                output_text = f"Nenhuma conexão ou atividade encontrada para a porta {porta}."
            self.show_output(f"Atividade na Porta {porta}", output_text)

        except FileNotFoundError:
            messagebox.showerror("Erro", "Comando 'netstat' ou 'findstr' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao verificar a porta:\n{e}")

    def fix_erro_11b(self):
        try:
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f')
            self.reiniciar_spooler_silencioso()
            messagebox.showinfo("Sucesso", "Correção para o erro 0x0000011b aplicada.\nÉ recomendado reiniciar o computador.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao aplicar correção: {e}")

    def fix_erro_bcb(self):
        try:
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f')
            self.reiniciar_spooler_silencioso()
            messagebox.showinfo("Sucesso", "Correção para o erro 0x00000bcb aplicada.\nÉ recomendado reiniciar o computador.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao aplicar correção: {e}")

    def fix_erro_709(self):
        try:
            os.system('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows" /v Device /t REG_SZ /d "" /f')
            messagebox.showinfo("Aviso", "A impressora padrão foi redefinida.\nPor favor, defina sua impressora desejada como padrão manualmente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao redefinir impressora: {e}")

    def reiniciar_spooler_silencioso(self):
        os.system("net stop spooler > nul 2>&1")
        os.system("net start spooler > nul 2>&1")

    def reiniciar_spooler(self):
        messagebox.showinfo("Aguarde", "Reiniciando o serviço de impressão...")
        os.system("net stop spooler")
        os.system("del /q /f /s C:\\Windows\\System32\\spool\\PRINTERS\\*.*")
        os.system("net start spooler")
        messagebox.showinfo("Sucesso", "Spooler reiniciado e fila de impressão limpa com sucesso.")

    def abrir_impressoras(self):
        os.system("start explorer shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}")

    def baixar_universal(self):
        webbrowser.open("https://raw.githubusercontent.com/Delutto/instalador_universal/main/Output/Instalador_Universal_0.9.4.exe")

    def teste_conexao(self):
        webbrowser.open("https://www.speedtest.net/")

    def baixar_anota_ai(self):
        webbrowser.open("https://app.anota.ai/download-app/anotaai-desktop")

    def baixar_impressora_ai(self):
        webbrowser.open("https://legacy-assets.anota.ai/printer/Impressora+Anota+AI-v5-1.exe")

    def show_output(self, title, text):
        """Cria uma nova janela para exibir a saída de texto de um comando."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("700x500")
        window.configure(bg=self.colors["bg"])

        text_frame = tk.Frame(window, bg=self.colors["card_bg"])
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap="word", font=('Consolas', 10), relief="solid", bd=1)
        text_widget.insert("1.0", text or "Nenhuma saída para exibir.")
        text_widget.config(state="disabled")

        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)

        btn_frame = tk.Frame(window, bg=self.colors["bg"])
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(
            btn_frame, text="Fechar", command=window.destroy,
            bg=self.colors["button"], fg=self.colors["button_text"],
            relief="flat", padx=20, pady=5
        ).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = SuporteApp(root)
    root.mainloop()