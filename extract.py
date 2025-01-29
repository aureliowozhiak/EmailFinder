import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from duckduckgo_search import DDGS
import re
import urllib.parse
import time

def create_output_dir():
    if not os.path.exists('arquivos'):
        os.makedirs('arquivos')

def download_file(url, filename):
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            with open(os.path.join('arquivos', filename), 'wb') as f:
                f.write(response.content)
            return True
    except:
        return False
    return False

def has_emails(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex para encontrar emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, content)
            return len(emails) > 0
    except:
        return False

def search_files(query, engine = 'google'):
    create_output_dir()
    
    # Add delay between searches to avoid rate limiting
    time.sleep(2)  # 2 second delay between searches
    
    failures = 0
    max_failures = 3
    
    try:
        # Busca sites relacionados à query
        if engine == 'google':
            sites = search(query + " filetype:csv OR filetype:txt", num_results=10)

        # >>>> Busca sites relacionados à query no DuckDuckGo - precisa melhorar a busca pois não retorna todos os resultados no formato de lista <<<<
        elif engine == 'duckduckgo':
            return_sites = DDGS().text(query + " filetype:csv OR filetype:txt", max_results=15)
            sites = [site['href'] for site in return_sites]
        
        for site in sites:
            try:
                time.sleep(1)  # Add delay between processing each site
                # Verifica se é um arquivo CSV ou TXT
                if site.lower().endswith(('.csv', '.txt')):
                    filename = os.path.basename(urllib.parse.unquote(site))
                    if download_file(site, filename):
                        file_path = os.path.join('arquivos', filename)
                        if not has_emails(file_path):
                            os.remove(file_path)
                        else:
                            print(f"Arquivo com emails encontrado: {filename}")
                
                # Se não for arquivo, tenta buscar links na página
                else:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    response = requests.get(site, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a')
                        
                        for link in links:
                            href = link.get('href')
                            if href and href.lower().endswith(('.csv', '.txt')):
                                full_url = urllib.parse.urljoin(site, href)
                                filename = os.path.basename(urllib.parse.unquote(full_url))
                                if download_file(full_url, filename):
                                    file_path = os.path.join('arquivos', filename)
                                    if not has_emails(file_path):
                                        os.remove(file_path)
                                    else:
                                        print(f"Arquivo com emails encontrado: {filename}")
                                    
            except Exception as e:
                print(f"Erro ao processar {site}: {str(e)}")
                failures += 1
                if failures >= max_failures:
                    print(f"Número máximo de falhas ({max_failures}) atingido. Parando a busca.")
                    return
                time.sleep(5)  # Add longer delay on error
                continue
            
    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        time.sleep(30)  # Add long delay if search fails
        failures += 1
        if failures >= max_failures:
            print(f"Número máximo de falhas ({max_failures}) atingido. Parando a busca.")
            return

def main():

    # aqui você pode adicionar as queries que você quer buscar
    queries = [
        "site:.xyz.br pessoas tipo tal"
    ]
    
    for query in queries:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"\nBuscando por: {query}")
                search_files(query, engine='google')
                break  # If successful, break the retry loop
            except Exception as e:
                print(f"Tentativa {attempt + 1} falhou: {str(e)}")
                if attempt < max_retries - 1:  # If not the last attempt
                    time.sleep(60)  # Wait 1 minute before retrying
                else:
                    print(f"Falha após {max_retries} tentativas para: {query}")

if __name__ == "__main__":
    main()
