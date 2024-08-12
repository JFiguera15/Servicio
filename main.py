import datetime
import os.path
import sqlite3
from tkinter import filedialog as fd
import FreeSimpleGUI as sg
from PIL import Image, ImageTk
import ventana_agregar
import ventana_base


def buscar_usuario(cedula, conexion):
    cursor = conexion.cursor()
    cursor.execute("select count(cedula) from usuarios where codigo = '" + cedula + "' ")
    for row in cursor:
        if row[0] == 0:
            return "Cédula no registrada en sistema.", " ", " ", " "
        else:
            cursor.execute(
                "select nombre, apellido, clasificacion, grado, seccion from usuarios where codigo = '" + cedula + "' ")
            for row in cursor:
                nombre = row[0] + " " + row[1]
                clasificacion = row[2]
                carpeta = establecer_carpeta(clasificacion, row[3], row[4])
                guardar_archivo(nombre, cedula, carpeta)
                guardar_acceso(conexion, cedula, carpeta)
                if clasificacion == 'Estudiante':
                    grado = row[3]
                    seccion = row[4]
                else:
                    grado = " "
                    seccion = " "
                return nombre, clasificacion, grado, seccion


def buscar_acceso(busqueda, conexion):
    resultados = []
    cursor = conexion.cursor()
    cursor.execute("select * from [historial de acceso] where codigo = '" + busqueda +
                   "' or fecha = '" + busqueda + "' order by fecha desc, hora desc")
    for row in cursor:
        resultados.append(list(row))
    return resultados


def buscar_foto(conexion, cedula):
    cursor = conexion.cursor()
    cursor.execute("select foto from usuarios where codigo = '" + cedula + "' ")
    for row in cursor:
        foto = row[0]
        if foto != 'None' and foto != '':
            return foto
    return "fotovacia.png"


def tabla_usuarios(conexion):
    resultados = []
    cursor = conexion.cursor()
    cursor.execute(
        "select nombre, apellido, cedula, grado, seccion, direccion, telefono, clasificacion, foto  from usuarios order by codigo ASC")
    for row in cursor:
        resultados.append(list(row))
    return resultados


def obtener_datos_usuario(conexion, codigo):
    resultados = []
    cursor = conexion.cursor()
    cursor.execute(
        "select codigo, nombre, apellido, cedula, grado, seccion, direccion, telefono, clasificacion, foto from usuarios where codigo = '" + codigo + "'")
    for row in cursor:
        resultados.append(list(row))
    return resultados


def obtener_codigos(conexion):
    resultados = []
    cursor = conexion.cursor()
    cursor.execute("select codigo from usuarios")
    for row in cursor:
        resultados.append(list(row))
    return resultados


def obtener_datos_acceso(conexion):
    resultados = []
    cursor = conexion.cursor()
    cursor.execute("select * from [historial de acceso] order by fecha desc, hora desc")
    for row in cursor:
        resultados.append(list(row))
    return resultados


def fecha_hora():
    tiempo = datetime.datetime.now()
    return tiempo.strftime("%d/%m/%Y %H:%M:%S")


def fecha():
    tiempo = datetime.date.today()
    return tiempo.strftime("%d_%m_%Y")


def establecer_carpeta(clasificacion, grado, seccion):
    if clasificacion == 'Profesor':
        carpeta = "registros\\Profesores\\"
    elif clasificacion == 'Personal':
        carpeta = "registros\\Personal\\"
    else:
        carpeta = "registros\\Estudiantes\\" + grado + "\\" + seccion + "\\"
    return carpeta


