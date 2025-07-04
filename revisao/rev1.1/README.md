# Tarefa de Revisão: Flask Básico e Conceitos Web
ps.: Revisão feita com o Deepseek.
## Objetivo:
Criar uma pequena aplicação Flask que implemente os conceitos estudados e responda a um questionário teórico.

## Parte 1: Aplicação Flask

Crie uma aplicação Flask chamada `quiz_app.py` com as seguintes rotas e funcionalidades:

1. Rota `/` (página inicial):
   - Deve renderizar um template `index.html`
   - Deve verificar se existe um cookie chamado "username"
   - Se o cookie existir, mostrar "Bem-vindo de volta, [username]!" no template
   - Se não existir, mostrar um link para "/login"

2. Rota `/login`:
   - Métodos GET e POST
   - GET: Renderiza um formulário de login (template `login.html`) com:
     - Campo para nome de usuário
     - Checkbox "Lembrar de mim"
   - POST: Processa o formulário:
     - Se "Lembrar de mim" estiver marcado, define um cookie "username" com o valor digitado
     - Redireciona para a página inicial

3. Rota `/quiz`:
   - Renderiza um template `quiz.html` com o questionário teórico (Parte 2)
   - O template deve usar comandos Python (Jinja2) para:
     - Exibir o nome do usuário (do cookie) se estiver logado
     - Mostrar uma mensagem diferente se for a primeira vez que acessa o quiz

4. Rota `/logout`:
   - Remove o cookie "username"
   - Redireciona para a página inicial

## Parte 2: Questionário Teórico

No template `quiz.html`, inclua o seguinte questionário:

### Métodos e Requisições:
1. Qual a diferença entre os métodos GET e POST em formulários HTML?
2. Como o Flask diferencia o tratamento de requisições GET e POST em uma rota?
3. O que é o objeto `request` no Flask e para que serve?

### Cookies:
4. O que são cookies em aplicações web e para que são usados?
5. Como o Flask permite definir cookies na resposta ao cliente?
6. Quais são as limitações de segurança ao usar cookies?

### Formulários:
7. Como um formulário HTML envia seus dados para o servidor?
8. Qual a importância do atributo `name` nos campos de um formulário?
9. Como o Flask acessa os dados enviados por um formulário?

## Requisitos Técnicos:
- Use `render_template` para todos os templates HTML
- Use `redirect` e `url_for` para navegação entre rotas
- Implemente o cookie com `set_cookie` e `make_response`
- Use comandos Jinja2 (`{% if %}`, `{% for %}`, `{{ variavel }}`) nos templates
- Os templates devem ter uma estrutura HTML básica (DOCTYPE, html, head, body)

## Entrega:
Envie o arquivo `quiz_app.py` e a pasta `templates` com todos os arquivos HTML necessários.

---

Esta tarefa combina a prática de desenvolvimento com Flask e a revisão dos conceitos teóricos importantes. Você precisará demonstrar conhecimento tanto na implementação quanto nas respostas ao questionário.