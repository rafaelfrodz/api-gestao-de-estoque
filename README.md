# 📦 API de Gestão de Estoque

Esta é uma API para gestão de estoque, desenvolvida com Flask, PostgreSQL e Redis. O sistema foi projetado para ser executado em containers Docker, oferecendo uma infraestrutura de fácil replicação e escalabilidade.

## ✅ Pré-requisitos

Antes de iniciar, certifique-se de que você tem as seguintes ferramentas instaladas:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Como Executar a Aplicação

1.  Clone o repositório:
    ```bash
    git clone [URL_DO_REPOSITORIO](https://github.com/rafaelfrodz/api-gestao-de-estoque)
    cd api-gestao-estoque
    ```
2.  Copie o arquivo de exemplo de variáveis de ambiente:
    ```bash
    cp .env.example .env
    ```
    Ajuste as variáveis no arquivo `.env` conforme necessário.
    
3.  Suba os containers com Docker Compose:
    ```bash
    docker compose up -d
    ```

A aplicação estará disponível em:

📍 http://localhost:5001

## 🧩 Serviços Disponíveis

| Serviço     | URL / Porta        |
| ----------- | ------------------ |
| API Flask   | http://localhost:5001 |
| PostgreSQL  | localhost:5432       |
| Redis       | localhost:6379       |

## 🧪 Executando os Testes

Para rodar os testes automatizados dentro do container:

```bash
docker-compose exec web pytest --cov=app tests/ --cov-report=term-missing
```
## 🛠️ Decisões Técnicas

### 📘 Arquitetura Flask

* Escolhido pela leveza e facilidade de prototipação de APIs.
* Ambiente configurado com debug ativo para desenvolvimento.

### 🐍 Peewee  
* Sintaxe limpa e de fácil compreensão, ideal para projetos com foco em agilidade e clareza de código.  
* Baixo consumo de recursos e excelente performance para aplicações de pequeno e médio porte.  
* Integração nativa com PostgreSQL, facilitando a manipulação de dados sem perder a legibilidade.

### PostgreSQL

* Banco de dados relacional utilizado como armazenamento principal.
* Versionamento: PostgreSQL 15.
* Inicialização com script `init.sql` automático.
* Healthcheck configurado para monitoramento da disponibilidade.

### Redis

* Usado para cache e controle de sessão.
* Imagem Alpine para leveza e melhor performance.

### 🐳 Containerização

* Docker utilizado para garantir a portabilidade do ambiente.
* Rede interna dedicada: `app-network`.
* Volumes persistentes para dados do banco de dados.
* Healthchecks configurados para garantir a ordem correta de inicialização.

## 📌 Comandos Úteis

* Parar a aplicação:
    ```bash
    docker compose down
    ```
* Ver os logs dos containers:
    ```bash
    docker compose logs -f
    ```

