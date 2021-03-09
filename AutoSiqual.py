# AutoSiqual - Ingresa datos automaticamente en Siqual ;)

import pyautogui, time, logging, PIL, datetime, pyperclip, ctypes
from datetime import timedelta
from ImportarDatos import importar_datos
from PegarDatos import pegar_datos

def numblock_activado():
    #devuelve True si la tecla esta activada y False si no lo está
    dll = ctypes.WinDLL ("User32.dll")
    VK_NUMLOCK = 0x90
    return bool(dll.GetKeyState(VK_NUMLOCK))

def clickear_imagen(nombre_imagen, indice = 0):
    ruta = 'img\\' + nombre_imagen
    ubicacion = list(pyautogui.locateAllOnScreen(ruta))  # busca todos las imagenes, el argumento confidence es por si varian algunos pixeles no encuentra algunas imagenes, default = 1 sino para un match exacto

    if len(ubicacion) == 0:
        logging.critical('No se encuentra el boton ' + nombre_imagen + '. ¿La ventana está cerrada?')
        logging.critical('El programa terminó abruptamente.')
        exit(1)

    coordenadas = pyautogui.center(ubicacion[indice])  # busca las coordenadas
    pyautogui.click(coordenadas[0], coordenadas[1]) # clickea la imagen


logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S", format='%(asctime)s [%(levelname)s] %(message)s')

demoraEntreComandos = 0.5  # la demora en segundos que espera entre cada comando del teclado o mouse
demoraEnAbrirPantallas = 1.5  # la demora en segundos que espera que abran las ventanas, depende de la conexion

cementos = ['CPC40', 'CPC30', 'CPN40', 'Plasticor']

logging.info('Programa Iniciado - Tiene 5 segundos para hacer foco (maximizar la pantalla de SIQUAL)')
time.sleep(5)

pyautogui.click  # para asegurar el foco

#Si estaba activado la tecla Bloq Num la desactivo porque sino no deja copiar la fecha
if (numblock_activado() == True):
    logging.info('Tecla Bloq Num desactivada.')
    pyautogui.press('numlock')

logging.info('Abriendo pantalla de Creación/Modificación de RIC')
pyautogui.hotkey('alt', 'e')  # Abre el menú de Gestión de Ensayos

time.sleep(demoraEntreComandos)
pyautogui.typewrite(['c', 'c', 'm'], interval=demoraEntreComandos)  # Abre la pantalla de creación de nuevo RIC

logging.info('Abriendo ventana de selección de RIC')
time.sleep(demoraEnAbrirPantallas)

for cemento in cementos:

    # clickea en el 2do boton de puntos suspensivos
    clickear_imagen(nombre_imagen = 'puntosSuspensivos.png', indice = 1)

    logging.info('Buscando ultimo RIC de %s', cemento)
    time.sleep(demoraEnAbrirPantallas)

    pyautogui.typewrite(['tab', 'tab'], interval=demoraEntreComandos)  # Me posiciono en el campo de fecha de inicio
    pyautogui.hotkey('shiftleft','end') #la selecciono
    pyautogui.press('del') # la borro
    time.sleep(demoraEntreComandos)

    fechaInicio = datetime.datetime.now() - timedelta(days=45)  # defino la fecha de inicio como 45 días antes de la fecha actual

    pyautogui.typewrite(fechaInicio.strftime('%Y-%m-%d'))  # Tipeo la fecha, con formato yyyy-mm-dd
    time.sleep(demoraEntreComandos)

    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=demoraEntreComandos)  # Apreto el boton buscar
    time.sleep(demoraEnAbrirPantallas)

    # busco el boton con la flecha apuntando hacia abajo de 'cod. producto' y lo clickeo
    clickear_imagen(nombre_imagen = 'flecha.png', indice = 2)
    time.sleep(demoraEnAbrirPantallas)

    # busco el item con el nombre del cemento que me interesa (la imagen se llama asi tambien) y lo clickeo
    clickear_imagen(cemento + '.png')
    time.sleep(demoraEnAbrirPantallas)

    # Presiono 5 veces la tecla av pag para ir al final de la tabla (ultima fecha) y presiono enter
    pyautogui.typewrite(['pagedown', 'pagedown', 'pagedown', 'pagedown', 'pagedown'], interval=demoraEntreComandos)

    # Clickeo en el cuadrado amarillo para seleccionar el ultimo RIC
    clickear_imagen('casilleroSeleccionado.png')
    time.sleep(demoraEntreComandos)

    pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'enter'], interval=demoraEntreComandos)  # Apreto el boton ok
    logging.info('Cargado el RIC de la fecha ')

    # Clickeo el botón 'Cargar Datos'
    clickear_imagen('cargarDatos.png')
    time.sleep(demoraEntreComandos)

    #Presiono TAB 5 veces para posicionarme sobre la fecha
    pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab'], interval=demoraEntreComandos)

    #selecciono y copio la fecha
    pyautogui.hotkey('shiftleft','end')
    time.sleep(demoraEntreComandos)

    pyautogui.hotkey('ctrl','c')
    time.sleep(demoraEntreComandos)
    
    fecha = pyperclip.paste()
    try:
        fechaInicio = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        logging.info('Fecha encontrada y copiada.')
        
        logging.info('Cargando datos de Base de Datos Productos.xlsx')
        listaDatos = importar_datos(fechaInicio, cemento)

        try:
            pegar_datos(listaDatos)
            
        except:
            logging.warning('No hay datos para cargar de ' + cemento)
    except:
        logging.warning('La fecha no se copió correctamente. ¿La tecla Bloq Num está activada?')
        break
logging.info('Finalizado')

