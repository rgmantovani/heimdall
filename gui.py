import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from Entities.User import User
from Entities.Key import Key
from System.HeimdallSystem import HeimdallSystem


class HeimdallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heimdall — Gerenciador de Chaves")
        self.root.geometry("940x580")
        self.root.resizable(True, True)

        self.system = HeimdallSystem()
        self.db = self.system.sgbd

        self._build_layout()
        self._show_tab_retirada()

    # ------------------------------------------------------------------ layout

    def _build_layout(self):
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=180)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="HEIMDALL", bg="#2c3e50", fg="white",
                 font=("Helvetica", 14, "bold"), pady=20).pack()

        nav = [
            ("Retirar / Devolver", self._show_tab_retirada),
            ("Usuários",           self._show_tab_usuarios),
            ("Chaves",             self._show_tab_chaves),
            ("Histórico",          self._show_tab_historico),
        ]
        for label, cmd in nav:
            tk.Button(sidebar, text=label, command=cmd,
                      bg="#34495e", fg="white", relief=tk.FLAT,
                      font=("Helvetica", 11), pady=10, cursor="hand2",
                      activebackground="#1abc9c", activeforeground="white",
                      ).pack(fill=tk.X, padx=10, pady=4)

        self.content = tk.Frame(self.root, bg="#ecf0f1")
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_retirada  = self._build_retirada()
        self.frame_usuarios  = self._build_usuarios()
        self.frame_chaves    = self._build_chaves()
        self.frame_historico = self._build_historico()

    def _clear_content(self):
        for f in (self.frame_retirada, self.frame_usuarios,
                  self.frame_chaves, self.frame_historico):
            f.pack_forget()

    # ------------------------------------------------------------------ retirada

    def _build_retirada(self):
        frame = tk.Frame(self.content, bg="#ecf0f1")

        tk.Label(frame, text="Retirar / Devolver Chave",
                 font=("Helvetica", 16, "bold"), bg="#ecf0f1", pady=15).pack()

        form = tk.Frame(frame, bg="#ecf0f1")
        form.pack(pady=10)

        tk.Label(form, text="Código do Usuário:", bg="#ecf0f1").grid(
            row=0, column=0, sticky=tk.E, padx=10, pady=8)
        self.entry_user = tk.Entry(form, width=28)
        self.entry_user.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Código da Chave (sala):", bg="#ecf0f1").grid(
            row=1, column=0, sticky=tk.E, padx=10, pady=8)
        self.entry_key = tk.Entry(form, width=28)
        self.entry_key.grid(row=1, column=1, pady=8)

        btn_frame = tk.Frame(frame, bg="#ecf0f1")
        btn_frame.pack(pady=14)

        tk.Button(btn_frame, text="  Retirar Chave  ", bg="#27ae60", fg="white",
                  relief=tk.FLAT, font=("Helvetica", 11),
                  command=self._action_withdraw).pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frame, text=" Devolver Chave  ", bg="#e67e22", fg="white",
                  relief=tk.FLAT, font=("Helvetica", 11),
                  command=self._action_return).pack(side=tk.LEFT, padx=12)

        self.lbl_status = tk.Label(frame, text="", bg="#ecf0f1",
                                   font=("Helvetica", 11))
        self.lbl_status.pack(pady=6)

        return frame

    def _show_tab_retirada(self):
        self._clear_content()
        self.frame_retirada.pack(fill=tk.BOTH, expand=True)

    def _action_withdraw(self):
        user_code = self.entry_user.get().strip().upper()
        key_code  = self.entry_key.get().strip().upper()
        if not user_code or not key_code:
            messagebox.showwarning("Atenção", "Preencha o código do usuário e da chave.")
            return
        try:
            # validar usuário
            if self.db.searchUserByCode(userCode=user_code) == []:
                messagebox.showerror("Erro", "Usuário não cadastrado.")
                return
            # validar chave
            keys = self.db.searchKeyByCode(keyCode=key_code)
            if keys == []:
                messagebox.showerror("Erro", "Chave não encontrada.")
                return
            if not keys[0].isAvailable():
                messagebox.showerror("Erro", "Chave não está disponível.")
                return
            self.db.withdrawKey(keyCode=key_code, userCode=user_code)
            self.lbl_status.config(
                text=f"Chave '{key_code}' retirada por '{user_code}'.", fg="#27ae60")
            self._safe_refresh_keys()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _action_return(self):
        user_code = self.entry_user.get().strip().upper()
        key_code  = self.entry_key.get().strip().upper()
        if not user_code or not key_code:
            messagebox.showwarning("Atenção", "Preencha o código do usuário e da chave.")
            return
        try:
            opened = self.db.searchWithdrawsByUsercode(userCode=user_code, status="opened")
            match = [w for w in opened if str(w.getKeyCode()).upper() == key_code]
            if not match:
                messagebox.showerror("Erro", "Não há retirada em aberto para esse usuário/chave.")
                return
            self.db.returnKey(userCode=user_code, keyCode=key_code)
            self.lbl_status.config(
                text=f"Chave '{key_code}' devolvida por '{user_code}'.", fg="#e67e22")
            self._safe_refresh_keys()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ------------------------------------------------------------------ usuários

    def _build_usuarios(self):
        frame = tk.Frame(self.content, bg="#ecf0f1")

        tk.Label(frame, text="Usuários", font=("Helvetica", 16, "bold"),
                 bg="#ecf0f1", pady=15).pack()

        cols = ("Código", "Nome", "Sobrenome", "Papel", "Curso")
        self.tree_users = ttk.Treeview(frame, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree_users.heading(c, text=c)
            self.tree_users.column(c, width=140, anchor=tk.CENTER)
        self.tree_users.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        btn_frame = tk.Frame(frame, bg="#ecf0f1")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Adicionar", bg="#2980b9", fg="white",
                  relief=tk.FLAT, command=self._dialog_add_user).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="Remover Selecionado", bg="#c0392b", fg="white",
                  relief=tk.FLAT, command=self._action_remove_user).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="Atualizar", bg="#7f8c8d", fg="white",
                  relief=tk.FLAT, command=self._refresh_users).pack(side=tk.LEFT, padx=8)

        return frame

    def _show_tab_usuarios(self):
        self._clear_content()
        self.frame_usuarios.pack(fill=tk.BOTH, expand=True)
        self._refresh_users()

    def _refresh_users(self):
        for row in self.tree_users.get_children():
            self.tree_users.delete(row)
        try:
            for u in self.db.listOfUsers:
                self.tree_users.insert("", tk.END, values=(
                    u.getCode(), u.getName(), u.getSurname(),
                    u.getRole(), u.getCourse()))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar usuários:\n{e}")

    def _dialog_add_user(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Adicionar Usuário")
        dlg.resizable(False, False)
        dlg.grab_set()

        fields = [("Nome", "name"), ("Sobrenome", "surname"),
                  ("Código", "code"), ("Papel", "role"), ("Curso", "course")]
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dlg, text=label + ":").grid(row=i, column=0,
                                                  sticky=tk.E, padx=12, pady=6)
            e = tk.Entry(dlg, width=30)
            e.grid(row=i, column=1, pady=6, padx=12)
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            if not all(data.values()):
                messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=dlg)
                return
            if self.db.searchUserByCode(userCode=data["code"]) != []:
                messagebox.showwarning("Atenção", "Já existe um usuário com esse código.", parent=dlg)
                return
            try:
                u = User()
                u.setName(data["name"]); u.setSurname(data["surname"])
                u.setCode(data["code"]); u.setRole(data["role"])
                u.setCourse(data["course"]); u.setPhoto(None)
                self.db.insertNewUser(newUser=u)
                self._refresh_users()
                dlg.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=dlg)

        tk.Button(dlg, text="Salvar", bg="#27ae60", fg="white", relief=tk.FLAT,
                  command=submit).grid(row=len(fields), column=0, columnspan=2, pady=14)

    def _action_remove_user(self):
        sel = self.tree_users.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um usuário na tabela.")
            return
        code = self.tree_users.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover o usuário com código '{code}'?"):
            try:
                self.db.removeAnUser(userCode=str(code))
                self._refresh_users()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    # ------------------------------------------------------------------ chaves

    def _build_chaves(self):
        frame = tk.Frame(self.content, bg="#ecf0f1")

        tk.Label(frame, text="Chaves", font=("Helvetica", 16, "bold"),
                 bg="#ecf0f1", pady=15).pack()

        cols = ("Sala", "Disponível")
        self.tree_keys = ttk.Treeview(frame, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree_keys.heading(c, text=c)
            self.tree_keys.column(c, width=250, anchor=tk.CENTER)
        self.tree_keys.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        btn_frame = tk.Frame(frame, bg="#ecf0f1")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Adicionar Chave", bg="#2980b9", fg="white",
                  relief=tk.FLAT, command=self._dialog_add_key).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="Atualizar", bg="#7f8c8d", fg="white",
                  relief=tk.FLAT, command=self._refresh_keys).pack(side=tk.LEFT, padx=8)

        return frame

    def _show_tab_chaves(self):
        self._clear_content()
        self.frame_chaves.pack(fill=tk.BOTH, expand=True)
        self._refresh_keys()

    def _refresh_keys(self):
        for row in self.tree_keys.get_children():
            self.tree_keys.delete(row)
        try:
            for k in self.db.listOfKeys:
                self.tree_keys.insert("", tk.END,
                                      values=(k.getRoom(), "Sim" if k.isAvailable() else "Não"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar chaves:\n{e}")

    def _safe_refresh_keys(self):
        try:
            self._refresh_keys()
        except Exception:
            pass

    def _dialog_add_key(self):
        room = simpledialog.askstring("Adicionar Chave",
                                      "Código/sala da chave:", parent=self.root)
        if room:
            room = room.strip().upper()
            keys = self.db.searchKeyByCode(keyCode=room)
            if keys:
                messagebox.showwarning("Atenção", "Já existe uma chave com esse código.")
                return
            try:
                self.db.insertNewKey(newKey=Key(room=room))
                self._refresh_keys()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    # ------------------------------------------------------------------ histórico

    def _build_historico(self):
        frame = tk.Frame(self.content, bg="#ecf0f1")

        tk.Label(frame, text="Histórico de Retiradas",
                 font=("Helvetica", 16, "bold"), bg="#ecf0f1", pady=15).pack()

        filter_frame = tk.Frame(frame, bg="#ecf0f1")
        filter_frame.pack()
        tk.Label(filter_frame, text="Filtro:", bg="#ecf0f1").pack(side=tk.LEFT, padx=6)
        self.cmb_filter = ttk.Combobox(
            filter_frame, values=["Todos", "Em aberto", "Finalizados"],
            state="readonly", width=16)
        self.cmb_filter.set("Todos")
        self.cmb_filter.pack(side=tk.LEFT, padx=4)
        tk.Button(filter_frame, text="Buscar", bg="#2980b9", fg="white",
                  relief=tk.FLAT, command=self._refresh_historico).pack(side=tk.LEFT, padx=8)

        cols = ("Usuário", "Chave", "Retirada", "Devolução")
        self.tree_hist = ttk.Treeview(frame, columns=cols, show="headings", height=13)
        widths = [160, 160, 220, 220]
        for c, w in zip(cols, widths):
            self.tree_hist.heading(c, text=c)
            self.tree_hist.column(c, width=w, anchor=tk.CENTER)
        self.tree_hist.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        return frame

    def _show_tab_historico(self):
        self._clear_content()
        self.frame_historico.pack(fill=tk.BOTH, expand=True)
        self._refresh_historico()

    def _refresh_historico(self):
        for row in self.tree_hist.get_children():
            self.tree_hist.delete(row)
        status_map = {"Todos": "all", "Em aberto": "opened", "Finalizados": "finished"}
        status = status_map.get(self.cmb_filter.get(), "all")
        try:
            withdraws = self.db.searchWithdrawsByStatus(status=status)
            for w in withdraws:
                final = w.getFinalTime() or "—"
                self.tree_hist.insert("", tk.END, values=(
                    w.getUserCode(), w.getKeyCode(),
                    w.getInitialTime(), final))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    HeimdallGUI(root)
    root.mainloop()
