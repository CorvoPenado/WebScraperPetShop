import os
import sys
from selenium import webdriver
from bot.filtration import BookingFiltration
from bot.PetilyHttpSelenium import PetilyScraperBot
import bot.constants as const

class Booking(webdriver.Chrome):
    def __init__(self, base_path=None, teardown=False):
            # Initialize ChromeOptions for headless operation
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")  # Use new headless mode
            options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
            options.add_argument("--no-sandbox")  # Bypass OS security model (for Linux)
            options.add_argument("--disable-features=WebGPU")
            options.add_argument("--disable-features=WebGL")
            options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues (for Linux)
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation flag

            # Initialize WebDriver with options
            super().__init__(options=options)

            self.teardown = teardown
            
            # Handle the base path for both normal and bundled execution
            if getattr(sys, 'frozen', False):
                # Running in a PyInstaller bundle
                self.base_path = sys._MEIPASS
            else:
                # Running in a normal Python environment
                self.base_path = base_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            self.maximize_window()  # Maximize (may still work in headless mode)
            self.implicitly_wait(15)  # Implicit wait for page load
            self.execute_script("window.scrollBy(0, 500);")  # Execute a scroll to trigger some rendering

            # Hide the 'navigator.webdriver' flag
            self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })

    # Rest of your class implementation remains the same
    
    #Categoria de ração DIVIDIDA
    def land_cachorro_sub_racao_seca(self):
        self.get(self._get_url("CACHORRO_RACAO_SUB_SECA"))

    def land_cachorro_sub_racao_umida(self):
        self.get(self._get_url("CACHORRO_RACAO_SUB_UMIDA"))

    def land_cachorro_sub_racao_prescrita(self):
        self.get(self._get_url("CACHORRO_RACAO_SUB_PRESCRITA"))

    def land_cachorro_sub_racao_natural(self):
        self.get(self._get_url("CACHORRO_RACAO_SUB_NATURAL"))
    #FIM DA CATEGORIA DE RAÇÃO
    
    #inicio categoria petiscos e ossos
    def land_cachorro_sub_petisco_oral(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_ORAL"))

    def land_cachorro_sub_petisco_natural(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_NATURAL"))

    def land_cachorro_sub_petisco_bifinhos(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_BIFINHOS"))

    def land_cachorro_sub_petisco_biscoitos(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_BISCOITOS"))

    def land_cachorro_sub_petisco_bolos(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_BOLOS"))

    def land_cachorro_sub_petisco_bebidas(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_BEBIDAS"))

    def land_cachorro_sub_petisco_ossinhos(self):
        self.get(self._get_url("CACHORRO_PETISCO_SUB_OSSINHOS"))
    #FIM DA CATEGORIA de petiscos e ossos
    
    #Começo categoria Higiene
    def land_cachorro_sub_higiene_tapetes(self):
        self.get(self._get_url("CACHORRO_HIGIENE_SUB_TAPETES"))

    def land_cachorro_sub_higiene_fraldas(self):
        self.get(self._get_url("CACHORRO_HIGIENE_SUB_FRALDAS"))

    def land_cachorro_sub_higiene_banheiros(self):
        self.get(self._get_url("CACHORRO_HIGIENE_SUB_BANHEIROS"))

    def land_cachorro_sub_higiene_cones(self):
        self.get(self._get_url("CACHORRO_HIGIENE_SUB_CONES"))
    #Fim da categoria de higiene    
    
    #Começo categoria de farmacia
    def land_cachorro_farmacia_sub_antipulgas(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_ANTIPULGAS"))

    def land_cachorro_farmacia_sub_medicamentos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_MEDICAMENTOS"))

    def land_cachorro_farmacia_sub_antiinflamatorios(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_ANTIINFLAMATORIOS"))

    def land_cachorro_farmacia_sub_antibioticos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_ANTIBIOTICOS"))

    def land_cachorro_farmacia_sub_suplementos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_SUPLEMENTOS"))

    def land_cachorro_farmacia_sub_vermifugos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_VERMIFUGOS"))

    def land_cachorro_farmacia_sub_homeopaticos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_HOMEOPATICOS"))

    def land_cachorro_farmacia_sub_oftalmologicos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_OFTALMOLOGICOS"))

    def land_cachorro_farmacia_sub_otologicos(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_OTOLOGICOS"))

    def land_cachorro_farmacia_sub_oral(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_ORAL"))

    def land_cachorro_farmacia_sub_banho(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_BANHO"))

    def land_cachorro_farmacia_sub_roupas(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_ROUPAS"))

    def land_cachorro_farmacia_sub_colares(self):
        self.get(self._get_url("CACHORRO_FARMACIA_SUB_COLARES")) 
    #Fim Categoria farmacia

    #Começo categoria brinquedo
    def land_cachorro_brinquedos_sub_pelucia(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_PELUCIA"))

    def land_cachorro_brinquedos_sub_bolinhas(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_BOLINHAS"))

    def land_cachorro_brinquedos_sub_nylon(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_NYLON"))

    def land_cachorro_brinquedos_sub_educativos(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_EDUCATIVOS"))

    def land_cachorro_brinquedos_sub_corda(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_CORDA"))

    def land_cachorro_brinquedos_sub_frisbees(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_FRISBEES"))

    def land_cachorro_brinquedos_sub_mordedores(self):
        self.get(self._get_url("CACHORRO_BRINQUEDOS_SUB_MORDEDORES"))
    #Fim Categoria brinquedo
    
    #inicio categoria de LIMPEZA - BANHO - BELEZA
    
    def land_cachorro_beleza_sub_banho_seco(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_BANHO_SECO"))

    def land_cachorro_beleza_sub_sabonetes(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_SABONETES"))

    def land_cachorro_beleza_sub_shampoos(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_SHAMPOOS"))

    def land_cachorro_beleza_sub_hidratantes(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_HIDRATANTES"))

    def land_cachorro_beleza_sub_perfumes(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_PERFUMES"))

    def land_cachorro_beleza_sub_higiene_bucal(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_HIGIENE_BUCAL"))

    def land_cachorro_beleza_sub_pentes(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_PENTES"))

    def land_cachorro_beleza_sub_lencos(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_LENCOS"))

    def land_cachorro_beleza_sub_limpeza_olhos(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_LIMPEZA_OLHOS"))

    def land_cachorro_beleza_sub_maquina_tosa(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_MAQUINA_TOSA"))

    def land_cachorro_beleza_sub_alicates(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_ALICATES"))

    def land_cachorro_beleza_sub_coletor(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_COLETOR"))

    def land_cachorro_beleza_sub_eliminador(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_ELIMINADOR"))

    def land_cachorro_beleza_sub_educadores(self):
        self.get(self._get_url("CACHORRO_BELEZA_SUB_EDUCADORES")) 
    
    #FIM CATEGORIA LIMPEZA-BANHO-BELEZA
    
    
    def land_cachorro_coleiras(self):
        self.get(self._get_url("CACHORRO_COLEIRAS"))
        
    def land_cachorro_cama(self):
        self.get(self._get_url("CACHORRO_CAMA"))
        
    def land_cachorro_casas(self):
        self.get(self._get_url("CACHORRO_CASAS"))
        
    def land_cachorro_comedouros(self):
        self.get(self._get_url("CACHORRO_COMEDOUROS"))
        
    def land_cachorro_portoes(self):
        self.get(self._get_url("CACHORRO_PORTOES"))
        
    def land_cachorro_roupas(self):
        self.get(self._get_url("CACHORRO_ROUPAS"))
        
    def land_cachorro_adestramento(self):
        self.get(self._get_url("CACHORRO_ADESTRAMENTO"))
        
    def land_cachorro_transporte(self):
        self.get(self._get_url("CACHORRO_TRANSPORTE"))
        
    #INICIO CACHORROS RACAO SECA NOVA OPCAO
    # Funções para Ração Adulto
    def land_cachorro_racao_seca_adulto_pequeno(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_ADULTO_PEQUENO"))

    def land_cachorro_racao_seca_adulto_medio(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_ADULTO_MEDIO"))

    def land_cachorro_racao_seca_adulto_grande(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_ADULTO_GRANDE"))

    def land_cachorro_racao_seca_adulto_mini(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_ADULTO_MINI"))

    def land_cachorro_racao_seca_adulto_gigante(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_ADULTO_GIGANTE"))

    # Funções para Ração Filhote
    def land_cachorro_racao_seca_filhote_pequeno(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_FILHOTE_PEQUENO"))

    def land_cachorro_racao_seca_filhote_medio(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_FILHOTE_MEDIO"))

    def land_cachorro_racao_seca_filhote_grande(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_FILHOTE_GRANDE"))

    def land_cachorro_racao_seca_filhote_mini(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_FILHOTE_MINI"))

    def land_cachorro_racao_seca_filhote_gigante(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_FILHOTE_GIGANTE"))

    # Funções para Ração Senior
    def land_cachorro_racao_seca_senior_pequeno(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_SENIOR_PEQUENO"))

    def land_cachorro_racao_seca_senior_medio(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_SENIOR_MEDIO"))

    def land_cachorro_racao_seca_senior_grande(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_SENIOR_GRANDE"))

    def land_cachorro_racao_seca_senior_mini(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_SENIOR_MINI"))

    def land_cachorro_racao_seca_senior_gigante(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_SENIOR_GIGANTE")) 

    
    #Cachorro cama
    def land_cachorro_camas_sub_almofadas(self):
        self.get(self._get_url("CACHORRO_CAMAS_SUB_ALMOFADAS"))

    def land_cachorro_camas_sub_camas(self):
        self.get(self._get_url("CACHORRO_CAMAS_SUB_CAMAS"))

    def land_cachorro_camas_sub_edredons(self):
        self.get(self._get_url("CACHORRO_CAMAS_SUB_EDREDONS"))
        
    #Alimentação
    def land_cachorro_alimentacao_sub_fontes(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_FONTES"))

    def land_cachorro_alimentacao_sub_dosadores(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_DOSADORES"))

    def land_cachorro_alimentacao_sub_porta_racao(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_PORTA_RACAO"))

    def land_cachorro_alimentacao_sub_comedouros(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_COMEDOUROS"))

    def land_cachorro_alimentacao_sub_bebedouros(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_BEBEDOUROS"))

    def land_cachorro_alimentacao_sub_jogo_americano(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_JOGO_AMERICANO"))

    def land_cachorro_alimentacao_sub_mamadeiras(self):
        self.get(self._get_url("CACHORRO_ALIMENTACAO_SUB_MAMADEIRAS"))
    
    #Auternativas
    def land_cachorro_racao_seca_idade_filhote(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_IDADE_FILHOTE"))

    def land_cachorro_racao_seca_idade_senior(self):
        self.get(self._get_url("CACHORRO_RACAO_SECA_IDADE_SENIOR"))
    
    #Roupas
    def land_cachorro_roupas_sub_inverno(self):
        self.get(self._get_url("CACHORRO_ROUPAS_SUB_INVERNO"))

    def land_cachorro_roupas_sub_verao(self):
        self.get(self._get_url("CACHORRO_ROUPAS_SUB_VERAO"))

    def land_cachorro_roupas_sub_diversos(self):
        self.get(self._get_url("CACHORRO_ROUPAS_SUB_DIVERSOS"))
    
    #GATOS ABAIXO
    
    #Gato ração
    def land_gato_racao_natural(self):
        self.get(self._get_url("GATO_RACAO_NATURAL"))
        
    def land_gato_racao_seca(self):
            self.get(self._get_url("GATO_RACAO_SECA"))

    def land_gato_racao_umida(self):
            self.get(self._get_url("GATO_RACAO_UMIDA"))

    def land_gato_racao_prescrita(self):
            self.get(self._get_url("GATO_RACAO_PRESCRITA"))
    #Fim gato ração
    
    #Gato petiscos
    def land_gato_petiscos_biscoitos(self):
        self.get(self._get_url("GATO_PETISCOS_BISCOITOS"))

    def land_gato_petiscos_bifinhos(self):
        self.get(self._get_url("GATO_PETISCOS_BIFINHOS"))
    #Fim gato petiscos
    
    #Gato areia
    def land_gato_areia_areias(self):
        self.get(self._get_url("GATO_AREIA_AREIAS"))

    def land_gato_areia_silica(self):
        self.get(self._get_url("GATO_AREIA_SILICA"))

    def land_gato_areia_caixas(self):
        self.get(self._get_url("GATO_AREIA_CAIXAS"))

    def land_gato_areia_banheiros(self):
        self.get(self._get_url("GATO_AREIA_BANHEIROS"))

    def land_gato_areia_acessorios(self):
        self.get(self._get_url("GATO_AREIA_ACESSORIOS"))
    #Fim gato areia
    
    #Gato farmacia
    def land_gato_farmacia_antipulgas(self):
        self.get(self._get_url("GATO_FARMACIA_ANTIPULGAS"))

    def land_gato_farmacia_vermifugos(self):
        self.get(self._get_url("GATO_FARMACIA_VERMIFUGOS"))

    def land_gato_farmacia_suplementos(self):
        self.get(self._get_url("GATO_FARMACIA_SUPLEMENTOS"))

    def land_gato_farmacia_antibioticos(self):
        self.get(self._get_url("GATO_FARMACIA_ANTIBIOTICOS"))

    def land_gato_farmacia_antiinflamatorios(self):
        self.get(self._get_url("GATO_FARMACIA_ANTIINFLAMATORIOS"))

    def land_gato_farmacia_banho(self):
        self.get(self._get_url("GATO_FARMACIA_BANHO"))

    def land_gato_farmacia_colares(self):
        self.get(self._get_url("GATO_FARMACIA_COLARES"))

    def land_gato_farmacia_homeopaticos(self):
        self.get(self._get_url("GATO_FARMACIA_HOMEOPATICOS"))

    def land_gato_farmacia_demais(self):
        self.get(self._get_url("GATO_FARMACIA_DEMAIS"))

    def land_gato_farmacia_oftalmologicos(self):
        self.get(self._get_url("GATO_FARMACIA_OFTALMOLOGICOS"))

    def land_gato_farmacia_otologicos(self):
        self.get(self._get_url("GATO_FARMACIA_OTOLOGICOS"))

    def land_gato_farmacia_roupas(self):
        self.get(self._get_url("GATO_FARMACIA_ROUPAS"))
    #Fim gato farmacia
    
    #Gato beleza
    def land_gato_beleza_sub_alicates(self):
        self.get(self._get_url("GATO_BELEZA_SUB_ALICATES"))

    def land_gato_beleza_sub_banho_seco(self):
        self.get(self._get_url("GATO_BELEZA_SUB_BANHO_SECO"))

    def land_gato_beleza_sub_higiene_bucal(self):
        self.get(self._get_url("GATO_BELEZA_SUB_HIGIENE_BUCAL"))

    def land_gato_beleza_sub_lencos(self):
        self.get(self._get_url("GATO_BELEZA_SUB_LENCOS"))

    def land_gato_beleza_sub_limpeza_olhos(self):
        self.get(self._get_url("GATO_BELEZA_SUB_LIMPEZA_OLHOS"))

    def land_gato_beleza_sub_maquina_tosa(self):
        self.get(self._get_url("GATO_BELEZA_SUB_MAQUINA_TOSA"))

    def land_gato_beleza_sub_pentes(self):
        self.get(self._get_url("GATO_BELEZA_SUB_PENTES"))

    def land_gato_beleza_sub_perfumes(self):
        self.get(self._get_url("GATO_BELEZA_SUB_PERFUMES"))

    def land_gato_beleza_sub_sabonetes(self):
        self.get(self._get_url("GATO_BELEZA_SUB_SABONETES"))

    def land_gato_beleza_sub_shampoos(self):
        self.get(self._get_url("GATO_BELEZA_SUB_SHAMPOOS"))

    def land_gato_beleza_sub_hidratantes(self):
        self.get(self._get_url("GATO_BELEZA_SUB_HIDRATANTES"))

    def land_gato_beleza_sub_eliminador(self):
        self.get(self._get_url("GATO_BELEZA_SUB_ELIMINADOR"))

    def land_gato_beleza_sub_educadores(self):
        self.get(self._get_url("GATO_BELEZA_SUB_EDUCADORES")) 
    #Fim gato beleza
    
    def land_gato_racao(self):
        self.get(self._get_url("GATO_URL"))
        
    def land_gato_petisco(self):
        self.get(self._get_url("GATO_PETISCO"))
        
    def land_gato_areia(self):
        self.get(self._get_url("GATO_AREIA"))
        
    def land_gato_farmacia(self):
        self.get(self._get_url("GATO_FARMACIA"))
        
    def land_gato_brinquedos(self):
        self.get(self._get_url("GATO_BRINQUEDOS"))
        
    def land_gato_beleza(self):
        self.get(self._get_url("GATO_BELEZA"))
        
    def land_gato_coleiras(self):
        self.get(self._get_url("GATO_COLEIRAS"))
        
    def land_gato_comedouros(self):
        self.get(self._get_url("GATO_COMEDOUROS"))
        
    def land_gato_transporte(self):
        self.get(self._get_url("GATO_TRANSPORTE"))
        
    def land_gato_camas(self):
        self.get(self._get_url("GATO_CAMAS"))
        
    def land_gato_roupas(self):
        self.get(self._get_url("GATO_ROUPAS"))
        
    def land_gato_racas(self):
        self.get(self._get_url("GATO_RACAS"))
    
    def land_casa_e_jardim(self):
        self.get(self._get_url("CASA_E_JARDIM_URL"))
    
    def land_peixe(self):
        self.get(self._get_url("PEIXE_URL"))

    def petily_racoes_secas(self):
        self.get(self._get_url("PETILY_RACOES_SECAS"))
    
    def petily_gato_racoes_secas(self):
        self.get(self._get_url("PETILY_GATO_RACAO_SECA"))
    
    def aplly_filtration(self):
        filtration = BookingFiltration(self)
        filtration.filter_products()

    def apply_filtration_petily(self):
        filtration = PetilyScraperBot(self)
        filtration.extract_data()

    def _get_url(self, constant_name):
        try:
            return getattr(const, constant_name)
        except AttributeError:
            print(f"Error: {constant_name} not found in constants.py.")
            return ""
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()