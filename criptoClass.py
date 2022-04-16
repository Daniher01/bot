from typing import Type

from conexion import bdConnect

class criptoClass():


    def __init__(self, cripto):
        self.idcripto = ''
        self.criptoactivo = ''
        self.ath = ''
        self.bd = bdConnect()
        self.cripto = cripto

    #Getters (metodos GET)

    def get_Id(self):
        return self.idcripto

    def get_Criptoactivo(self):
        return self.criptoactivo

    def get_Ath(self):
        return self.ath

    #Setters (metodos SET)

    def set_Id(self, id):
        self.idcripto = id

    def set_Criptoactivo(self, criptoactivo):
        self.criptoactivo = criptoactivo

    def set_Ath(self, ath):
        self.ath = ath


    #metodos propios de la clase
    def buscarCripto(self):
        cur = self.bd.cursor()
        query = "SELECT * FROM cripto WHERE criptoactivo = '%s'" %self.cripto
        cur.execute(query)
        print(cur.fetchall())

        cur.close()

    def agregarCripto(self, ath):
        cur = self.bd.cursor()
        query = "INSERT INTO cripto (criptoactivo, ath) VALUES(%s, %s)"
        datos = (self.cripto, ath)
        cur.execute(query, datos)
        self.bd.commit()

c = criptoClass('BTCUSDT')
c.agregarCripto(69000)