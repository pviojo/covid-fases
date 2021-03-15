# Covid Fases

Script que genera un archivo con los periodos de cada comuna según fase del plan paso a paso y sus casos activos al comienzo y fin.


## Prerequisitos

* [Docker](https://store.docker.com/search?offering=community&type=edition)
* [Docker-compose](https://docs.docker.com/compose/install/)

## Como usarlo

````
docker-compose run service python process.py
`````

Al ejecutarlo genera un archivo en la carpeta `output` con el resultado.

Cada fila corresponde a un periodo de la comuna con paso, fecha de inicio y fin, activos al inicio y fin y variación de casos (absoluta y porcentual)

Origen de datos:

* https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto19
* https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto74