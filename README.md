# tp-aa
Tp de la materia Aprendizaje Automático 2016

##

## Cómo correrlo

1. Dataset

Bajarse el dataset y meterlo en `/data`. Renombrar `ham_dev.json` y `spam_dev.json` a `ham.json` y `spam.json` a secas

Luego, partir el set de datos en desarrollo y test

Correr
```
$ python split_set.py
```

(correr con `--help` para opciones)

3. Instalar dependencias

Asumimos que tenemos python 2.7.12 (fíjense de instalar esta versión) y con pip corriendo.

Nos paramos en el directorio del proyecto, y hacemos

```
$ pip install -r requirements.txt
```

Esto instala todas las dependencias que estamos usando (Numpy, IPython, Matplotlib)


4. Correr el ejemplo

```
$ python baseline.py
```

o correr directamente el nuestro

```
$ python main.py
```