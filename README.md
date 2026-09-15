# Agendamento Inteligente

Mini sistema web de agendamento desenvolvido como parte de um desafio técnico Full Stack.

O sistema permite que o usuário escolha uma data, consulte os horários disponíveis, selecione um horário e realize um agendamento. Os dados são persistidos em banco de dados e a disponibilidade considera finais de semana, feriados e horários já ocupados.

## Funcionalidades

- Seleção de data para agendamento
- Consulta de horários disponíveis
- Bloqueio de finais de semana
- Bloqueio de feriados
- Horário de funcionamento das 08:00 às 18:00
- Duração de 1 hora por agendamento
- Bloqueio de horários já ocupados
- Criação de agendamento
- Persistência dos agendamentos em banco de dados
- Retorno de confirmação após o agendamento

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- Pytest

### Frontend

- React
- Vite
- JavaScript
- CSS

## Integração com API de feriados

O backend realiza o consumo da API pública de feriados da Nager para verificar a disponibilidade da data selecionada.

API utilizada:

```text
https://date.nager.at/api/v3/PublicHolidays/2026/BR
```

A consulta é realizada pelo backend durante a validação da disponibilidade da data.

## Regras de negócio

- O horário de funcionamento é das 08:00 às 18:00.
- Cada agendamento possui duração de 1 hora.
- Não é permitido agendar em finais de semana.
- Não é permitido agendar em feriados.
- Não é permitido agendar em horários já ocupados.
- Horários fora da faixa de funcionamento são rejeitados.

## API REST

### Consultar horários disponíveis

```http
GET /available?date=2026-02-10
```

Retorna os horários disponíveis para a data informada.

### Criar agendamento

```http
POST /appointments
```

Exemplo de requisição:

```json
{
  "date": "2026-02-10",
  "time": "10:00:00"
}
```

### Listar agendamentos

```http
GET /appointments
```

Retorna os agendamentos persistidos no banco de dados.

## Fluxo da aplicação

```text
Usuário escolhe uma data
        ↓
Frontend consulta o backend
        ↓
Backend consulta a API de feriados
        ↓
Backend valida a data
        ↓
Backend verifica horários ocupados
        ↓
Backend retorna os horários disponíveis
        ↓
Usuário seleciona um horário
        ↓
Backend valida e salva o agendamento
        ↓
Frontend exibe a confirmação
```

## Testes

O backend possui testes automatizados para validar as principais regras de disponibilidade e agendamento.

Para executar os testes:

```bash
cd backend
python -m pytest
```

Validação realizada durante o desenvolvimento:

```text
8 passed
```

Também foram realizadas validações manuais das rotas da API e do fluxo de agendamento pelo frontend.

## Estrutura do projeto

```text
agendamento-inteligente/
├── .gitignore
├── README.md
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── availability.py
│   │   │   ├── holidays.py
│   │   │   └── schedule.py
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── tests/
│   │   └── test_availability.py
│   │
│   └── requirements.txt
│
└── frontend/
    ├── public/
    │   └── favicon.svg
    ├── src/
    │   ├── App.css
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    ├── eslint.config.js
    ├── index.html
    ├── package-lock.json
    ├── package.json
    └── vite.config.js
```

## Como executar

### Backend

Na raiz do projeto:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie o servidor:

```bash
python -m uvicorn app.app:app --reload
```

O backend ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa da API está disponível em:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Abra outro terminal e acesse a pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

Mantenha o backend em execução enquanto utilizar o frontend.

## Validação do frontend

Para executar a verificação do código:

```bash
npm run lint
```

Para gerar o build:

```bash
npm run build
```

## IA como copiloto de desenvolvimento

A Inteligência Artificial foi utilizada como ferramenta de apoio durante o desenvolvimento, atuando como copiloto para exploração de soluções, revisão de código, identificação de problemas e documentação.

A organização do projeto, as decisões de arquitetura, a implementação das funcionalidades, a validação das regras de negócio e a execução dos testes foram conduzidas e revisadas por mim ao longo do desenvolvimento.