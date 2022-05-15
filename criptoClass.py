from typing import Type

from conexion import bdConnect

class criptoClass():


    def __init__(self, idcripto):
        self.idcripto = ''
        self.criptoactivo = ''
        self.ath = ''
        self.bd = bdConnect()
        self.cripto = idcripto

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


    """
    metodos propios de la clase
    """

    #trae todos los datos de esa cripto
    def buscarCripto(self):
        cur = self.bd.cursor()
        query = "SELECT * FROM cripto WHERE criptoactivo = '%s'" %self.cripto
        cur.execute(query)
        data = cur.fetchall()
        for d in data:
            self.set_Id(d[0])
            self.set_Criptoactivo(d[1])
            self.set_Ath(d[2])
        cur.close()

    #permite agregar una cripto
    def agregarCripto(self):
        cur = self.bd.cursor()
        query = "INSERT INTO cripto (criptoactivo) VALUES('%s')" %self.cripto
        datos = (self.cripto)
        cur.execute(query)
        self.bd.commit()

    #actualiza el ath de la cripto
    def actualizarCripto(self, ath):
        cur = self.bd.cursor()
        query = "UPDATE cripto SET ath = %s WHERE criptoactivo=%s"
        datos = (ath, self.cripto)
        cur.execute(query, datos)
        self.bd.commit()


#c = criptoClass('BTCUSDT')
#c.buscarCripto()
