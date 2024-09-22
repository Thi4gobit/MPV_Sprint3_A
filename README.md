# MPV_Sprint3_A

Este pequeno projeto faz parte do MVP do módulo da disciplina **Desenvolvimento Back-end Avançado** 

A aplicação é utilizada para registro e consultas de treinos de ciclismo.

As principais tecnologias que serão utilizadas aqui é o:
 - [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)

---
### Interoperabilidade

Esta aplicação interage com outra API também escopo deste MVP. Para visualizar a outra API acesse:
 - [MPV_Sprint3_B](https://github.com/Thi4gobit/MVP_Sprint3_B)

Para testes com interoperabilidade recomenda-se a execução do **MPV_Sprint3_B** antes da execução desta aplicação.

---
### Instalação

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando a aplicação

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---
### Acesso no browser

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
### Importante!

Para garantir a interoperabilidade das aplicações, execute no docker conforme mostrado adiante ou ajuste a linha de código em `app.py` conforme a configuração da aplicação em **MPV_Sprint3_B**. Por exemplo:

```py
EXTERNAL_API_URL = "http://localhost:8000/workouts"
```

---
### Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Cosiderando a interoperabilidade com o **MPV_Sprint3_B** crie uma rede para inerligar as duas aplicações.

Para criar uma rede no docker execute **como administrador** o seguinte comando:

```
$ docker network create mvp
```

Para verificar se a rede foi criada execute:

```
$ docker network ls
```

Confira se a rede foi criada.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t flask .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d --name flask --network mvp -p 5000:5000 flask
```

Uma vez executado, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### Dicas

>Se o nome dado a imagem no docker em **MPV_Sprint3_B** for diferente de **django**, ajuste a linha de código em `app.py`:
>
>```py
>EXTERNAL_API_URL = "http://django:8000/workouts"
>```
>
>Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
