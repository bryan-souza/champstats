# ChampStats API

Nosso objetivo é juntar as informações referentes aos mais diversos campeonatos de e-sports em um unico lugar

## Execução

Você pode executar a API como um container _standalone_ ou utilizando Docker Compose.

### Para executar em modo _standalone_:

Primeiro, é necessário que você construa o container localmente
```shell
docker build -t champstats:latest . 
```

Agora, para executar o container:
```shell
docker run -e DB_URL=mongodb://[usuario]:[senha]@[host]:[porta] champstats:latest
```

### Para executar utilizando docker-compose

Deixamos um arquivo `docker-compose.yml` no repositório para facilitar o _deploy_.
Primeiramente, você deve modificar o arquivo `docker-compose.yml`, alterando
o nome de usuário root e sua respectiva senha (linhas 15 e 16, respectivamente).
Após isso, você deve alterar a URL passada como variável de ambiente para o
container da API (linha 30).

Por fim, execute o comando abaixo para construir a imagem do container e fazer o
_deploy_:
```shell
docker-compose up --build
```