def interfaz_principal():
    sg.theme('DarkBlue13')
    menu = [["Archivo", ["&Abrir archivo...", "---", "&Salir"]],
            ["Datos", ["Visualizar Base de datos"]]]
    layout = [[sg.Menu(menu)],
              [sg.Text("Código: ", font=('lucida', 15, 'bold')), sg.Input(key="-TEXTO-", do_not_clear=False),
               sg.Button("Entrar")],
              [sg.HSeparator()],
              [sg.Image('logo.png'), sg.VSeparator(), sg.Image('fotovacia.png', key="-FOTO-")],
              [sg.HSeparator()],
              [sg.Text("", key="-NOMBRE-", font=('lucida', 15, 'bold'))],
              [sg.Text("", key="-CLASIF-", font=('lucida', 15, 'bold'))],
              [sg.Text("", key="-GRADO-", font=('lucida', 15, 'bold'))],
              [sg.Text("", key="-ESTADO-", font=('lucida', 15, 'bold'))]]
    return sg.Window("Asistencia", layout, finalize=True, resizable=True, icon='logo.ico', element_justification='center')


def actualizar_texto(cedula, ventana):
    nombre, clasificacion, grado, seccion = buscar_usuario(cedula, conexion)
    ventana["-NOMBRE-"].update(nombre)
    ventana["-CLASIF-"].update(clasificacion)
    if clasificacion == "Estudiante":
        ventana["-GRADO-"].update(grado + " grado sección: " + seccion)
        if grado == "Maternal":
            ventana["-GRADO-"].update(grado + " sección: " + seccion)
        else:
            ventana["-GRADO-"].update(grado + " grado sección: " + seccion)
    else:
        ventana["-GRADO-"].update(grado + seccion)
    if nombre != "Cédula no registrada en sistema.":
        carpeta = establecer_carpeta(clasificacion, grado, seccion)
        if llegada_salida(cedula, carpeta) % 2 != 0:
            ventana["-ESTADO-"].update("ENTRA", background_color="green")
        else:
            ventana["-ESTADO-"].update("SALE", background_color="red")
    else:
        ventana["-ESTADO-"].update("", background_color="#000000")
    foto = buscar_foto(conexion, cedula)
    if os.path.isfile(foto):
        foto = buscar_foto(conexion, cedula)
        foto = Image.open(foto)
        foto = foto.resize((400, 400), resample=Image.BICUBIC)
        foto = ImageTk.PhotoImage(foto)
        ventana["-FOTO-"].update(data=foto)
    else:
        ventana["-FOTO-"].update(foto)


def guardar_acceso(conexion, codigo, carpeta):
    cursor = conexion.cursor()
    tiempo = fecha_hora().split()
    if llegada_salida(codigo, carpeta) % 2 != 0:
        valores = [codigo, tiempo[0], tiempo[1], "ENTRADA"]
    else:
        valores = [codigo, tiempo[0], tiempo[1], "SALIDA"]
    cursor.execute("INSERT INTO [Historial de acceso] values (?, ?, ?, ?)", valores)
    conexion.commit()


def llegada_salida(cedula, carpeta):
    with open(carpeta + fecha() + ".txt", 'r') as archivo:
        datos = archivo.read()
        return datos.count(cedula)


def guardar_archivo(nombre, cedula, carpeta):
    with open(carpeta + fecha() + ".txt", 'a') as archivo:
        if llegada_salida(cedula, carpeta) % 2 != 0:
            archivo.write("SALIO " + nombre + " " + cedula + " " + fecha_hora() + "\n")
        else:
            archivo.write("ENTRO " + nombre + " " + cedula + " " + fecha_hora() + "\n")
        archivo.close()


