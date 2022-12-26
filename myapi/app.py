from typing import Optional
from sqlmodel import Session, SQLModel, select, col
from myapi.db import create_db_and_tables ,engine


#IMPORTO LOS MODELOS
from myapi.models import (
    Usuario,
    UsuarioCreate,
    Rifas,
)



#PARA LA CREACION DE UN NUEVO USUARIO
def create_usuario(usu: UsuarioCreate):
    usu_1 = Usuario(nombre=usu.c_nombre, clave=usu.c_clave, saldo=10000)

    with Session(engine) as session:
        session.add(usu_1)  #guarda el registro en la "session"
        session.commit()    #guarda los datos en la database
        session.refresh(usu_1)
        return usu_1




#PARA LA CREACCION DE UNA NUEVA RIFA
def create_rifa(usu_id: int, rif_cantidad: int, rif_precio: int, rif_premios: list):

    with Session(engine) as session:
        rifa = Rifas(id_usuario=usu_id, estado="Abierta", cantidad=rif_cantidad, precio=rif_precio)

        for i in range(rif_cantidad):
            rifa.numero += str(i)
            rifa.estado_numero += "Comprar"

            if i != (rif_cantidad-1):
                rifa.numero += " "
                rifa.estado_numero += " "

        for i in rif_premios:
            rifa.premios += i
            if i != rif_premios[-1]:
                rifa.premios += " "

        session.add(rifa)  #guarda el registro en la "session"
        session.commit()    #guarda los datos en la database




#PARA CUANDO SE DESEA ENTRAR CON LA CUENTA DE UN USUARIO
def ingresar_usuario(usu_nombre: str, usu_clave: str):

    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.nombre == usu_nombre, Usuario.clave == usu_clave)         #Eso le dice que queremos seleccionar todas las columnas necesarias de la tabla USUARIO donde el ID sea 0.
        resultado = session.exec(seleccion)     #Esto le indicará a la "sesión"que debe ejecutar ese SELECT en la base de datos y recuperar los resultados.

        usuario = resultado.first()       #con esto se guarda, en "usuario", el primer registro encontrado
    
    if usuario==None:
        return False
    else:
        return usuario




#PARA MOSTRAR TODAS LAS RIFAS EXISTENTES
def mostrar_rifas():
    lista_rifas = []
    with Session(engine) as session:
        seleccion = select(Rifas)
        resultado = session.exec(seleccion)

        for rifa in resultado:
            lista_rifas.append(rifa.id)
            lista_rifas.append(rifa.estado)
            lista_rifas.append(rifa.cantidad)
            lista_rifas.append(rifa.precio)

    return lista_rifas




#PARA MOSTRAR LOS NUMEROS DE UNA RIFA SELECCIONADA
def mostrar_numeros(rif_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        lista_numeros = rifa.numero.split(" ")
        
    return lista_numeros




#PARA MOSTRAR LOS RSTADOS DE CADA NUMERO DE UNA RIFA SELECCIONADA
def mostrar_estados(rif_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        lista_estados = rifa.estado_numero.split(" ")
    
    return lista_estados




#PARA MOSTRAR LOS PREMIOS DE UNA RIFA SELECCIONADA
def mostrar_premios(rif_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        lista_premios = rifa.premios.split(" ")

    return lista_premios




#PARA CUANDO EL USUARIO DESEE DESHABILITAR SU CUENTA
def eliminar_usuario(usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        session.delete(usuario)         #se elimina el usuario
        session.commit()                #se modifica la database

        #el objeto "usuario" aun se puede usar para su retorno




#PARA CUENDO SE HAYAN COMPRADO TODOS LOS NUMEROS DE UNA RIFA
def cerrar_rifa(rifa_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rifa_id)
        resultado = session.exec(seleccion)

        rifa = resultado.first()
        rifa.estado = "Cerrada"
        session.add(rifa)
        session.commit()




#PARA CUANDO EL USUARIO DECIDA CAMBIAR SU NOMBRE
def modificar_nombre_usuario(new_nombre: str, usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.nombre = new_nombre
        session.add(usuario)
        session.commit()




#PARA CUANDO EL USUARIO DECIDA CAMBIAR SU CLAVE
def modificar_clave_usuario(new_clave: str, usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.clave = new_clave
        session.add(usuario)
        session.commit()




#PARA RECARGAR EL SALDO DEL USUARIO
def agregar_saldo_usuario(usu_id: int, re_saldo: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.saldo += re_saldo      #se modifica el saldo
        usuario.recargas += (" " + str(re_saldo))   #el saldo recargado se agrega al historial del usuario
        session.add(usuario)            #se modifica la sesion
        session.commit()                #se modifica la database
        session.refresh(usuario)        #se actualiza el objeto

    return usuario.saldo




def comprar_numeros(rif_id: int, usu_nombre: str, numeros: list):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        lista_estados = rifa.estado_numero.split(" ")

        for i in numeros:
            lista_estados[i] = usu_nombre

        rifa.estado_numero = " "
        rifa.estado_numero = rifa.estado_numero.join(lista_estados)
        
        session.add(rifa)
        session.commit()




#PARA CUANDO EL PROPIETARIO DECIDA SORTEAR LA RIFA
def sortear_rifa(rif_id: int, ganadores: list):
    with Session(engine) as session:

        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()
        lista_premios = rifa.premios.split(" ")


        x=0
        for i in ganadores:
            seleccion = select(Usuario).where(Usuario.nombre == i)
            resultado = session.exec(seleccion)
            usuario = resultado.first()
            usuario.mis_premios += str(lista_premios[x])
            if lista_premios[x] != lista_premios[-1]:
                usuario.mis_premios += " "
            x += 1

            session.add(usuario)
            session.commit()


        x=0
        for i in ganadores:
            lista_premios[x] += ("-->" + i)
            x += 1

        rifa.premios = " "
        rifa.premios = rifa.premios.join(lista_premios)
        rifa.estado = "Sorteada"
        session.add(rifa)
        session.commit()
