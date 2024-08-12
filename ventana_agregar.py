import FreeSimpleGUI as sg


def creacion():
    layout = [[sg.Text("Agregar nuevo usuario a la base de datos:", font=('lucida', 12, 'bold'))],
              [sg.HSeparator()],
              [sg.Text("Identificador:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-CODIGO-")],
              [sg.Text("Nombre:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-NOMBRE-")],
              [sg.Text("Apellido:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-APELLIDO-")],
              [sg.Text("Cédula:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-CEDULA-")],
              [sg.Text("Grado:", size=(10, 1), font=('lucida', 12, 'bold')), sg.Combo(['Maternal', '1er', '2do', '3er',
                                                          '4to', '5to', '6to', 'Profesor', 'Personal'],
                                                         readonly=True, default_value='Profesor', key="-GRADO-")],
              [sg.Text("Sección:", size=(10, 1), font=('lucida', 12, 'bold')),
               sg.Combo(['1', '2', '3', 'A', 'B', 'C', 'U'], default_value='U', readonly=True, key="-SECCION-")],
              [sg.Text("Dirección:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-DIRECCION-")],
              [sg.Text("Teléfono:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-TELEFONO-")],
              [sg.Text("Clasificación:", size=(10, 1), font=('lucida', 12, 'bold')),
               sg.Combo(['Estudiante', 'Profesor', 'Personal'],
                                                                 default_value='Profesor', readonly=True,
                                                                 key="-CLASIFICACION-")],
              [sg.Text("Foto:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(key="-FOTO-"),
               sg.FileBrowse(button_text="Buscar", file_types=(("Archivos de imagen", ".png .jpg"),))],
              [sg.HSeparator()],
              [sg.Button("Agregar usuario")]
              ]
    return sg.Window("Agregar usuario", layout, element_justification='left', finalize=True, icon='logo.ico')


def creacion_editar(datos):
    layout = [[sg.Text("Editar datos:", font=('lucida', 12, 'bold'))],
              [sg.HSeparator()],
              [sg.Text("Identificador:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][0]), key="-CODIGO-")],
              [sg.Text("Nombre:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][1]), key="-NOMBRE-")],
              [sg.Text("Apellido:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][2]), key="-APELLIDO-")],
              [sg.Text("Cédula:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][3]), key="-CEDULA-")],
              [sg.Text("Grado:", size=(10, 1), font=('lucida', 12, 'bold')), sg.Combo(['Maternal', '1er', '2do', '3er',
                                                          '4to', '5to', '6to', 'Profesor', 'Personal'],
                                                         readonly=True, default_value='Profesor', key="-GRADO-")],
              [sg.Text("Sección:", size=(10, 1), font=('lucida', 12, 'bold')),
               sg.Combo(['1', '2', '3', 'A', 'B', 'C', 'U'], default_value='U', readonly=True, key="-SECCION-")],
              [sg.Text("Dirección:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][6]), key="-DIRECCION-")],
              [sg.Text("Teléfono:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][7]), key="-TELEFONO-")],
              [sg.Text("Clasificación:", size=(10, 1), font=('lucida', 12, 'bold')), sg.Combo(['Estudiante', 'Profesor', 'Personal'],
                                                                 default_value='Profesor', readonly=True,
                                                                 key="-CLASIFICACION-")],
              [sg.Text("Foto:", size=(10, 1), font=('lucida', 12, 'bold')), sg.InputText(str(datos[0][9]), key="-FOTO-"),
               sg.FileBrowse(file_types=(("Archivos de imagen", ".png .jpg"),))],
              [sg.HSeparator()],
              [sg.Button("Editar usuario")]
              ]
    return sg.Window("Editar usuario", layout, element_justification='left', icon='logo.ico', finalize=True)


def agregar(conexion, valores):
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO USUARIOS (CODIGO, NOMBRE, APELLIDO, CEDULA, GRADO, SECCION, DIRECCION, TELEFONO, CLASIFICACION, FOTO) values (?,?,?,?,?,?,?,?,?,?)",
        valores)
    conexion.commit()
    sg.popup("Agregado con éxito", title="Éxito")


def editar(conexion, valores, codigo_original):
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE usuarios set CODIGO = ?, nombre = ?, apellido = ?, cedula = ?, grado = ?, seccion = ?, direccion = ?, telefono = ?, "
        "clasificacion = ?, foto = ? where codigo = '" + str(
            codigo_original) + "'", valores)
    conexion.commit()
    sg.popup("Editado con éxito", title="Éxito")
