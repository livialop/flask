# Estudo para a 2a prova do 1o bimestre.
A avaliação será focada na autenticação de usuários utilizando flask-login. Pedi para o DeepSeek fazer um exercício para mim:
 

### **Exercício: Autenticação com Flask + Flask-Login (Sem Banco de Dados)**  
**Objetivo:**  
Criar um sistema de autenticação com registro, login e logout, usando **cookies**, **sessões** e **flash messages**, sem banco de dados.

---

### **Instruções Passo a Passo:**

#### **1. Estrutura do Projeto**  
Mantenha a mesma estrutura de pastas, mas remova a pasta `models` (não usaremos SQLAlchemy).

#### **2. Armazenamento em Memória**  
- No `app.py`, crie um **dicionário global** para simular o banco de dados:  
  ```python
  users_db = {}  # Formato: {username: {"email": "user@exemplo.com", "password_hash": "hash_da_senha"}}
  ```

#### **3. Modelo de Usuário (Simplificado)**  
- No `app.py`, defina uma classe `User` com:  
  - Métodos obrigatórios do Flask-Login (`is_authenticated`, `get_id`, etc.).  
  - Um método para verificar senhas (use `werkzeug.security.check_password_hash`).

#### **4. Rotas Principais (`app.py`)**  
- **Rota `/register` (`register.html`):**  
  - Valide se o `username` já existe em `users_db`.  
  - Hasheie a senha com `generate_password_hash` e armazene no dicionário.  
  - Mensagem flash: "Registro bem-sucedido!".  

- **Rota `/login` (`login.html`):**  
  - Verifique se o `username` existe em `users_db` e se a senha está correta.  
  - Use `login_user()` e `session` para manter o login.  
  - Mensagem flash para erros: "Usuário ou senha inválidos.".  

- **Rota `/logout`:**  
  - Use `logout_user()` e limpe a sessão.  

- **Rota `/profile` (protegida com `@login_required`):**  
  - Mostre dados do usuário logado (recuperados de `users_db`).

#### **5. Templates (HTML + CSS)**  
- **`base.html`:**  
  - Mostre mensagens flash com `get_flashed_messages()`.  
  - Links condicionais (ex: "Logout" só aparece se logado).  
- **Formulários (`login.html`, `register.html`):**  
  - Estilize com CSS (campos obrigatórios, feedback de erros).

#### **6. Sessões e Cookies**  
- Use `session` para armazenar o `username` após o login.  
- Teste no navegador (F12 → Application → Cookies) para ver o cookie `session`.  

#### **7. Funcionalidades Extras (Opcionais)**  
- Adicione "Lembre-me" no login (use `remember=True` em `login_user`).  
- Página `/admin` restrita a um usuário específico (ex: `username="admin"`).

---

### **O Que Será Testado:**  
1. **Registro:**  
   - Impede usernames duplicados.  
   - Senhas são hasheadas antes de armazenar.  
2. **Login/Logout:**  
   - Sessão persiste até logout ou fechar navegador.  
   - Cookie `session` é criado corretamente.  
3. **Proteção de Rotas:**  
   - Acesso a `/profile` sem login → redireciona para `/login`.  
4. **Mensagens Flash:**  
   - Aparecem após ações (ex: "Você saiu" após logout).

---

### **Dicas:**  
- Para hashear senhas:  
  ```python
  from werkzeug.security import generate_password_hash, check_password_hash
  password_hash = generate_password_hash("senha123")
  check_password_hash(password_hash, "senha123")  # → True/False
  ```
- Use `session.clear()` no logout para limpar dados.  

**Observação:** Como não há banco de dados, os usuários serão **perdidos ao reiniciar o servidor**. Isso é intencional para simplificar o exercício.  

Boa prática!