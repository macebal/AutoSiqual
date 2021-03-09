import pyautogui, time, logging, PIL, datetime, pyperclip
from datetime import timedelta

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S", format='%(asctime)s [%(levelname)s] %(message)s')

demoraEntreComandos = 0.5  # la demora en segundos que espera entre cada comando del teclado o mouse
demoraEnAbrirPantallas = 1.5  # la demora en segundos que espera que abran las ventanas, depende de la conexion

def clickear_imagen(nombre_imagen, indice = 0, confianza = 1):
    ruta = 'img\\' + nombre_imagen

    if confianza < 1:
        ubicacion = list(pyautogui.locateAllOnScreen(ruta, confidence=confianza))  # busca todos las imagenes, el argumento confidence es por si varian algunos pixeles no encuentra algunas imagenes, default = 1 sino para un match exacto
    else:
        ubicacion = list(pyautogui.locateAllOnScreen(ruta))
        
    if len(ubicacion) == 0:
        logging.critical('No se encuentra el boton ' + nombre_imagen + '. ¿La ventana está cerrada?')
        logging.critical('El programa terminó abruptamente.')
        exit(1)

    coordenadas = pyautogui.center(ubicacion[indice])  # busca las coordenadas
    pyautogui.click(coordenadas[0], coordenadas[1]) # clickea la imagen

def pegar_datos(listaDatos):
    for dictHora in listaDatos:
        
        # clickea en el boton de copiar RIC
        clickear_imagen('copiarRIC.png')

        #Presiono TAB 5 veces para posicionarme sobre la fecha
        pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab'], interval=demoraEntreComandos)

        #selecciono y copio la fecha
        pyautogui.hotkey('shiftleft','end')
        pyautogui.typewrite(['del'])

        pyautogui.typewrite(datetime.datetime.strftime(dictHora['Fecha'], '%Y-%m-%d'))
        pyautogui.typewrite(['tab'])

        # clickea en el boton de grabar
        clickear_imagen(nombre_imagen = 'grabar.png', confianza = 0.9)
        time.sleep(demoraEnAbrirPantallas)

        #cierro el cartel de grabado con exito
        pyautogui.typewrite(['enter'])
        time.sleep(demoraEnAbrirPantallas)

        # clickea en el boton de ver RIE
        clickear_imagen(nombre_imagen = 'RIE.png', confianza = 0.9)
        time.sleep(demoraEnAbrirPantallas)

        # clickea en el boton de ver Ensayos/Resultados
        clickear_imagen('ensayosResultados.png')
        time.sleep(demoraEnAbrirPantallas)

        pyautogui.hotkey('alt', 'down')

        time.sleep(demoraEnAbrirPantallas)
        
        for i in range(7):
            pyautogui.typewrite(['down'])

        time.sleep(demoraEnAbrirPantallas)

        pyautogui.typewrite(['enter'])

        time.sleep(demoraEnAbrirPantallas)

        pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'tab', 'tab'], interval=demoraEntreComandos)

        pyautogui.typewrite(['pageup', 'pageup', 'pageup', 'pageup', 'pageup'], interval=demoraEntreComandos)

        pyautogui.typewrite(str(dictHora['CAOT']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['SIO2']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['AL2O3']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['FE2O3']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['MGO']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['SO3']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['K2O']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['NA2O']).replace('.',','))

        for i in range(5):
            pyautogui.typewrite(['down'])
            
        pyautogui.typewrite(str(dictHora['CAOL']).replace('.',',')) if dictHora['CAOL'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['CO2']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['PF']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['RICARB']).replace('.',',')) if dictHora['RICARB'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['G45U']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['G75U']).replace('.',','))
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(round(dictHora['SBA']))) if dictHora['SBA'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['MVOL']).replace('.',',')) if dictHora['MVOL'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['AGP']).replace('.',',')) if dictHora['AGP'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['IP'].hour * 60 + dictHora['IP'].minute)) if dictHora['IP'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['FP'].hour * 60 + dictHora['FP'].minute)) if dictHora['FP'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['EXAU']).replace('.',',')) if dictHora['EXAU'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['BARI'] / 1000).replace('.',',')) if dictHora['BARI'] != None else None

        for i in range(14):
            pyautogui.typewrite(['down'])

        pyautogui.typewrite(str(dictHora['R2']).replace('.',',')) if dictHora['R2'] != None else None
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(['down'])
        pyautogui.typewrite(str(dictHora['R7']).replace('.',',')) if dictHora['R7'] != None else None
        pyautogui.typewrite(['down'])

        time.sleep(demoraEnAbrirPantallas)
        
        # clickea en el boton de Grabar Datos
        clickear_imagen(nombre_imagen = 'grabarDatos.png', confianza = 0.9)
        time.sleep(demoraEnAbrirPantallas)
        
        pyautogui.typewrite(['enter'])
        time.sleep(demoraEnAbrirPantallas)
        pyautogui.typewrite(['enter'])

        # clickea en el boton de Cerrar
        clickear_imagen(nombre_imagen = 'cerrar1.png', confianza = 0.8)
        time.sleep(demoraEnAbrirPantallas)
       
        # clickea en el boton de Cerrar
        clickear_imagen(nombre_imagen = 'cerrar2.png', confianza = 0.9)
