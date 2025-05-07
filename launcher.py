import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar, Style
import threading
from queue import Queue
import subprocess
import sys
import os
import runpy
from threading import Event

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        
        # Set default values that can be overridden by kwargs
        button_config = {
            'bg': '#ffffff',
            'fg': '#007AFF',
            'activebackground': '#f0f0f0',
            'activeforeground': '#0051D5',
            'font': ('Helvetica', 15),
            'bd': 0,
            'relief': "flat",
            'anchor': 'center',
            'justify': 'center',
            'padx': 20,
            'pady': 10,
        }
        
        # Update defaults with any provided kwargs
        button_config.update(kwargs)
        
        super().__init__(parent, **button_config)
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['bg'] = '#f0f0f0'

    def on_leave(self, e):
        self['bg'] = '#ffffff'

class ModernFrame(tk.Frame):
    """A custom frame with rounded corners and shadow effect"""
    def __init__(self, parent, **kwargs):
        bg_color = kwargs.pop('bg', '#ffffff') if 'bg' in kwargs else '#ffffff'
        super().__init__(parent, bg=bg_color, **kwargs)
        self.configure(padx=15, pady=15, relief="flat", bd=0)
        
        

class ProgressWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Coleta")
        self.window.geometry("500x600")  # Aumentei a altura para 600px
        self.window.configure(bg='#f5f5f7')
        self.window.resizable(False, False)
        
        # Add a stop event flag
        self.stop_event = Event()
        self.chrome_drivers = []  # Lista para manter rastreamento dos drivers
        
        # Main container with fixed height
        self.container = ModernFrame(self.window, bg='#ffffff')
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header = tk.Label(
            self.container,
            text="Progresso da coleta de dados",
            font=('Helvetica', 20, 'bold'),
            bg='#ffffff',
            fg='#000000'
        )
        self.header.pack(pady=(0, 20))

        # Log text frame com altura fixa
        self.log_frame = tk.Frame(self.container, bg='#ffffff')
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

        self.log_text = tk.Text(
            self.log_frame,
            height=10,  # Altura fixa em linhas
            bg='#f5f5f7',
            fg='#000000',
            font=('Helvetica', 13),
            relief="flat",
            padx=10,
            pady=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Modern scrollbar
        scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Bottom frame para progress bar e botão
        bottom_frame = tk.Frame(self.container, bg='#ffffff')
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # Progress bar
        style = Style()
        style.configure(
            "iOS.Horizontal.TProgressbar",
            troughcolor='#f5f5f7',
            background='#007AFF',
            thickness=6
        )
        self.progress_bar = Progressbar(
            bottom_frame,
            style="iOS.Horizontal.TProgressbar",
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 20))

        # Stop button com tamanho fixo
        self.stop_button = ModernButton(
            bottom_frame,
            text="Stop",
            command=self.stop_scraping,
            fg='#ff3333',
            width=15,  # Largura fixa em caracteres
            height=2,  # Altura em linhas de texto
            font=('Helvetica', 14),  # Fonte um pouco maior
            padx=30,  # Padding horizontal
            pady=15   # Padding vertical
        )

        self.stop_button.pack(pady=(0, 10))

        self.booking_instance = None
        sys.stdout = self
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def write(self, text):
        try:
            self.log_text.insert(tk.END, text)
            self.log_text.see(tk.END)
            self.window.update()
        except:
            pass

    def flush(self):
        pass

    def cleanup_chrome(self):
        """Limpa todas as instâncias do Chrome e ChromeDriver"""
        # Tenta fechar o driver atual se existir
        if self.booking_instance:
            try:
                if hasattr(self.booking_instance, 'driver'):
                    self.booking_instance.driver.quit()
            except Exception as e:
                print(f"Erro ao fechar driver principal: {e}")

        # Tenta fechar todos os drivers registrados
        for driver in self.chrome_drivers:
            try:
                driver.quit()
            except:
                pass

        # Força o fechamento de processos do Chrome/ChromeDriver no Windows
        if os.name == 'nt':  # Windows
            try:
                os.system('taskkill /f /im chromedriver.exe')
                os.system('taskkill /f /im chrome.exe')
            except:
                pass
        else:  # Linux/Mac
            try:
                os.system('pkill chromedriver')
                os.system('pkill chrome')
            except:
                pass

    def stop_scraping(self):
        print("Stopping scraping process...")
        self.stop_button.config(text="Stopping...", state="disabled")
        
        # Set the stop event
        self.stop_event.set()
        
        # Fechar todas as instâncias do Chrome
        self.cleanup_chrome()
        
        # Force kill all threads except main thread
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                try:
                    thread._stop()
                except:
                    pass
        
        # Reset stdout and destroy window
        sys.stdout = sys.__stdout__
        self.window.destroy()
        
        # Force exit the application
        os._exit(0)

    def set_booking_instance(self, instance):
        self.booking_instance = instance
        if hasattr(instance, 'stop_event'):
            instance.stop_event = self.stop_event
        # Registra o driver se existir
        if hasattr(instance, 'driver'):
            self.chrome_drivers.append(instance.driver)

    def on_closing(self):
        self.stop_scraping()

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.window.update()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DataMiner Pet")
        
        version_label = tk.Label(
            self.root,
            text="DataMiner Pet BETA version: 0.2.311",
            font=('Helvetica', 10),
            bg='#f5f5f7',
            fg='lightgrey'  # Changed to light grey
        )
        version_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-2) 
        
        # Set fixed phone-like dimensions
        window_width = 500
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg='#f5f5f7')

        # Set base path
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Try to style the title bar (Windows only)
        try:
            self.root.attributes('-alpha', 0.95)  # Slight transparency
            if os.name == 'nt':  # Windows
                # Remove default title bar
                self
        except:
            pass

        # Load background and icon
        self.load_background()
        
        # Create main container
        self.main_container = ModernFrame(self.root, bg='#ffffff')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.show_main_menu()
    
    def handle_category_click(self, store_type, key):
        """Decide se mostra mais subcategorias ou executa o script"""
        subcats = self.get_subcategories(key)
        
        if subcats:  # Se houver mais subcategorias
            self.show_subcategories(store_type, key)
        else:  # Se for um script final
            self.run_script(key)

    def create_title_bar(self):
        title_bar = tk.Frame(self.root, bg='#ffffff', height=30)
        title_bar.pack(fill=tk.X)
        
        # Load and display icon
        try:
            icon_path = os.path.join(self.base_path, "app", "static", "icon.ico")
            icon_image = Image.open(icon_path)
            # Resize icon to fit title bar
            icon_image = icon_image.resize((16, 16), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = tk.Label(title_bar, image=self.icon_photo, bg='#ffffff')
            icon_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Error loading icon in title bar: {e}")
        
        close_button = tk.Label(title_bar, text="×", bg='#ffffff', fg='#007AFF', font=('Helvetica', 16))
        close_button.pack(side=tk.RIGHT, padx=10)
        close_button.bind('<Button-1>', lambda e: self.root.destroy())
        close_button.bind('<Enter>', lambda e: close_button.configure(fg='#ff3b30'))
        close_button.bind('<Leave>', lambda e: close_button.configure(fg='#007AFF'))
        
        # Make window draggable
        title_bar.bind('<Button-1>', self.save_last_click)
        title_bar.bind('<B1-Motion>', self.dragging)


    def save_last_click(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def dragging(self, event):
        x = event.x - self.lastClickX + self.root.winfo_x()
        y = event.y - self.lastClickY + self.root.winfo_y()
        self.root.geometry(f"+{x}+{y}")

    def load_background(self):
        try:
            background_image_path = os.path.join(self.base_path, "app", "static", "BLOG-DATA-MINING.png")
            iconbitpath = os.path.join(self.base_path, "app", "static", "icon.ico")
            self.root.iconbitmap(iconbitpath)

            bg_image = Image.open(background_image_path)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.main_container,
            text="DataMiner  Pet",
            font=('Helvetica', 25, 'bold'),
            bg='#ffffff',
            fg='#000000'
        )
        title.pack(pady=(0, 30))

        # Main buttons
        ModernButton(
            self.main_container,
            text="Petz",
            command=lambda: self.show_categories('Petz')
        ).pack(pady=10, fill=tk.X)
        
        """
        ModernButton(
            self.main_container,
            text="Petly",
            command=lambda: self.show_categories('Petily')
        ).pack(pady=10, fill=tk.X)"""

        # Divider
        tk.Frame(self.main_container, height=1, bg='#e5e5e5').pack(fill=tk.X, pady=20)

        # Exit button
        ModernButton(
            self.main_container,
            text="Exit",
            fg='#ff3b30',
            command=self.root.destroy
        ).pack(pady=10)

    @staticmethod
    def get_store_categories(store_name):
        """
        Returns store categories and their corresponding subcategories
        """
        if store_name == "Petz":
            return [
                ("Cachorro", "dog_categories"),  # Instead of direct script, reference subcategory group
                ("Gato", "cat_categories"),
            ]
        elif store_name == "Petily":
            return [
                ("Cachorro", "dry_food_categories"),
                ("Gato","dry_food_cat_categories")
            ]
        return [("Categoria Padrão", "default_categories")]

    @staticmethod
    def get_subcategories(category_key):
        """
        Returns subcategories and their corresponding scripts based on the category key
        """
        subcategories = {
            "dog_categories": [
                ("Ração", "dog_racoes"),
                ("Petiscos e Ossos", "dog_petiscos"),
                ("Tapetes, Fraldas e Banheiros", "cachorro_cachorro_tapetes_fraldas_banheiros.py"),
                ("Farmácia", "dog_farmacia"),
                ("Brinquedos", "dog_brinquedos"),
                ("Coleiras, guias e peitorais", "cachorro_coleiras.py"),
                ("Beleza e Limpeza", "dog_beleza"),
                ("Camas e Cobertores", "dog_camas"),
                ("Casa e Tocas", "cachorro_casas.py"),
                ("Acessórios de Alimentação", "dog_alimento"),
                ("Acessórios de Transporte", "cachorro_transporte.py"),
                ("Portões, Grades e Escadas", "cachorro_portoes.py"),
                ("Roupas", "dog_roupas"),
                ("Adestramento e Comportamento", "cachorro_adestramento.py"),
            ],
            "dog_racoes":[
                ("Ração Seca", "dog_porte"),
                ("Ração Umida", "cachorro_sub_racao_umida.py"),
                ("Ração Prescrita", "cachorro_sub_racao_prescrita.py"),
                ("Ração Natural", "cachorro_sub_racao_natural.py"),
            ],
            "dog_alimento": [
                ("Fontes", "cachorro_alimentacao_sub_fontes.py"),
                ("Dosadores de Ração", "cachorro_alimentacao_sub_dosadores.py"),
                ("Porta Ração", "cachorro_alimentacao_sub_porta_racao.py"),
                ("Comedouros", "cachorro_alimentacao_sub_comedouros.py"),
                ("Bebedouros", "cachorro_alimentacao_sub_bebedouros.py"),
                ("Jogo Americano", "cachorro_alimentacao_sub_jogo_americano.py"),
                ("Mamadeiras", "cachorro_alimentacao_sub_mamadeiras.py"),
            ],
            "dog_roupas": [
                ("Almofadas e Colchonetes", "cachorro_camas_sub_almofadas.py"),
                ("Camas", "cachorro_camas_sub_camas.py"),
                ("Edredons, Cobertores e Mantas", "cachorro_camas_sub_edredons.py"),
            ],
            "dog_camas": [
                ("Roupas de Inverno", "cachorro_roupas_sub_inverno.py"),
                ("Roupas de Verão", "cachorro_roupas_sub_verao.py"),
                ("Diversos", "cachorro_roupas_sub_diversos.py"),
            ],
            "dog_porte": [
                ("Adulto", "dog_racao_seca_adulto"),
                ("Filhote", "cachorro_racao_seca_idade_filhote.py"),
                ("Sênior", "cachorro_racao_seca_idade_senior.py"),
            ],
            "dog_racao_seca_adulto": [
                ("Gigante", "cachorro_racao_seca_adulto_gigante.py"),
                ("Grande", "cachorro_racao_seca_adulto_grande.py"),
                ("Médio", "cachorro_racao_seca_adulto_medio.py"),
                ("Mini", "cachorro_racao_seca_adulto_mini.py"),
                ("Pequeno", "cachorro_racao_seca_adulto_pequeno.py"),
            ],
            "dog_racao_seca_filhote": [
                ("Gigante", "cachorro_racao_seca_filhote_gigante.py"),
                ("Grande", "cachorro_racao_seca_filhote_grande.py"),
                ("Médio", "cachorro_racao_seca_filhote_medio.py"),
                ("Mini", "cachorro_racao_seca_filhote_mini.py"),
                ("Pequeno", "cachorro_racao_seca_filhote_pequeno.py"),
            ],
            "dog_racao_seca_senior": [
                ("Gigante", "cachorro_racao_seca_senior_gigante.py"),
                ("Grande", "cachorro_racao_seca_senior_grande.py"),
                ("Médio", "cachorro_racao_seca_senior_medio.py"),
                ("Mini", "cachorro_racao_seca_senior_mini.py"),
                ("Pequeno", "cachorro_racao_seca_senior_pequeno.py"),
            ],
            "dog_petiscos":[
                ("Cuidado Oral", "cachorro_sub_petisco_oral.py"),
                ("Petiscos Naturais", "cachorro_sub_petisco_natural.py"),
                ("Bifinhos", "cachorro_sub_petisco_bifinhos.py"),
                ("Biscoitos", "cachorro_sub_petisco_biscoitos.py"),
                ("Bolos e Chocolates", "cachorro_sub_petisco_bolos.py"),
                ("Bebidas e molhos", "cachorro_sub_petisco_bebidas.py"),
                ("Ossinhos", "cachorro_sub_petisco_ossinhos.py"),
            ],
            "dog_brinquedos":[
                ("Bichinhos de Pelúcia", "cachorro_brinquedos_sub_pelucia.py"),
                ("Bolinhas", "cachorro_brinquedos_sub_bolinhas.py"),
                ("Brinquedos em Nylon", "cachorro_brinquedos_sub_nylon.py"),
                ("Brinquedos Educativos", "cachorro_brinquedos_sub_educativos.py"),
                ("Brinquedos de Corda", "cachorro_brinquedos_sub_corda.py"),
                ("Frisbees", "cachorro_brinquedos_sub_frisbees.py"),
                ("Mordedores", "cachorro_brinquedos_sub_mordedores.py"),
            ],
            "dog_farmacia":[
                ("Antipulgas e Carrapatos", "cachorro_farmacia_sub_antipulgas.py"),
                ("Demais medicamentos", "cachorro_farmacia_sub_medicamentos.py"),
                ("Anti-inflamatórios", "cachorro_farmacia_sub_antiinflamatorios.py"),
                ("Antibióticos", "cachorro_farmacia_sub_antibioticos.py"),
                ("Suplementos e Vitaminas", "cachorro_farmacia_sub_suplementos.py"),
                ("Vermífugos", "cachorro_farmacia_sub_vermifugos.py"),
                ("Homeopáticos e Florais", "cachorro_farmacia_sub_homeopaticos.py"),
                ("Oftalmológicos", "cachorro_farmacia_sub_oftalmologicos.py"),
                ("Otológicos", "cachorro_farmacia_sub_otologicos.py"),
                ("Cuidado Oral", "cachorro_farmacia_sub_oral.py"),
                ("Banho Terapêuticos", "cachorro_farmacia_sub_banho.py"),
                ("Roupas Cirúrgicas", "cachorro_farmacia_sub_roupas.py"),
                ("Colares Elizabetanos", "cachorro_farmacia_sub_colares.py"),
            ],
            "dog_beleza":[
                ("Banho à Seco e Talcos", "cachorro_beleza_sub_banho_seco.py"),
                ("Sabonetes", "cachorro_beleza_sub_sabonetes.py"),
                ("Shampoos e Condicionadores", "cachorro_beleza_sub_shampoos.py"),
                ("Hidratantes", "cachorro_beleza_sub_hidratantes.py"),
                ("Perfumes e Colônias", "cachorro_beleza_sub_perfumes.py"),
                ("Higiene Bucal", "cachorro_beleza_sub_higiene_bucal.py"),
                ("Pentes, Escovas e Rasqueadeiras", "cachorro_beleza_sub_pentes.py"),
                ("Lenços Umidecidos", "cachorro_beleza_sub_lencos.py"),
                ("Limpeza de Olhos e Ouvidos", "cachorro_beleza_sub_limpeza_olhos.py"),
                ("Máquina de Tosa e Acessórios", "cachorro_beleza_sub_maquina_tosa.py"),
                ("Alicates e Tesouras", "cachorro_beleza_sub_alicates.py"),
                ("Eliminador de Odores e Desinfetantes", "cachorro_beleza_sub_eliminador.py"),
                ("Educadores, Repelentes e Atrativos", "cachorro_beleza_sub_educadores.py"),
            ],
            "cat_categories": [
                ("Ração", "cat_racoes"),
                ("Petiscos", "gato_petisco.py"),
                ("Areias e banheiros", "gato_areia.py"),
                ("Farmácia", "cat_farmacia"),
                ("Arranhadores e Brinquedos", "gato_brinquedos.py"),
                ("Beleza e Limpeza", "cat_beleza"),
                ("Coleiras e Peitorais", "gato_coleiras.py"),
                ("Acessórios para Alimentação", "gato_comedouros.py"),
                ("Acessórios de Transporte", "gato_transporte.py"),
                ("Camas, Almofadas e Tocas", "gato_camas.py"),
                ("Roupas", "gato_roupas.py"),
            ],
            "cat_racoes":[
                ("Ração Seca", "gato_racao_seca.py"),
                ("Ração Umida", "gato_racao_umida.py"),
                ("Ração Prescrita", "gato_racao_prescrita.py"),
                ("Ração Natural", "gato_racao_natural.py"),
            ],
            "cat_farmacia":[
                ("Antipulgas e Carrapatos", "gato_farmacia_antipulgas.py"),
                ("Demais medicamentos", "gato_farmacia_demais.py"),
                ("Anti-inflamatórios", "gato_farmacias_antiinflamatorios.py"),
                ("Antibióticos", "gato_farmacia_antibioticos.py"),
                ("Suplementos e Vitaminas", "gato_farmacia_suplementos.py"),
                ("Vermífugos", "gato_farmacia_vermifugos.py"),
                ("Homeopáticos e Florais", "gato_farmacia_homeopaticos.py"),
                ("Oftalmológicos", "gato_farmacia_oftalmologicos.py"),
                ("Otológicos", "gato_farmacia_otologicos.py"),
                ("Banho Terapêuticos", "gato_farmacias_banho.py"),
                ("Roupas Cirúrgicas", "gato_farmacia_roupas.py"),
                ("Colares Elizabetanos", "gato_farmacia_colares.py"),
            ],
            "cat_beleza":[
                ("Alicates e Tesouras", "gato_beleza_sub_alicates.py"),
                ("Banho à Seco e Talcos", "gato_beleza_sub_banho_seco.py"),
                ("Higiene Bucal", "gato_beleza_sub_higiene_bucal.py"),
                ("Lenços Umidecidos", "gato_beleza_sub_lencos.py"),
                ("Limpeza de Olhos e Ouvidos", "gato_beleza_sub_limpeza_olhos.py"),
                ("Máquina de Tosa e Acessórios", "gato_beleza_sub_maquina_tosa.py"),
                ("Pentes, Escovas e Rasqueadeiras", "gato_beleza_sub_pentes.py"),
                ("Perfumes e Colônias", "gato_beleza_sub_perfumes.py"),
                ("Sabonetes", "gato_beleza_sub_sabonetes.py"),
                ("Shampoos e Condicionadores", "gato_beleza_sub_shampoos.py"),
                ("Hidratantes", "gato_beleza_sub_hidratantes.py"),
                ("Eliminador de Odores e Desinfetantes", "gato_beleza_sub_eliminador.py"),
                ("Educadores, Repelentes e Atrativos", "gato_beleza_sub_educadores.py"),
            ],
            # Add more category groups as needed
        }
        return subcategories.get(category_key, [])

    def handle_category_click(self, store_type, key):
        """Decide se mostra mais subcategorias ou executa um script"""
        subcats = self.get_subcategories(key)
        
        if subcats:  # Se houver mais subcategorias
            self.show_subcategories(store_type, key)
        else:  # Se for um script final
            self.run_script(key)
    
    def show_categories(self, store_type):
        self.clear_container()
        
        header = tk.Label(
            self.main_container,
            text=f"Categorias - {store_type}:",
            font=('Helvetica', 16, 'bold'),
            bg='#ffffff',
            fg='#000000'
        )
        header.pack(pady=(0, 30))

        categories = self.get_store_categories(store_type)

        for label, category_key in categories:
            ModernButton(
                self.main_container,
                text=label,
                command=lambda k=category_key: self.show_subcategories(store_type, k)
            ).pack(pady=10, fill=tk.X)

        tk.Frame(self.main_container, height=1, bg='#e5e5e5').pack(fill=tk.X, pady=20)

        ModernButton(
            self.main_container,
            text="Back",
            fg='#007AFF',
            command=self.show_main_menu
        ).pack(pady=10)

    def show_subcategories(self, store_type, category_key):
        self.clear_container()

        subcategories = self.get_subcategories(category_key)
        
        if not subcategories:
            self.run_script(category_key)
            return

        # Header
        header = tk.Label(
            self.main_container,
            text=f"Subcategorias - {store_type}:",
            font=('Helvetica', 16, 'bold'),
            bg='#ffffff',
            fg='#000000'
        )
        header.pack(pady=(0, 10))

        # Container principal com scroll
        scroll_container = tk.Frame(self.main_container, bg='#ffffff')
        scroll_container.pack(fill=tk.BOTH, expand=True)

        # Configuração do Canvas e Scrollbar
        canvas = tk.Canvas(scroll_container, bg='#ffffff', highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient=tk.VERTICAL, command=canvas.yview)
        
        # Empacota na ordem correta
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame interno para os botões (CENTRALIZADO)
        buttons_frame = tk.Frame(canvas, bg='#ffffff')
        canvas.create_window((0, 0), window=buttons_frame, anchor="nw")

        # Habilita scroll com mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Atualiza o frame para centralizar
        def _configure_buttons_frame(event):
            canvas.itemconfig(buttons_frame_id, width=event.width)
            
        buttons_frame_id = canvas.create_window((0, 0), window=buttons_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        buttons_frame.bind("<Configure>", _configure_buttons_frame)

        # Botões centralizados
        for label, key in subcategories:
            btn = ModernButton(
                buttons_frame,
                text=label,
                command=lambda k=key: self.handle_category_click(store_type, k)
            )
            btn.pack(pady=10, fill=tk.X, expand=True, padx=20)  # Reduzi o padx

        # Divisor centralizado
        tk.Frame(buttons_frame, height=1, bg='#e5e5e5').pack(fill=tk.X, pady=20, padx=20)

        # Botão Voltar
        ModernButton(
            buttons_frame,
            text="Back",
            fg='#007AFF',
            command=lambda: self.show_categories(store_type)
        ).pack(pady=10, fill=tk.X, expand=True, padx=20)


    

    def run_script(self, script_name):
        def script_thread():
            progress_window = ProgressWindow(self.root)
            try:
                script_dir = sys._MEIPASS if getattr(sys, "frozen", False) else self.base_path
                script_path = os.path.join(script_dir, "bot", script_name)
                #print(f"Running script")
                print(f"Iniciando a coleta...")
                
                original_cwd = os.getcwd()
                os.chdir(os.path.dirname(script_path))
                
                globals_dict = runpy.run_path(script_path, run_name="__main__")
                if 'booking_filtration' in globals_dict:
                    booking_instance = globals_dict['booking_filtration']
                    progress_window.set_booking_instance(booking_instance)
            except Exception as e:
                print(f"Error running script {script_name}: {e}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to run {script_name}: {str(e)}"))
            finally:
                os.chdir(original_cwd)

        thread = threading.Thread(target=script_thread, daemon=True)
        thread.start()


        
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
