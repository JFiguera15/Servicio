import FreeSimpleGUI as sg


def creacion(datos, acceso):
    col1 = [[sg.Button("Nuevo usuario", size=(10, 1))],
            [sg.Button("Borrar datos", size=(10, 1))],
            [sg.Button("Editar datos", size=(10, 1))]
            ]
    pestaña1 = [[sg.Table(values=datos,
                          headings=["Nombre", "Apellido", "Cédula", "Grado", "Sección", "Dirección",
                                    "Teléfono", "Clasificación", "Foto"], key="-TABLA_USUARIOS-", size=(1, 14)
                          , auto_size_columns=False),
                 sg.VSeparator(), sg.Column(col1)]]

    pestaña2 = [[sg.Push(), sg.Text("Búsqueda:", font=('lucida', 12, 'bold')), sg.InputText(key="-BUSQUEDA-"),
                 sg.Button("Buscar"), sg.Button("Fecha", target="-BUSQUEDA-"), sg.Button("Carpeta registros"),
                 sg.Push()],
                [sg.Push(), sg.Table(values=acceso,
                                     headings=["Codigo", "Fecha", "Hora", "Estado"], key="-TABLA_ACCESO-", size=(1, 12))
                    , sg.Push()]]

    layout = [[sg.TabGroup([[sg.Tab("Usuarios", pestaña1), sg.Tab("Historial de acceso", pestaña2)]])]]
    return sg.Window("Base de datos", layout, finalize=True, icon='logo.ico')
