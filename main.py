from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Abrindo o navegador 
navegador = webdriver.Chrome()

#Acessando o Google/duckduckgo (Infelizmente ao acessar o google, caimos no recaptcha)
navegador.get("https://duckduckgo.com")
navegador.maximize_window()

#Pesquisando botão de search do google
pesquisa_google = navegador.find_element(By.NAME, "q")

#Clicando no botão
pesquisa_google.click()
time.sleep(2)

#Escrevendo no botão de pesquisa
pesquisa_google.send_keys("cases de agente de IA")
pesquisa_google.send_keys(Keys.RETURN)
time.sleep(2)

#Crio o array para receber titulos e links
titulos_links = []

#Extraindo links e títulos dos sites
c = 0
while c != 2:
    resultados = navegador.find_elements(By.CSS_SELECTOR, 'h2 a span')
    for sites in resultados:
        titulo = sites.text # Pegando o título do <span>
        link = sites.find_element(By.XPATH, './ancestor::a').get_attribute("href") # Pegando o link da tag <a>

        if (titulo and link): #se for true guardamos
            titulos_links.append((titulo, link))

    # Scroll pra baixo pra que botão apareça
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Acho botão para carregar mais
    bottom_more = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.ID, "more-results"))
    )
    bottom_more.click()
    c += 1

# for titulo, link in titulos_links:
#     print(f"Título: {titulo}\n Link: {link}\n")

# nome do arquivo TXT
arquivo_txt = "resultados_busca.txt"

# Salvando os dados no arquivo TXT
with open(arquivo_txt, mode='w', encoding='utf-8') as file:
    for titulo, link in titulos_links:
        file.write(f"Título: {titulo}\nLink: {link}\n\n")

print(f"Os dados foram salvos no arquivo: {arquivo_txt}")
