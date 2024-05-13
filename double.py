import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Função para fazer login
def fazer_login(driver, email, senha):
    print("Fazendo login...")
    driver.get('https://blaze1.space/pt/games/double?modal=auth&tab=login')
    time.sleep(3)
    campo_email = driver.find_element(By.XPATH, '//*[@id="auth-modal"]/div/form/div[1]/div/input')
    campo_email.send_keys(email)
    campo_senha = driver.find_element(By.XPATH, '//*[@id="auth-modal"]/div/form/div[2]/div/input')
    campo_senha.send_keys(senha)
    botao_login = driver.find_element(By.XPATH, '//*[@id="auth-modal"]/div/form/div[4]/button')
    botao_login.click()
    print("Login realizado com sucesso.")

# Função para obter os 5 resultados anteriores
def resultados():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTY4MTkwOSwiYmxvY2tzIjpbXSwiaWF0IjoxNzE1Mzk5OTI4LCJleHAiOjE3MjA1ODM5Mjh9.LI0bHYdA0-M-L6fOuTaTz0OyRWsYcnyOhRvx6lr6dKY',
        'device_id': 'c46fd3f5-bcbc-4192-a762-87c0ce63ffe5',
        'priority': 'u=1, i',
        'referer': 'https://blaze1.space/pt/games/double',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'session_id': '1713338467776',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-client-language': 'pt',
        'x-client-version': 'v2.1971.0',
    }

    response = requests.get('https://blaze1.space/api/roulette_games/recent', headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Retorna o mais recente
        results = [result['color'] for result in data[:1]]
        return results

# Inicializar o driver do Selenium
driver = webdriver.Chrome()  # Você precisa do WebDriver do Chrome ou de outro navegador

# Login
fazer_login(driver, "email@gmail.com", "@senha")

# Inicializar a variável para armazenar o resultado anterior
resultado_anterior = None

campo_input = None  # Definindo campo_input fora do bloco try

# Variável para rastrear se o campo de input já foi preenchido nesta rodada
input_preenchido = False

# Loop
while True:
    # Obtém os 5 resultados mais recentes
    results = resultados()

    # Verifica se houve alteração no resultado mais recente
    if resultado_anterior != results:
        # Atualiza o resultado anterior
        resultado_anterior = results
        # Printa os resultados atuais apenas se houver uma alteração
        print('Resultados Cor:', results)
        
        # Reinicia a variável de controle de ação para cada nova rodada
        acao_executada = False
        # Reinicia a variável de controle do jogo iniciado para cada nova rodada
        jogo_iniciado = False
        # Reinicia a variável de controle do campo de input preenchido para cada nova rodada
        input_preenchido = False

    # Loop através dos resultados e realize ações com base neles
    for result in results:
        if result == 0 or result == 1:
            try:
                # Verifica se a ação já foi executada nesta rodada
                if not acao_executada:
                    # Localiza o botão com a classe "grey double" e texto "2x"
                    botao_2x = driver.find_element(By.XPATH, '//button[@class="grey double" and contains(text(), "2x")]')
                    botao_2x.click()
                    print("Clicando em '2x'.")
                    # Define a variável de controle de ação como True após executar a ação
                    acao_executada = True
            except NoSuchElementException:
                print("Botão '2x' não encontrado.")
        elif result == 2:
            try:
                # Verifica se o campo de input já foi preenchido nesta rodada
                if not input_preenchido:
                    # Espera até que o campo de input esteja disponível
                    if campo_input is None:
                        campo_input = driver.find_element(By.XPATH, '//div[@class="input-field-wrapper"]/input[@class="input-field"]')
                    # Verifica se há um valor presente no campo de entrada antes de limpar
                    if campo_input.get_attribute("value"):
                        # Limpa o campo de input se houver um valor presente
                        campo_input.clear()
                        print("Valor do campo de input limpo.")
                    # Insere o valor 0.10 no campo de input
                    campo_input.send_keys("0.10")
                    print("Valor inserido automaticamente: 0.10")
                    # Define a variável de controle do campo de input preenchido como True após preencher o campo
                    input_preenchido = True
                    time.sleep(2)
            except NoSuchElementException:
                print("Campo de input não encontrado.")

    # Verifica se o jogo já foi iniciado
    if not jogo_iniciado:
        try:
            WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//button[text()="Esperando"]')))
            botao_comecar_jogo = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Começar o jogo"]')))
            botao_comecar_jogo.click()
            print("Clicando em 'Começar o jogo'.")
            # Define a variável de controle do jogo iniciado como True após iniciar o jogo
            jogo_iniciado = True
        except TimeoutException:
            print("Timeout ao tentar encontrar o botão 'Começar o jogo'.")

    time.sleep(3)
