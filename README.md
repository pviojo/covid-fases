# Covid Fases

Script que genera un archivo con los periodos de cada comuna según fase del plan paso a paso y sus casos activos al comienzo y fin. **Se actualiza en la siguiente hora decambios en los origenes de datos.**


## Prerequisitos

* [Docker](https://store.docker.com/search?offering=community&type=edition)
* [Docker-compose](https://docs.docker.com/compose/install/)

## Como usarlo

````
docker-compose run service python process.py
`````

Al ejecutarlo genera un archivos en la carpeta `output` con los resultados.

* output-{date}.csv: Listado de todos los periodos por comuna (para la fecha de ejecución)
* latest.csv: Listado de todos los periodos por comuna (Último archivo generado)
* current_fases-{date}.csv: Listado del periodo actual en que se encuentra cada comuna (para la fecha de ejecución)
* current_fases.csv: Listado del periodo actual en que se encuentra cada comuna (Último archivo generado)
* current_fase-{date}-{paso}.csv: Listado del periodo actual en que se encuentra cada comuna, filtrado por comunas del paso {paso} (para la fecha de ejecución)
* current_fase-{paso}.csv: Listado del periodo actual en que se encuentra cada comuna, filtrado por comunas del paso {paso} (Último archivo generado)


Cada fila corresponde a un periodo de la comuna con paso, fecha de inicio y fin, activos al inicio y fin y variación de casos (absoluta y porcentual)

Origen de datos:

* https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto19
* https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto74

## Licencia

[MIT](https://opensource.org/licenses/MIT)