if __name__ == '__main__':
    base = fd.askopenfilename(title="Busqueda de archivo", initialdir="os.getcwd()",
                              filetypes=(("Archivos de base de datos", ".db"),))
    conexion = sqlite3.connect(base)
    ventana1 = interfaz_principal()
    ventana1.maximize()
    ventana1['-TEXTO-'].bind("<Return>", "_Enter")
    ventana2 = None
    ventana3 = None
    codigo_usuario = None
    while True:
        try:
            ventana, event, values = sg.read_all_windows()
            if (event == sg.WIN_CLOSED or event == "Salir") and ventana == ventana1:
                break
            elif event == sg.WIN_CLOSED and ventana == ventana2:
                ventana2.close()
                ventana2 = None
            elif event == sg.WIN_CLOSED and ventana == ventana3:
                ventana3.close()
                ventana3 = None
            elif event == "Entrar" or event == "-TEXTO-" + "_Enter":
                actualizar_texto(values["-TEXTO-"], ventana)
            elif event == "Abrir archivo...":
                base_nueva = fd.askopenfilename(title="Busqueda de archivo", initialdir="os.getcwd()",
                                                filetypes=(("Archivos de base de datos", ".db"),))
                conexion = sqlite3.connect(base_nueva)
            elif event == "Visualizar Base de datos":
                ventana2 = ventana_base.creacion(tabla_usuarios(conexion), obtener_datos_acceso(conexion))
                ventana2['-BUSQUEDA-'].bind("<Return>", "_Enter")
            elif event == "Nuevo usuario":
                ventana3 = ventana_agregar.creacion()
            elif event == "Agregar usuario":
                valores = (
                    values["-CODIGO-"], values["-NOMBRE-"], values["-APELLIDO-"], values["-CEDULA-"],
                    values["-GRADO-"], values["-SECCION-"],
                    values["-DIRECCION-"], values["-TELEFONO-"], values["-CLASIFICACION-"], values["-FOTO-"])
                ventana_agregar.agregar(conexion, valores)
                ventana2["-TABLA_USUARIOS-"].update(tabla_usuarios(conexion))
                ventana2.refresh()
            elif event == "Borrar datos":
                posicion = values['-TABLA_USUARIOS-'][0]
                cursor = conexion.cursor()
                cursor.execute("delete from USUARIOS where codigo = " + str(obtener_codigos(conexion)[posicion][0]))
                conexion.commit()
                ventana2["-TABLA_USUARIOS-"].update(tabla_usuarios(conexion))
                ventana2.refresh()
                sg.popup("Borrado con éxito", title="Éxito")
            elif event == "Editar datos":
                posicion = values['-TABLA_USUARIOS-'][0]
                cursor = conexion.cursor()
                codigo_usuario = str(obtener_codigos(conexion)[posicion][0])
                ventana3 = ventana_agregar.creacion_editar(obtener_datos_usuario(conexion, codigo_usuario))
            elif event == "Editar usuario":
                valores = (
                    values["-CODIGO-"], values["-NOMBRE-"], values["-APELLIDO-"], values["-CEDULA-"],
                    values["-GRADO-"], values["-SECCION-"],
                    values["-DIRECCION-"], values["-TELEFONO-"], values["-CLASIFICACION-"], values["-FOTO-"])
                ventana_agregar.editar(conexion, valores, codigo_usuario)
                ventana2["-TABLA_USUARIOS-"].update(tabla_usuarios(conexion))
                ventana2.refresh()
            elif event == "Fecha":
                lista_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                               "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                fecha = sg.popup_get_date(locale="esp", month_names=lista_meses)
                if fecha:
                    mes, dia, año = fecha
                    ventana2['-BUSQUEDA-'].update(f"{dia:0>2d}/{mes:0>2d}/{año}")
                    resultados = buscar_acceso(f"{dia:0>2d}/{mes:0>2d}/{año}", conexion)
                    if not resultados:
                        sg.popup("No hay registros con el dato indicado.")
                    ventana2["-TABLA_ACCESO-"].update(resultados)
            elif event == "Carpeta registros":
                os.startfile("registros")
            elif event == "Buscar" or event == "-BUSQUEDA-" + "_Enter":
                if values["-BUSQUEDA-"] != "":
                    resultados = buscar_acceso(values["-BUSQUEDA-"], conexion)
                    if not resultados:
                        sg.popup("No hay registros con el dato indicado.")
                    ventana2["-TABLA_ACCESO-"].update(resultados)
                else:
                    ventana2["-TABLA_ACCESO-"].update(obtener_datos_acceso(conexion))


        except Exception as ex:
            if str(ex) == 'list index out of range':
                sg.popup("Por favor seleccione un usuario", title="Error")
            elif str(ex) == 'no such table: usuarios':
                sg.popup("No hay base de datos seleccionada", title="Error")
            print(ex)

ventana.close()
