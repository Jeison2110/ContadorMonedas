#Importaciion de bibliotecas
import cv2 as cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

#Funcion que organiza los puntos de acuerdo a la matriz de coordenadas
def ordenarpuntos(puntos):
    n_puntos=np.concatenate([puntos[0],puntos[1],puntos[2],puntos[3]]).tolist()
    y_order=sorted(n_puntos,key=lambda n_puntos:n_puntos[1])
    x1_order=y_order[:2]
    x1_order=sorted(x1_order,key=lambda x1_order:x1_order[0])
    x2_order=y_order[2:4]
    x2_order=sorted(x2_order,key=lambda x2_order:x2_order[0])
    return [x1_order[0],x1_order[1],x2_order[0],x2_order[1]]

#Funcion que alineaa la escala de pixelesen deacuerdo con el ancho y el alto
def alineamiento(imagen,ancho,alto):
    imagen_alineada=None
    grises=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    tipoumbral,umbral=cv2.threshold(grises, 150,255, cv2.THRESH_BINARY)
    cv2.imshow("CamaraMonedas", umbral)
    contorno=cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contorno=sorted(contorno,key=cv2.contourArea,reverse=True)[:1]
    for c in contorno:
        epsilon=0.01*cv2.arcLength(c, True)
        approximacion=cv2.approxPolyDP(c, epsilon, True)
        if len(approximacion)==4:
            puntos=ordenarpuntos(approximacion)
            puntos1=np.float32(puntos)
            puntos2=np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
            M = cv2.getPerspectiveTransform(puntos1, puntos2)
            imagen_alineada=cv2.warpPerspective(imagen, M, (ancho,alto))
    return imagen_alineada

