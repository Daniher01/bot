from conexion import bdConnect

class ordenClass():

    def __init__(self, simbolo):
        self.bd = bdConnect()
        self.idOrden = ''
        self.monto = ''
        self.precio = ''
        self.tipo_orden = ''
        self.fecha = ''
        self.status = ''
        self.simbolo = simbolo

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

    def get_simbolo(self):
        return self.simbolo


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

    def set_simbolo(self,simbolo):
        self.simbolo = simbolo



    """
    metodos propios de la clase
    """

    def buscarOrdenes_cripto_status(self, status):
        try:
            cur = self.bd.cursor()
            query = "SELECT * FROM orden " \
                    "WHERE status = '%s'" % (status)
            cur.execute(query)
            data = cur.fetchall()
            return data
            cur.close()
        except Exception as e:
            error('function::buscarOrdenes_cripto_status',e)

    def insertarOrden(self, idorden, monto, precio, tipo_orden, fecha, status):
        try:
            cur = self.bd.cursor()
            query = "INSERT INTO orden (idorden, monto, precio_compra, tipo_orden, fecha, status, simbolo) " \
                    "VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
                    idorden, monto, precio, tipo_orden, fecha, status, self.simbolo)
            cur.execute(query)
            self.bd.commit()
        except Exception as e:
            print('function::insertarOrden', e)


    def updateOrden(self, idorden, status):
        try:
            cur = self.bd.cursor()
            query = "UPDATE orden SET status='%s' WHERE idorden='%s'" % (status, idorden)
            cur.execute(query)
            self.bd.commit()
        except Exception as e:
            print('function::updateOrden', e)









