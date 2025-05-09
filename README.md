# flask
# Criação de ambientes virtuais e execução da aplicação
Para a utilização de ambos tutoriais, certifique-se que o Python está instalado na sua máquina.
## Windows
_ps.: Os passos **2-5** só precisam ser executados se ocorrer erro para a criação do ambiente virtual._
1. Crie o diretório que será utilizado
2. Acesse o Power Shell
3. Navegue até o diretório WINDOWS/system32
4. Escreva na linha de comando:  ```Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned```
5. Após isso, confirme com "S"
6. Abra o cmd e navegue até o diretório criado no passo 1.
7. Crie o ambiente virtual com o comando: ```py -m venv .env```
8. Ative o ambiente virtual com o comando: ```.\.env\Scripts\activate```
9. Instale o flask no seu ambiente virtual com o código: ```pip install flask```
10. Com a aplicação já feita, execute a aplicação com o código: ```flask run --debug```
11. Para sair do ambiente virtual, escreva na linha de comando: ```deactivate```
#
## Linux
1. Crie o diretório que será utilizado.
2. Acesse o Terminal.
3. Navegue até o diretório criado no passo 1.
4. Para criar o ambiente virtual, escreva na linha de comando: ```python3 -m venv .env```
5. Para acessar o ambiente virtual
