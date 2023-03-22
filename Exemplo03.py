from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

options = webdriver.ChromeOptions()
#options.add_argument("--window-size=1980,1020")
options.add_argument("--log-level=3")
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
login_url = 'https://store.steampowered.com/?l=portuguese'

print('Passo 1: Acessar o site da Steam')
try:
    driver.get(login_url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.save_screenshot('tela01.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o site da kabum')
    quit()

print('Passo 2: Pesquisar e acessar a página do jogo "Ultrakill" ')
try:
    action = ActionChains(driver)
    #Cliclar na barra de pesquisa e digitar o nome do jogo
    menu = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.ID,'store_nav_search_term')))
    action.move_to_element(menu).click().send_keys("Ultrakill").perform()
    #Clicar sobre o primeiro resultado que aparece após digitar o nome do jogo
    menu = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search_suggestion_contents"]/a[1]')))
    action.move_to_element(menu).click().perform()

    driver.save_screenshot('tela02.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar a página do jogoj')
    quit()

print('Passo 3: Acessar a página da distribuidora  ')
try:
    action = ActionChains(driver)
    #Acessar a página da distribuidora
    menu = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="game_highlights"]/div[1]/div/div[3]/div[4]/div[2]')))
    action.move_to_element(menu).click().perform()
    #Rolar a página até a seção de jogos
    driver.execute_script("window.scrollBy(0,800)","")
    time.sleep(3)
    #Clicar em "Mais vendidos
    menu = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="filter_box"]/div[1]/a[2]')))
    action.move_to_element(menu).click().perform()
    #Clicar no filtro "Jogos"
    menu = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.ID,'filter_app_type_game')))
    action.move_to_element(menu).click().perform()

    driver.save_screenshot('tela03.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar página da distribuidora')
    quit()

print('Passo 4: Gravar no nome dos jogos e seus preços')
try:
    tabela = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[7]/div[6]/div[4]/div[4]/div/form/div[2]/div/div[2]')))
    conteudo_html = tabela.get_attribute('outerHTML')
    lista = BeautifulSoup(conteudo_html,'html.parser')

    with open('lista_jogos.csv','w') as arquivo:
        for tabelas in lista.find_all('div',{'class':'landingTable'}):
            linha = ''
            for tabela in tabelas.find_all('div',{'class':'recommendation'}):
                linha=''
                for jogos in tabela.find_all('span',{'class':'color_created'}):
                    linha += jogos.text
                for data in tabela.find_all('span',{'class':'curator_review_date'}):
                    linha +='\t'+data.text

             #print(linha)
            arquivo.write(linha+'\n')
    arquivo.close

    with open('lista_jogos.html','w') as arquivo:
        arquivo.write(str(conteudo_html))
    arquivo.close()
except:
    driver.quit()
    print('Erro ao salvar lista de jogos e preços')
    quit()