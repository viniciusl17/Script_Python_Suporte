import tkinter as tk
from tkinter import messagebox, simpledialog, font
import os
import webbrowser
import subprocess
import sys

class SuporteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Suporte Técnico")
        self.root.geometry("500x750")
        self.root.resizable(False, True)

        self.colors = {
            "bg": "#f0f4f8",
            "card_bg": "#ffffff",
            "text": "#003d4d",
            "header": "#005f69",
            "button": "#003B99",
            "button_text": "#ffffff",
            "border": "#e0e0e0",
            "attention_bg": "#fff3cd",
            "attention_fg": "#664d03"
        }

        self.root.configure(bg=self.colors["bg"])

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=10)
        self.title_font = ("Helvetica", 12, "bold")
        self.desc_font = ("Helvetica", 9)
        self.section_font = ("Helvetica", 11, "bold")
        self.header_font = ("Helvetica", 14, "bold")
        self.emoji_font = ("Helvetica", 20)

        self.create_header()
        self.create_main_frame()
        self.create_menu_cards()

    def create_header(self):
        attention_frame = tk.Frame(self.root, bg=self.colors["bg"])
        attention_frame.pack(fill="x", padx=25, pady=(10, 0))
        
        tk.Label(
            attention_frame,
            text="Para melhor experiência, Execute como Administrador",
            font=("Helvetica", 9, "italic"),
            fg=self.colors["attention_fg"],
            bg=self.colors["attention_bg"],
            pady=5
        ).pack(fill="x")

        header_frame = tk.Frame(self.root, bg=self.colors["bg"])
        header_frame.pack(fill="x", padx=25, pady=(5, 10))

        tk.Label(
            header_frame,
            text="Menu Suporte Técnico",
            font=self.header_font,
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(side="left")

        tk.Label(
            header_frame,
            text="v1.2",
            font=("Helvetica", 9),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(side="right")

    def create_main_frame(self):
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
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_menu_cards(self):
        self.add_section("GERAL", 0)
        self.add_card("Otimizar sistema", "✨", "Limpeza detalhada de temporários", self.otimizar_sistema, 1)
        self.add_card("Flush DNS", "🌐", "Limpar cache DNS", self.flush_dns, 2)
        self.add_card("Informações de rede", "📡", "Mostra configurações de rede", self.info_rede, 3)
        self.add_card("Ping Servidor", "💻", "Testar conexão com servidor", self.ping_servidor, 4)
        self.add_card("Central de rede", "🔗", "Abrir configurações de rede", self.central_rede, 5)
        self.add_card("Gerenciador de Tarefas", "📋", "Abrir Gerenciador de tarefas", self.gerenciador_tarefa, 6)
        self.add_card("Atividade Porta", "🚪", "Ver e finalizar atividades nas portas", self.gerenciador_porta, 7)
        self.add_section("IMPRESSORAS", 8)
        self.add_card("Instalador Universal", "⬇️", "Baixar programa das impressoras", self.baixar_universal, 9)
        self.add_card("Fix erro 0x0000011b", "🪛", "Corrigir erro de impressão", self.fix_erro_11b, 10)
        self.add_card("Fix erro 0x00000bcb", "🪛", "Corrigir erro de impressão", self.fix_erro_bcb, 11)
        self.add_card("Fix erro 0x00000709", "🪛", "Corrigir erro de impressão padrão", self.fix_erro_709, 12)
        self.add_card("Reiniciar spooler", "🔄", "Reinicia o serviço de impressão", self.reiniciar_spooler, 13)
        self.add_card("Dispositivos e impressoras", "🔧", "Abrir gerenciador de impressoras", self.abrir_impressoras, 14)
        self.add_section("TESTE DE CONEXÃO", 15)
        self.add_card("Teste de conexão", "🚀", "Abrir speedtest.net", self.teste_conexao, 16)
        self.add_section("SOFTWARES", 17)
        self.add_card("Anota AI Desktop", "⬇️", "Baixar versão atualizada", self.baixar_anota_ai, 18)
        self.add_card("Advanced Ip Scanner", "⬇️", "Baixar Advanced Ip Scanner", self.baixar_advanced, 19)
        self.add_card("Revo Uninstaller", "⬇️", "Baixar Revo Unistaller", self.baixar_revo, 20)

    def add_section(self, title, row):
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
        card = tk.Frame(
            self.scrollable_frame,
            bg=self.colors["card_bg"],
            borderwidth=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["border"],
            highlightthickness=1
        )
        card.grid(row=row, column=0, sticky="ew", padx=25, pady=4)
        card.grid_columnconfigure(1, weight=1)
        icon_label = tk.Label(
            card, text=icon, font=self.emoji_font, bg=self.colors["card_bg"], fg=self.colors["text"]
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=(15, 12), pady=10, sticky="n")
        title_label = tk.Label(
            card, text=title, font=self.title_font, bg=self.colors["card_bg"], fg=self.colors["text"], anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="sew", pady=(10, 0))
        desc_label = tk.Label(
            card, text=description, font=self.desc_font, bg=self.colors["card_bg"], fg=self.colors["text"], anchor="w"
        )
        desc_label.grid(row=1, column=1, sticky="new")
        separator = tk.Frame(card, bg=self.colors["border"], width=1)
        separator.grid(row=0, column=2, rowspan=2, sticky='ns', padx=5, pady=8)
        btn = tk.Button(
            card, text="Executar", command=command, bg=self.colors["button"], fg=self.colors["button_text"],
            relief="flat", font=("Helvetica", 9, "bold"), width=10, padx=10, pady=5
        )
        btn.grid(row=0, column=3, rowspan=2, padx=(5, 15), pady=10, sticky="ns")

    def otimizar_sistema(self):
        messagebox.showinfo("Otimização", "A otimização será iniciada. Este processo pode levar alguns minutos.")
        log_report = []
        log_report.append("--- ETAPA 1: Limpeza de Arquivos Temporários ---\n")
        
        try:
            temp_dir = os.path.expandvars('%TEMP%')
            arquivos_excluidos = 0
            pastas_excluidas = 0
            
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        log_report.append(f"Arquivo excluído - {file_path}")
                        os.remove(file_path)
                        arquivos_excluidos += 1
                    except OSError:
                        log_report.append(f"AVISO: Não foi possível excluir o arquivo (em uso): {file_path}")
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        log_report.append(f"Pasta excluída - {dir_path}")
                        os.rmdir(dir_path)
                        pastas_excluidas += 1
                    except OSError:
                        log_report.append(f"AVISO: Não foi possível excluir a pasta (não está vazia): {dir_path}")
            
            log_report.append(f"\nLimpeza de temporários concluída. {arquivos_excluidos} arquivo(s) e {pastas_excluidas} pasta(s) processado(s).\n")

            log_report.append("\n--- ETAPA 2: Limpeza de Disco (cleanmgr) ---\n")
            cleanmgr_path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "cleanmgr.exe")
            if os.path.exists(cleanmgr_path):
                log_report.append("Iniciando a Limpeza de Disco do Windows...")
                subprocess.run([cleanmgr_path, "/sagerun:1"], capture_output=True, text=True)
                log_report.append("Limpeza de disco concluída.\n")
            else:
                log_report.append("AVISO: O utilitário 'cleanmgr.exe' não foi encontrado. Pulando esta etapa.\n")

        except Exception as e:
            log_report.append(f"\n!!! ERRO DURANTE A OTIMIZAÇÃO: {e} !!!")
        finally:
            log_report.append("\n--- OTIMIZAÇÃO FINALIZADA ---")
            self.show_output("Relatório de Otimização do Sistema", "\n".join(log_report))

    def reiniciar_spooler(self):
        log_report = []
        log_report.append("--- INICIANDO REINICIALIZAÇÃO DO SPOOLER DE IMPRESSÃO ---\n")
        try:
            log_report.append("Parando o serviço de Spooler...")
            os.system("net stop spooler")
            log_report.append("... Serviço parado com sucesso.\n")

            spool_dir = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'spool', 'PRINTERS')
            log_report.append(f"Limpando a fila de impressão em: {spool_dir}...")
            
            if os.path.exists(spool_dir):
                arquivos_spool_excluidos = 0
                for filename in os.listdir(spool_dir):
                    file_path = os.path.join(spool_dir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            log_report.append(f"  - Excluindo arquivo de spool: {filename}")
                            os.remove(file_path)
                            arquivos_spool_excluidos += 1
                    except Exception as e:
                        log_report.append(f"    [AVISO] Não foi possível excluir {filename}: {e}")
                log_report.append(f"... Fila de impressão limpa. {arquivos_spool_excluidos} arquivo(s) excluído(s).\n")
            else:
                log_report.append("... Diretório de spool não encontrado. Pulando etapa de limpeza.\n")

            log_report.append("Iniciando o serviço de Spooler...")
            os.system("net start spooler")
            log_report.append("... Serviço iniciado com sucesso.\n")

        except Exception as e:
            log_report.append(f"\n!!! ERRO DURANTE A REINICIALIZAÇÃO DO SPOOLER: {e} !!!")
        finally:
            log_report.append("\n--- PROCESSO DE REINICIALIZAÇÃO CONCLUÍDO ---")
            self.show_output("Relatório de Reinicialização do Spooler", "\n".join(log_report))

    def flush_dns(self):
        os.system("ipconfig /flushdns")
        messagebox.showinfo("Sucesso", "Cache DNS limpo com sucesso!")

    def info_rede(self):
        try:
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, 
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
        if not porta or not porta.isdigit():
            return
        try:
            p1 = subprocess.Popen(['netstat', '-aon'], stdout=subprocess.PIPE, text=True, encoding='cp850', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            p2 = subprocess.Popen(['findstr', f":{porta}"], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp850', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            p1.stdout.close()
            output, _ = p2.communicate()
            if not output.strip():
                messagebox.showinfo("Atividade na Porta", f"Nenhuma conexão ou atividade encontrada para a porta {porta}.")
                return
            pids_to_kill = set()
            lines = output.strip().split('\n')
            details = []
            for line in lines:
                clean_line = line.strip()
                parts = [p for p in clean_line.split(' ') if p]
                if parts and parts[-1].isdigit():
                    pids_to_kill.add(parts[-1])
                    details.append(clean_line)
            if not pids_to_kill:
                self.show_output(f"Atividade na Porta {porta}", output)
                return
            pids_list = sorted(list(pids_to_kill))
            pids_str = ", ".join(pids_list)
            details_str = "\n".join(details)
            if messagebox.askyesno(
                "Finalizar Múltiplos Processos?",
                f"Encontrado(s) {len(pids_list)} processo(s) com PID(s): {pids_str} utilizando a porta {porta}.\n\n"
                f"Detalhes:\n{details_str}\n\n"
                f"Deseja finalizar TODOS os processos encontrados?"
            ):
                success_pids = []
                failed_pids_info = []
                for pid in pids_list:
                    try:
                        kill_command = ["taskkill", "/F", "/PID", pid]
                        subprocess.run(kill_command, capture_output=True, text=True, check=True, encoding='cp850', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
                        success_pids.append(pid)
                    except subprocess.CalledProcessError as e:
                        error_msg = e.stderr.strip() or e.stdout.strip()
                        failed_pids_info.append(f"{pid} ({error_msg})")
                    except Exception as e:
                        failed_pids_info.append(f"{pid} (Erro: {e})")
                success_str = f"Processos finalizados com sucesso: {', '.join(success_pids)}\n" if success_pids else ""
                failed_str = f"Falha ao finalizar os processos com PID: {', '.join(failed_pids_info)}" if failed_pids_info else ""
                final_message = "Relatório da Operação:\n\n" + success_str + failed_str
                if failed_pids_info:
                    final_message += "\n\nAlgumas falhas podem ocorrer por falta de permissão. Tente executar o programa como administrador."
                    messagebox.showwarning("Operação Concluída com Falhas", final_message.strip())
                else:
                    messagebox.showinfo("Operação Concluída", final_message.strip())
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

    def abrir_impressoras(self):
        os.system("start explorer shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}")

    def baixar_universal(self):
        webbrowser.open("https://raw.githubusercontent.com/Delutto/instalador_universal/main/Output/Instalador_Universal_0.9.4.exe")

    def teste_conexao(self):
        webbrowser.open("https://www.speedtest.net/")

    def baixar_anota_ai(self):
        webbrowser.open("https://app.anota.ai/download-app/anotaai-desktop")

    def baixar_advanced(self):
        webbrowser.open("https://www.advanced-ip-scanner.com/br/download/")
        
    def baixar_revo(self):
        webbrowser.open("https://drive.google.com/file/d/1foBLAGXWVGjggftV0RQHqwjJ2TSyO08q/view?usp=drive_link")

    def show_output(self, title, text):
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
            btn_frame, text="Fechar", command=window.destroy, bg=self.colors["button"], fg=self.colors["button_text"],
            relief="flat", padx=20, pady=5
        ).pack(side="right")


if __name__ == "__main__":
    # Bloco principal simplificado. A responsabilidade de abrir o console
    # agora é do executável gerado pelo PyInstaller (sem a flag --windowed).
    root = tk.Tk()
    app = SuporteApp(root)
    root.mainloop()