# Funcion que ajusta el texto de la ventana
def AjustarTexto(event):
    # Obtener el ancho y alto actual de la ventana
    windowwidth = ventana.winfo_width()
    windowheight = ventana.winfo_height()

    # Calcular el tamaño de la fuente en función del tamaño de la ventana
    fontsize = min(windowwidth // 35, windowheight // 10)

    # Configurar la fuente del contenido_label
    labelpestaniaIni.config(font=("Times New Roman", fontsize))
    labelpestaniaHelp.config(font=("Times New Roman", fontsize))
    labelpestaniaAcer.config(font=("Times New Roman", fontsize))
    enlacedescarga.config(font=("Times New Roman", fontsize))

# Función para abrir el enlace en un navegador web
def AbrirEnlace():
    import webbrowser
    webbrowser.open("https://www.dev47apps.com/droidcam/windows/")

# Funcion de nueva bventa y logica del contador de monedas
def AbrirNuevaVentana():
    nuevaventana = tk.Toplevel(ventana) #Crea la venta
    nuevaventana.title("Contador Monedas - V 0.0.1") #Pone el titulo
    icono = tk.PhotoImage(file="Recursos\Moneda.png") #Ico para la mentana
    nuevaventana.iconphoto(False, icono) #Carga el Ico
    nuevaventana.configure(bg="aliceblue") #Color de fondo
    nuevaventana.geometry("320x180") #Tamaño de la venta
    nuevaventana.maxsize(320, 180) #Tamaño maximo ventana nueva
    nuevaventana.minsize(320, 180) #Tamaño minimo ventana nueva

    Imagen = tk.PhotoImage(file="Recursos\Monedas.png") #Carga la imagen de las monedas
    
    LabelImagen = tk.Label(nuevaventana, image=Imagen, bg="aliceblue") #Imagen monedas png
    LabelImagen.pack()

    #Texto inicial para la venta nueva
    labelText = tk.Label(nuevaventana, text="Tienes un total de \n $: 0 pesos", bg="aliceblue")   
    labelText.pack()    
    
    labelText.config(font=("Times New Roman", 16)) #Fuente y tamaño letra


    #Opcion para inicial OpenCV con la camara del celular
    capturavideo= cv2.VideoCapture(1)

    #Bucle para que la camara permanesca encendida
    while True:
        tipocamara,camara=capturavideo.read()
        
        #validacion para verficar que si se tenga una camara como dispositivo
        if tipocamara==False:
            break

        #Variable con las medidas de la cartulina negra pasadas a la funcion alineamiento
        imagen_A6=alineamiento(camara,ancho=480,alto=640)


        #Condicional donde se valida y se llama a las funciones para contar las monedas 
        if imagen_A6 is not None:
            puntos=[]
            imagen_gris=cv2.cvtColor(imagen_A6,cv2.COLOR_BGR2GRAY)
            blur=cv2.GaussianBlur(imagen_gris,(5,5),1)
            _,umbral2=cv2.threshold(blur,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
            cv2.imshow("CamaraMonedas",umbral2)
            contorno2=cv2.findContours(umbral2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            cv2.drawContours(imagen_A6, contorno2, -1, (255,0,0),2)

            #Creacion de variables
            suma1, suma2, suma3, suma4, suma5 = 0, 0, 0, 0, 0
            suma6, suma7, suma8, suma9 = 0, 0, 0, 0
            
            #Bucle para setear el contorno de las monedas
            for c_2 in contorno2:
                area=cv2.contourArea(c_2)
                Momentos = cv2.moments(c_2)
                if(Momentos["m00"]==0):
                    Momentos["m00"]=1.0
                x=int(Momentos["m10"]/Momentos["m00"])
                y=int(Momentos["m01"]/Momentos["m00"])

                #Condicionales para cada una de las medidas de las monedas

                #Condicional para la moneda de 50 Nueva
                if area < 4765:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$50",(x,y) , font, 0.75, (0,255,0),2)
                    suma1=suma1+50
                
                #Condicional para la moneda de 100 Nueva
                elif area < 6880:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$100",(x,y) , font, 0.75, (0,255,0),2)
                    suma2=suma2+100
                
                #Condicional para la moneda de 50 Vieja
                elif area < 7377:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$50",(x,y) , font, 0.75, (0,255,0),2)
                    suma3=suma3+50
                
                #Condicional para la moneda de 200 Nueva
                elif area < 8421:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$200",(x,y) , font, 0.75, (0,255,0),2)
                    suma4=suma4+200
                
                #Condicional para la moneda de 100 Vieja
                elif area < 8889:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$100",(x,y) , font, 0.75, (0,255,0),2)
                    suma5=suma5+100
                
                #Condicional para la moneda de 500 Vieja
                elif area < 9288:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$500",(x,y) , font, 0.75, (0,255,0),2)
                    suma6=suma6+500
                
                #Condicional para la moneda de 500 Nueva
                elif area < 9450:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$500",(x,y) , font, 0.75, (0,255,0),2)
                    suma7=suma7+500
                
                #Condicional para la moneda de 200 Vieja
                elif area < 10029:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$200",(x,y) , font, 0.75, (0,255,0),2)
                    suma8=suma8+200
                
                #Condicional para la moneda de 1000 Nueva
                else:
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_A6, "$1000",(x,y) , font, 0.75, (0,255,0),2)
                    suma9=suma9+1000

            #suma el total de las monedas
            total=suma1+suma2+suma3+suma4+suma5+suma6+suma7+suma8+suma9
            TotalFinal =  round(total,0)
            

            cv2.imshow("Imagen A6", imagen_A6)# Muestra el area de trabajo
            cv2.imshow("camara", camara)#Muestra la camara completa

            #Muentra el todas del valor actualizando la venta
            labelText.config(text = f"Tienes un total de \n $: {TotalFinal} pesos")
            nuevaventana.update()

            
        #Condicional para cerrar el programa con oprimmir la tecla q
        if cv2.waitKey(1) == ord('q'):
            nuevaventana.destroy()
            break  


    #Opciones para que cuando termine el progama de cierre la camara    
    capturavideo.release()
    cv2.destroyAllWindows() 


#INICIO=====================Seteo Configuracio Venta===========================
ventana = tk.Tk() #Crea la ventana
ventana.title("Contador Monedas - V 0.0.1") #Pone el titulo
icono = tk.PhotoImage(file="Recursos\Moneda.png") #Ico para la mentana
ventana.iconphoto(False, icono) #Carga el Ico
ventana.configure(bg="aliceblue")
#FIN=====================Seteo Configuracio Venta===========================


#INICIO=====================Configuracion Venta Tamaño===========================
# Obtener las dimensiones de la pantalla
screenwidth = ventana.winfo_screenwidth()
screenheight = ventana.winfo_screenheight()


# Condicional para validar que la venta no sea muy grande
if screenwidth >= 800 and screenheight >= 660:
    screenwidth = 600
    screenheight = 660

# Establecer el tamaño de la ventana
ventana.geometry(f"{screenwidth}x{screenheight}")

# Establecer el tamaño máximo de la ventana (800x600 en este ejemplo)
ventana.maxsize(screenwidth, screenheight)
#FIN=====================Configuracion Venta Tamaño===========================


#INICIO=====================Creacion de ventas como pestañas===========================
# Crear el widget Notebook
pestanias = ttk.Notebook(ventana)

# Crear pestañas
pestaniaIni = ttk.Frame(pestanias)
pestaniaHelp = ttk.Frame(pestanias)
pestaniaAcer = ttk.Frame(pestanias)

# Agregar pestañas al Notebook
pestanias.add(pestaniaIni, text="INICIO")
pestanias.add(pestaniaHelp, text="HELP")
pestanias.add(pestaniaAcer, text="ACERCA DE")


# Agregar contenido a las pestañas
labelpestaniaIni = tk.Label(pestaniaIni, text="""
Bienvenido al contador de monedas
una App que te ayudara a identificar 
por medio de AI y la camara de tu
celular la cantidad de monedas y 
el valor que tengas visible a la 
camara

Si quieres saber mas de como
utilizar esta herramienta
dirigete a la opcion de HELP
""")

labelpestaniaHelp = tk.Label(pestaniaHelp, text="""
Para ejecutar correctamente esta app
es muy importante que sigas los 
pasos acontinucación:
                             
1-Tener en tu computador instalado 
DroidCam Cliente, si no lo tienes dar
clien en desacrgar DroidCamClient 
2-Instalar la app de DroidCam en tu celular
desde la APPStore o Apple
3-Tener una hoja de cartulina en fondo negro
4-Tener una cartulina blanca, recortada en un
rectangulo con medidas A6(10,5cm x 14,8cm)
5-Iniciar primero la conexion con DroidCam
6-Una vez conectado el DroidCam, proceder a
dar click en el boton INICIAR CONTADOR
7-Para finalizar la conexion con la camara
seleccionar la ventana y precionar la tecla "q"
""")

labelpestaniaAcer = tk.Label(pestaniaAcer, text="""
App creada por:
Jeison Valencia
Esperanza Castro

©/Derechos reservados

Corporación Iberoamericana

02 de Septiembre del 2023
V 0.0.1

Soporte a:
ecastrol@ibero.edu.co
jvalen28@ibero.edu.co
""")

# Mostrar las pestañas
labelpestaniaIni.pack(padx=10, pady=10)
labelpestaniaHelp.pack(padx=10, pady=10)
labelpestaniaAcer.pack(padx=10, pady=10)
pestanias.pack(padx=10, pady=10, fill="both", expand=True)
#FIN=====================Creacion de ventas como pestañas===========================


#INICIO=====================Creacion enlace de la descarga===========================
# Crear un enlace para la descarga
enlacedescarga = ttk.Label(pestaniaHelp, text="Descargar DroidCamClient", cursor="hand2", foreground="blue")
enlacedescarga.bind("<Button-1>", lambda e: AbrirEnlace())
enlacedescarga.pack()
#FIN=====================Creacion enlace de la descarga===========================


#INICIO=====================Creacion del boton===========================
#Boton para iniciar la app
BotonIni = tk.Button(ventana, text="INICIAR CONTADOR", command=AbrirNuevaVentana, bg="darkgray")

BotonIni.pack(pady=5)
#GIN=====================Creacion del boton===========================


# Ajusta el tamaño de la letra de las ventanas
ventana.bind("<Configure>", AjustarTexto)


if __name__ == "__main__":
    ventana.mainloop() #Inicializa el proyecto