from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import openpyxl
import os
import sys
from time import sleep
from urllib.parse import urlparse
import requests
from threading import Thread, Lock
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class PetilyScraperBot:
    def __init__(self, main_driver: WebDriver, num_threads=3):
        self.main_driver = main_driver
        self.num_threads = num_threads
        self.drivers = []
        self.product_queue = Queue()
        self.processed_products = 0
        self.excel_lock = Lock()
        self.print_lock = Lock()
        
        # Inicializa drivers adicionais para as threads
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Modo headless para threads adicionais
        for _ in range(num_threads):
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_script_timeout(30000)
            self.drivers.append(driver)
        
        current_url = self.main_driver.current_url
        parsed_url = urlparse(current_url)
        self.base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path_parts = parsed_url.path.strip('/').split('/')
        category = path_parts[1] if len(path_parts) >= 2 and path_parts[0] == 'collections' else 'products'
        
        if getattr(sys, 'frozen', False):
            executable_dir = os.path.dirname(sys.executable)
        else:
            executable_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.produtos_folder = os.path.join(executable_dir, "produtos")
        if not os.path.exists(self.produtos_folder):
            os.makedirs(self.produtos_folder)
        
        self.excel_file = os.path.join(self.produtos_folder, f"produtos_petily_{category}.xlsx")
        self._initialize_excel()
        
        # Session para requisições HTTP
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _check_if_sold_out(self, driver):
        """Check if the product is sold out using multiple methods."""
        try:
            # Check for aria-label="Esgotado" on button
            sold_out_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Esgotado"]')
            if sold_out_buttons:
                return True

            # Additional checks for sold out status
            sold_out_elements = driver.find_elements(By.CSS_SELECTOR, 
                '.sold-out, [data-sold-out="true"], .product-form__buttons button[disabled]')
            for elem in sold_out_elements:
                if elem.get_attribute('aria-label') == 'Esgotado' or 'Esgotado' in elem.text:
                    return True

            return False
        except Exception as e:
            self._safe_print(f"[DEBUG] Error checking sold out status: {e}")
            return False

    def __del__(self):
        # Fecha todos os drivers adicionais
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass

    def _safe_print(self, message):
        with self.print_lock:
            print(message)

    def _initialize_excel(self):
        if not os.path.exists(self.excel_file):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Products"
            sheet.append(["Título", "Preço", "Original Price", "Link", "Variação"])
            workbook.save(self.excel_file)
            self._safe_print(f"Excel file initialized at {self.excel_file}")

    def _append_to_excel(self, data):
        with self.excel_lock:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    workbook = openpyxl.load_workbook(self.excel_file)
                    sheet = workbook.active
                    sheet.append([
                        data['Título'], 
                        data['Preço'], 
                        data['Original Price'],
                        data['Link'], 
                        data['Variação']
                    ])
                    workbook.save(self.excel_file)
                    
                    self.processed_products += 1
                    self._safe_print(f"Saved product {self.processed_products}: {data['Título']} - {data['Variação']}")
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        self._safe_print(f"Failed to save to Excel after {max_retries} attempts: {e}")
                    else:
                        self._safe_print(f"Error appending data, retrying... ({attempt + 1}/{max_retries})")
                        sleep(0.5)

    def _get_prices(self, driver):
        """Get current and original prices with improved selectors."""
        wait = WebDriverWait(driver, 5)
        current_price = "N/A"
        original_price = "Sem promoção"
        
        price_selectors = [
            '.price-item--sale',
            '.price-item--regular',
            '.price__regular .price-item',
            '.price .money',
            '[data-regular-price]',
            '.product__price'
        ]
        
        try:
            for selector in price_selectors:
                try:
                    price_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    current_price = price_element.text.strip()
                    if current_price:
                        # Try to find original price if there's a sale
                        try:
                            regular_element = driver.find_element(By.CLASS_NAME, 'price-item--regular')
                            original_price = regular_element.text.strip()
                        except:
                            pass
                        break
                except TimeoutException:
                    continue
        except Exception as e:
            self._safe_print(f"[ERROR] Error getting prices: {e}")
            
        return current_price, original_price

    def _check_product_availability(self, driver):
        try:
            sold_out = driver.find_element(By.CSS_SELECTOR, '#ProductSection-product-customizado2 div.div dl div dd span')
            return sold_out.text.strip() != "Esgotado"
        except:
            return True
        
    def _get_page_products(self, url):
        try:
            self._safe_print(f"\n[DEBUG] Acessando URL: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Log do HTML para debug
            self._safe_print("[DEBUG] Procurando produtos na página...")
            all_products = []
            
            # Primeiro método: grid-view-item
            products = soup.find_all(class_='grid-view-item')
            self._safe_print(f"[DEBUG] Produtos encontrados com grid-view-item: {len(products)}")
            all_products.extend(products)
            
            # Segundo método: product-card
            products = soup.find_all(class_='product-card')
            self._safe_print(f"[DEBUG] Produtos encontrados com product-card: {len(products)}")
            all_products.extend(products)
            
            # Terceiro método: seletores alternativos
            products = soup.select('.product-grid .grid__item, .collection-grid .grid__item, [data-product-card]')
            self._safe_print(f"[DEBUG] Produtos encontrados com seletores alternativos: {len(products)}")
            all_products.extend(products)
            
            # Remove duplicatas baseado no href
            unique_products = []
            seen_links = set()
            
            for product in all_products:
                try:
                    # Tenta diferentes padrões de links
                    link_elem = (product.find('a', class_='grid-view-item__link') or 
                            product.find('a', class_='full-unstyled-link') or
                            product.find('a', href=True))
                    
                    if link_elem and 'href' in link_elem.attrs:
                        link = link_elem['href']
                        if link not in seen_links:
                            seen_links.add(link)
                            unique_products.append(product)
                            self._safe_print(f"[DEBUG] Produto encontrado: {link}")
                except Exception as e:
                    self._safe_print(f"[DEBUG] Erro ao processar produto: {e}")
            
            self._safe_print(f"[DEBUG] Total de produtos únicos encontrados: {len(unique_products)}")
            return unique_products
            
        except Exception as e:
            self._safe_print(f"[ERROR] Erro ao buscar produtos da página {url}: {e}")
            return []

    def _process_variations(self, driver, title, link):
        """Process product variations with improved organization and stock checking."""
        self._safe_print(f"\n[DEBUG] Processing product: {title}")
        self._safe_print(f"[DEBUG] Product URL: {link}")
        
        variations_data = []  # Store all variations data for sorting
        
        try:
            wait = WebDriverWait(driver, 5)
            
            # Find variation selectors
            select_elements = (
                driver.find_elements(By.ID, 'SingleOptionSelector-0') or
                driver.find_elements(By.CLASS_NAME, 'single-option-selector') or
                driver.find_elements(By.CSS_SELECTOR, '[data-single-option-selector]')
            )
            
            if not select_elements:
                # Handle single product without variations
                if not self._check_if_sold_out(driver):
                    current_price, original_price = self._get_prices(driver)
                    if current_price and current_price != "N/A":
                        variations_data.append({
                            'Título': title,
                            'Preço': current_price,
                            'Original Price': original_price,
                            'Link': link,
                            'Variação': 'Única'
                        })
            else:
                # Handle product with variations
                select = Select(select_elements[0])
                variations = [(i, option.text) for i, option in enumerate(select.options)]
                
                for index, variation_name in variations:
                    try:
                        if index > 0:
                            driver.get(link)
                            sleep(1)
                            # Refind selector after page reload
                            select_elements = (
                                driver.find_elements(By.ID, 'SingleOptionSelector-0') or
                                driver.find_elements(By.CLASS_NAME, 'single-option-selector') or
                                driver.find_elements(By.CSS_SELECTOR, '[data-single-option-selector]')
                            )
                            if select_elements:
                                select = Select(select_elements[0])
                        
                        select.select_by_index(index)
                        sleep(1)
                        
                        if not self._check_if_sold_out(driver):
                            current_price, original_price = self._get_prices(driver)
                            if current_price and current_price != "N/A":
                                variations_data.append({
                                    'Título': title,
                                    'Preço': current_price,
                                    'Original Price': original_price,
                                    'Link': link,
                                    'Variação': variation_name
                                })
                    
                    except Exception as e:
                        self._safe_print(f"[ERROR] Error processing variation {variation_name}: {e}")
            
            # Sort variations data by variation name and save to Excel
            variations_data.sort(key=lambda x: x['Variação'])
            for data in variations_data:
                self._append_to_excel(data)
                
        except Exception as e:
            self._safe_print(f"[ERROR] General error processing product {title}: {str(e)}")

    def _worker(self, thread_id):
        self._safe_print(f"\n[DEBUG] Iniciando worker {thread_id}")
        driver = self.drivers[thread_id]
        wait = WebDriverWait(driver, 10)
        
        while True:
            try:
                product = self.product_queue.get_nowait()
                if product is None:
                    self._safe_print(f"[DEBUG] Worker {thread_id} finalizando")
                    break
                
                link, title = product
                self._safe_print(f"\n[DEBUG] Worker {thread_id} processando: {title}")
                self._safe_print(f"[DEBUG] Link: {link}")
                
                remaining = self.product_queue.qsize()
                self._safe_print(f"[DEBUG] Produtos restantes na fila: {remaining}")
                
                driver.get(link)
                self._safe_print(f"[DEBUG] Página carregada: {link}")
                
                try:
                    title_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-single__title')))
                    title = title_elem.text.strip()
                    self._safe_print(f"[DEBUG] Título encontrado: {title}")
                except Exception as e:
                    self._safe_print(f"[DEBUG] Erro ao encontrar título: {e}")
                
                self._process_variations(driver, title, link)
                
            except Queue.Empty:
                self._safe_print(f"[DEBUG] Fila vazia para worker {thread_id}")
                break
            except Exception as e:
                self._safe_print(f"[ERROR] Erro no worker {thread_id}: {e}")
            finally:
                self.product_queue.task_done()

    def extract_data(self):
        page = 1
        base_url = self.main_driver.current_url
        all_products = []

        self.total_products = len(all_products)
        #print(f"\nIniciando processamento de {self.total_products} produtos com {self.num_threads} Trabalhadores")
        print(f"\nAguarde...")
        
        # Coleta todos os produtos primeiro
        while True:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            product_cards = self._get_page_products(url)
            
            if not product_cards:
                break
                
            self._safe_print(f"Found {len(product_cards)} products on page {page}")
            
            for card in product_cards:
                try:
                    link_elem = card.find(class_='grid-view-item__link')
                    if not link_elem or 'href' not in link_elem.attrs:
                        continue
                        
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = self.base_domain + link
                        
                    title = link_elem.get('title', '')
                    all_products.append((link, title))
                    
                except Exception as e:
                    self._safe_print(f"Error processing product card: {e}")
                    continue
            
            page += 1
        
        # Coloca todos os produtos na fila
        for product in all_products:
            self.product_queue.put(product)
            
        # Adiciona None para cada thread para sinalizar término
        for _ in range(self.num_threads):
            self.product_queue.put(None)
        
        # Inicia as threads
        threads = []
        for i in range(self.num_threads):
            thread = Thread(target=self._worker, args=(i,))
            thread.start()
            threads.append(thread)
        
        # Espera todas as threads terminarem
        for thread in threads:
            thread.join()
        
        self._safe_print("Extraction completed!")