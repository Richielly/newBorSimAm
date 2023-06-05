import flet as ft
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep


def get_options(username, password):
    url = "https://servicos.tce.pr.gov.br/tcepr/municipal/simam/Paginas/Consulta.aspx"

    try:
        driver = webdriver.Firefox()
        driver.get(url)

        # Preencher campos de usuário e senha
        username_field = driver.find_element(By.ID, "Login")
        username_field.send_keys(username)
        password_field = driver.find_element(By.ID, "Senha")
        password_field.send_keys(password)

        # Submeter o formulário de login
        password_field.submit()

        sleep(1)

        # Verificar se o elemento #idPessoaJuridica está presente
        element_id_pessoa_juridica = driver.find_element(By.CSS_SELECTOR, "#idPessoaJuridica")

        # Obter todas as opções do elemento select
        select_element = Select(element_id_pessoa_juridica)
        options = [option.text for option in select_element.options]

        return options
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        driver.quit()


def main(page: ft.Page):
    page.title = "Autenticação de Usuário"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    txt_username = ft.TextField(label="Usuário:", value="80170641953", width=300)
    txt_password = ft.TextField(label="Senha:", value="Dirlei1310", width=300)
    btn_login = ft.TextButton(text="Login", width=200)
    lbl_result = ft.Text(size=20)
    select_options = None

    def on_login_click(e):
        nonlocal select_options

        username = txt_username.value.strip()
        password = txt_password.value

        if username and password:
            select_options = get_options(username, password)

            if select_options:
                lbl_result.value = "Opções obtidas com sucesso!"
                lbl_result.color = ft.colors.GREEN
                # print(select_options)  # Exemplo: Imprimir as opções no console
                for opt in select_options:
                    drop_entidade.options.append(ft.dropdown.Option(opt))
                page.update()
                return select_options
            else:
                lbl_result.value = "Falha no login. Verifique suas credenciais."
                lbl_result.color = ft.colors.RED
        else:
            lbl_result.value = "Informe um usuário e senha válidos."
            lbl_result.color = ft.colors.RED

        page.update()

    btn_login.on_click = on_login_click
    page.add(txt_username)
    page.add(txt_password)
    page.add(btn_login)
    page.add(lbl_result)
    drop_entidade = ft.Dropdown(width=800)
    page.add(drop_entidade)


if __name__ == "__main__":
    ft.app(target=main)
