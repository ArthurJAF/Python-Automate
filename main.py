from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Initialize the driver
def initializing():
    #Abrindo o navegador 
    navegador = webdriver.Chrome()
    #Acessando o Google/duckduckgo (Infelizmente ao acessar o google, caimos no recaptcha)
    navegador.get("https://duckduckgo.com")
    navegador.maximize_window()

    return navegador

#Search for the parameter
def search(navegador, term):
    #Pesquisando botão de search do google
    pesquisa_google = navegador.find_element(By.NAME, "q")

    #Clicando no botão
    pesquisa_google.click()
    time.sleep(2)

    #Escrevendo no botão de pesquisa
    pesquisa_google.send_keys(term)
    pesquisa_google.send_keys(Keys.RETURN)
    time.sleep(2)

#Extracting the titles and links 
def extracting_info(navegador, limit=30): 
    
    titulos_links = []  #crio um array para guardar os resultados da pesquisa
    vistos = set() #crio um conjunto

    while True: 
        resultados = navegador.find_elements(By.CSS_SELECTOR, 'h2 a span')

        for sites in resultados:
            titulo = sites.text #Pegando o título do <span>
            link = sites.find_element(By.XPATH, './ancestor::a').get_attribute("href") #Pegando o link da tag <a>

            if (titulo and link and link not in vistos): #se for true guardamos
                titulos_links.append((titulo, link))
                vistos.add(link)

        # Scroll pra baixo pra que botão apareça
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Acho botão para carregar mais
        bottom_more = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "more-results"))
        )
        bottom_more.click()
        
        if (len(titulos_links) >= limit):
            break
        

    return titulos_links

#Saving the result of the search in a txt file
def saving_results_txt(resultados, arquivo_txt):
    # Salvando os dados no arquivo TXT
    with open(arquivo_txt, mode='w', encoding='utf-8') as file:
        for titulo, link in resultados:
            file.write(f"Título: {titulo}\nLink: {link}\n\n")

def main():
    termo_de_busca = "cases de agente de IA" 
    nome_do_arquivo_txt = "resultados_busca.txt" #nome do aqruivo onde vão ser guardadas as informações

    navegador = initializing() #saving the return in a variable
    search(navegador, termo_de_busca)
    resultados = extracting_info(navegador)
    saving_results_txt(resultados, nome_do_arquivo_txt)

    print(f"Os dados foram salvos no arquivo: {nome_do_arquivo_txt}")
    navegador.quit()

main()
