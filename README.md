
# Back Sistema Digital

Esta API utiliza Django, Django REST Framework e JWT para gerenciar usuários e permissões. A seguir, estão descritas as instruções de instalação e os endpoints disponíveis na aplicação.

---

## Instruções de Instalação

1. **Clone o repositório via SSH:**

   ```bash
   git clone git@github.com:Prodos-Digital/back-sistema-escolar.git
   cd back-sistema-escolar
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o arquivo `.env` na raiz do projeto** (ao lado de `manage.py`) com o seguinte conteúdo:

   ```env
   DB_HOST=localhost
   DB_PORT=5433
   DB_NAME=educa_digital
   DB_USER=postgres
   DB_PASSWORD=123

   SECRET_KEY=SUA-SECRET-KEY-AQUI
   DEBUG=True
   ```

5. **Realize as migrações e crie um superusuário:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Inicie o servidor:**

   ```bash
   python manage.py runserver
   ```

   A API ficará disponível em `http://127.0.0.1:8000/`.

---

## API Endpoints (Views)

### 1. Cadastro de Usuário (User Registration)

- **Endpoint:** `POST /users/register/`
- **Descrição:** Cria um novo usuário com `is_active=false` (inativo por padrão).
- **Exemplo de requisição:**

  ```bash
  curl -X POST http://127.0.0.1:8000/users/register/ \
    -H "Content-Type: application/json" \
    -d '{
          "username": "jose",
          "email": "jose@example.com",
          "first_name": "José",
          "last_name": "Silva",
          "password": "senha123"
        }'
  ```

- **Resposta (201 Created):**

  ```json
  {
    "id": 1,
    "username": "jose",
    "email": "jose@example.com",
    "first_name": "José",
    "last_name": "Silva",
    "is_active": false,
    "is_staff": false,
    "permissions": []
  }
  ```

---

### 2. Login (CustomLoginView)

- **Endpoint:** `POST /users/login/`
- **Descrição:** Realiza o login via JWT. Se o usuário estiver ativo, retorna os tokens (access e refresh) e os dados completos do usuário, incluindo a lista de permissões.
- **Exemplo de requisição:**

  ```bash
  curl -X POST http://127.0.0.1:8000/users/login/ \
    -H "Content-Type: application/json" \
    -d '{
          "username": "jose",
          "password": "senha123"
        }'
  ```

---

### 3. Detalhes, Atualização e Deleção de Usuário (User Detail)

- **Endpoint:** `GET, PUT/PATCH, DELETE /users/<id>/`

---

### 4. Endpoints de Permissões (Permission Endpoints)

- **Localização:** `/users/permissions/` (utiliza ViewSet)

---

### 5. Adicionar/Remover Permissão de um Usuário

- **Endpoint para adicionar permissão:** `POST /users/<id>/add-permission/`
- **Endpoint para remover permissão:** `POST /users/<id>/remove-permission/`

---

> **Nota:**  
> Para todos os endpoints que exigem autenticação, inclua o cabeçalho:
>
> ```
> Authorization: Bearer <seu_token_access>
> ```
