Claro, aquí tienes el mismo contenido con el formato solicitado:

---

# Git y GitHub

Aunque los conceptos y la historia detrás de la creación de Git son fascinantes, es esencial comprender que este sistema de control de versiones se maneja principalmente a través de comandos de Linux. Esto se debe a que el creador de Linux, Linus Torvalds, fue quien también creó Git.

---

## Comandos Básicos de Linux

```bash
# Listado de todos los archivos y directorios en el directorio actual
ls
```
- **Descripción**: Este comando muestra una lista de todos los archivos y directorios en el directorio actual.

```bash
# Acceder a un directorio específico
cd <nombre_de_la_carpeta>

# Ejemplo
cd TuCarpeta

# Volver al directorio anterior
cd ..
```
- **Descripción**: `cd` es el comando usado para cambiar el directorio actual. Puedes utilizar la tecla `Tab` para autocompletar nombres de carpetas y archivos.

```bash
# Mostrar la ruta completa del directorio actual
pwd
```
- **Descripción**: `pwd` (print working directory) muestra la ruta completa del directorio en el que te encuentras actualmente.

```bash
# Crear una nueva carpeta o directorio
mkdir <nombre_de_tu_carpeta>
```
- **Descripción**: `mkdir` (make directory) se utiliza para crear un nuevo directorio con el nombre especificado.

```bash
# Ver los commits realizados
git log
```
- **Descripción**: `git log` Este comando te permite ver todos los commits realizado del directorio en el que te encuentras.

```bash
# Historial completo de commits, aunque se hayan cortado las ramas
git reflog
```
- **Descripción**: `git checkout` Este comando nos permite ver el historial completo de las ramas, aunque hayamos hecho  un git reset --hard o hayamos cortado las otras ramas.

```bash
# Para situarnos en un punto concreto
git checkout <hash del commit>
```
- **Descripción**: `git checkout` Este comando te permite volver a una version pasada de tu proyecto, pero debera haber sido hecha con un commit.

```bash
# Resetea todo hasta el ultimo commit
git reset
```
- **Descripción**: `git reset` Este comando te permite volver hacia atras al ultimo commit directamente.
---
