from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd
import requests
import io
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=chrome_options)

def delete_files():
    for filename in ['WebTable.csv', 'datatable01.csv', 'datatable02.csv']:
        if os.path.exists(filename):
            os.remove(filename)

def download_file(url, file_name):
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

def login(driver, username, password):
    driver.get('https://rpaexercise.aisingapore.org/')
    driver.maximize_window()
    sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="panel1a-content"]/div/p/div[3]/a').click()
    driver.find_element(By.XPATH, '//*[@id="outlined-search"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="login"]').click()

def create_jobs():
    dados = pd.read_csv('datatable01.csv')
    df = pd.DataFrame(dados, columns=["jobTitle", "jobDescription", "hiringDepartment", "educationLevel", "postingStartDate", "postingEndDate", "remote", "jobType"])

    jobs_ids = []
    for row in df.itertuples():
        nav.find_element(By.XPATH, '//*[@id="newJobPosting"]').click()
        nav.find_element(By.XPATH, '//*[@id="jobTitle"]').send_keys(row[1])
        nav.find_element(By.XPATH, '//*[@id="jobDescription"]').send_keys(row[2])
        
        departamento_dropdown = Select(nav.find_element(By.XPATH, '//*[@id="hiringDepartment"]'))
        departamento_dropdown.select_by_value(row[3])
        nivel_educacao_dropdown = Select(nav.find_element(By.XPATH, '//*[@id="educationLevel"]'))
        nivel_educacao_dropdown.select_by_value(row[4])

        nav.find_element(By.XPATH, '//*[@id="postingStartDate"]').send_keys(row[5])
        nav.find_element(By.XPATH, '//*[@id="postingEndDate"]').send_keys(row[6])

        sleep(0.5)

        if row[7] == 'Yes':
            nav.find_element(By.XPATH, '//*[@id="remote"]/label[1]/span[1]/span[1]').click()
        elif row[7] == 'No':
            nav.find_element(By.XPATH, '//*[@id="remote"]').click()
            
        if row[8] == 'Full-time':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[1]/span[1]').click()
        elif row[8] == 'Full-time/Permanent':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[1]/span[1]').click()
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[4]/span[1]').click()

        if row[8] == 'Part-time':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[2]/span[1]').click()

        elif row[8] == 'Part-time/Temp':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[2]/span[1]').click()
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[3]/span[1]').click()

        if row[8] == 'Temp':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[3]/span[1]').click()   
        
        if row[8] == 'Permanent':
            nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[8]/div/label[4]/span[1]').click()   

        sleep(0.5)
        
        nav.find_element(By.XPATH, '//*[@id="submit"]').click()

        # Esperar até que o elemento com o ID "jobId" esteja presente na página
        try:
            job_id = nav.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[1]/div/input').get_attribute('value')
            jobs_ids.append(job_id)
        except Exception as e:
            print("Erro ao tentar encontrar o ID do trabalho:", e)


# Configurações iniciais
nav = setup_driver()

# Remover arquivos existentes
delete_files()


# Baixar arquivo 1 e fazer login
download_file('https://docs.google.com/uc?export=download&id=1tEHImtjYPP2PPeeelD3nIPcaKFmfSJF8', 'datatable01.csv')
login(nav, 'jane007', 'TheBestHR123')





# # Iterar sobre os IDs dos trabalhos e clicar nos links
# for job_id in jobs_ids:
#     nav.find_element(By.XPATH, f'//a[@href="/jobs/{job_id}"]/button/span[text()="View Applicant List"]').click()

#     # Logica do loop para pegar os dados da tabela
#     tabela = nav.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/table').get_attribute('innerText')

#     tabela_io = io.StringIO(tabela)
#     dados = pd.read_csv(tabela_io, delimiter='\t')

#     dados.to_csv('WebTable.csv', mode='a', index=None, header=True)

#     tabela_df = pd.DataFrame(dados, columns=["Full Name", "Email", "Address", "Education Level", "Pre-screening Score"])

#     # Tratamento dos dados
#     tabela_df = tabela_df.dropna(how='all', axis=1)
#     tabela_df = tabela_df.dropna()

#     # Lógica para checar linha a linha se o candidato esta aprovado ou não
#     contador = 0
#     graduacao = nav.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/div[10]/p').get_attribute('innerText')

#     for row in tabela_df.itertuples():
#         sleep(0.5)
#         contador += 1

#         # Lógica para clickar no botão aprovar ou rejeitar
#         if row[4] == graduacao and row[5] >= 70:
#             nav.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[{contador}]/td[7]/div/div/button[1]').click()
#         elif row[4] != graduacao or row[5] < 70:
#             nav.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[{contador}]/td[7]/div/div/button[2]').click()  

#     nav.find_element(By.XPATH, '//*[@id="backToList"]/span[1]').click()


# # Baixando segundo arquivo para fazer a verificação
# url = 'https://docs.google.com/uc?export=download&id=1tEHImtjYPP2PPeeelD3nIPcaKFmfSJF8'
# caminho_arquivo = 'datatable02.csv'
# response = requests.get(url)

# with open(caminho_arquivo, 'wb') as file:
#     file.write(response.content)


# url = 'https://docs.google.com/uc?export=download&id=1tEHImtjYPP2PPeeelD3nIPcaKFmfSJF8'
# file_name = 'datatable01.csv'

# # Caminho para os arquivos CSV
# caminho_arquivo1 = "datatable01.csv"
# caminho_arquivo2 = "datatable02.csv"

# # Carregando os dados dos arquivos CSV em DataFrames
# df1 = pd.read_csv(caminho_arquivo1)
# df2 = pd.read_csv(caminho_arquivo2)

# # Verificando se os DataFrames são iguais
# if df1.equals(df2):
#     print("Não existem novas atualizações.")
#     nav.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div[2]/div/button[2]').click()
#     sleep(0.2)
#     nav.quit()
# else:
#     print("Os arquivos CSV possuem diferenças nos dados.")