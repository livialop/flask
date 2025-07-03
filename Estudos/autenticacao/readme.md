# Estudo para a 2a prova do 1o bimestre.
A avaliação será focada na autenticação de usuários utilizando flask-login. Pedi para o DeepSeek fazer um exercício para mim:
 
### Objetivo do Exercício:
Criar um sistema de autenticação com registro, login, logout e proteção de rotas, utilizando cookies, sessões e mensagens flash.

---

### **Instruções Passo a Passo:**

#### **1. Configuração Inicial**
- Crie um ambiente virtual e instale os pacotes necessários (`flask`, `flask-login`, `flask-sqlalchemy`, etc.) no `requirements.txt`.
- Configure o `app.py` para inicializar o Flask, Flask-Login e o banco de dados (SQLite).

#### **2. Modelo de Usuário (`models/user.py`)**
- Defina uma classe `User` com:
  - Campos: `id` (PK), `username` (único), `email` (único), `password_hash`.
  - Métodos exigidos pelo Flask-Login (`is_authenticated`, `is_active`, `get_id`, etc.).
- Adicione um método `set_password` para hashear senhas (use `werkzeug.security`).

#### **3. Rotas Básicas (`app.py`)**
- **Rota `/` (`index.html`):**
  - Página inicial que mostra:
    - "Bem-vindo, [usuário]!" se logado.
    - Links para "Login" ou "Registrar" se anônimo.
- **Rota `/register` (`register.html`):**
  - Formulário com campos: `username`, `email`, `password`, `confirm_password`.
  - Validações:
    - Senhas coincidem.
    - Usuário/email não existem no banco.
  - Após registro, redireciona para login com mensagem flash: "Registro bem-sucedido!".
- **Rota `/login` (`login.html`):**
  - Formulário com `username` e `password`.
  - Verifica credenciais e usa `login_user()` do Flask-Login.
  - Mensagem flash para erros: "Credenciais inválidas.".
- **Rota `/logout`:**
  - Chama `logout_user()` e redireciona para a home com mensagem: "Você saiu.".

#### **4. Templates (HTML + CSS)**
- **`base.html`:** 
  - Layout base com blocos para conteúdo.
  - Inclua mensagens flash (use `get_flashed_messages()`).
  - Links condicionais (ex: mostrar "Logout" apenas se logado).
- **Páginas específicas:**
  - Estilize os formulários com os arquivos CSS correspondentes.
  - Exiba erros de validação nos formulários (se houver).

#### **5. Autenticação e Sessões**
- Use `@login_required` para proteger rotas (ex: `/profile`).
- Configure `login_manager` no `app.py` para gerenciar sessões.
- Teste o cookie de sessão:
  - Verifique no navegador (F12 → Application → Cookies) após login.

#### **6. Funcionalidades Extras (Opcionais)**
- Adicione "Lembre-me" no login (use `remember=True` em `login_user()`).
- Página de perfil (`/profile`) que requer login.

---

### **O Que Será Testado:**
1. **Registro:**
   - Impede usuários/emails duplicados.
   - Hasheia senhas corretamente.
2. **Login/Logout:**
   - Sessão persiste apenas enquanto logado.
   - Cookies são configurados corretamente.
3. **Proteção de Rotas:**
   - Acesso a `/profile` sem login → redireciona para login.
4. **Mensagens Flash:**
   - Aparecem no template após ações (erros, sucessos).

---

### **Dicas:**
- Use `session` para armazenar dados temporários (ex: tentativas de login).
- Para hashear senhas: `generate_password_hash` e `check_password_hash`.

Este exercício cobre todos os conceitos essenciais de autenticação com Flask-Login, incluindo cookies, sessões e mensagens flash. Boa prática!