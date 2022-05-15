from conexion import bdConnect

class ordenClass():

    def __init__(self, idcripto):
        self.bd = bdConnect()
        self.idOrden = ''
        self.monto = ''
        self.precio = ''
        self.tipo_orden = ''
        self.fecha = ''
        self.status = ''
        self.idcripto = idcripto

    # Getters (metodos GET)

    def get_id(self):
        return self.idOrden

    def get_monto(self):
        return self.monto

    def get_precio(self):
        return self.precio

    def get_tipo_orden(self):
        return self.tipo_orden

    def get_fecha(self):
        return self.fecha

    def get_status(self):
        return self.status

    def get_idCripto(self):
        return self.idcripto


    # Setters (metodos SET)

    def set_id(self, id):
        self.idOrden = id

    def set_monto(self, monto):
        self.monto = monto

    def set_precio(self, precio):
        self.precio = precio

    def set_tipo_orden(self, tipo_orden):
        self.tipo_orden = tipo_orden

    def set_fecha(self, fecha):
        self.fecha = fecha

    def set_status(self, status):
        self.status = status

    def set_idCripto(self,idCripto):
        self.idcripto = idCripto



    """
    metodos propios de la clase
    """

    def buscarOrdenes_cripto_fecha(self, fecha):
        cur = self.bd.cursor()
        query = "SELECT * FROM orden " \
                "INNER JOIN cripto on cripto.idcripto = orden.cripto_idcripto" \
                "WHERE cripto_idcripto = '%s' AND fecha = '%s'" %self.idcripto %fecha
        cur.execute(query)
        data = cur.fetchall()
        cur.close()

    def insertarOrden(self, monto, precio, tipo_orden, fecha, status):
        cur = self.bd.cursor()
        query = "INSERT INTO orden (monto, precio, tipo_orden, fecha, status) " \
                "VALUES('%s','%s','%s','%s','%s')"
        datos = (monto, precio, tipo_orden, fecha, status)
        cur.execute(query)
        self.bd.commit()

    def updateOrden(self, status, id):
        cur = self.bd.cursor()
        query = "UPDATE orden SET status = %s WHERE idorden=%s"
        datos = (status, id)
        cur.execute(query, datos)
        self.bd.commit()





