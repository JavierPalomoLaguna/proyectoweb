class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        if "carro" not in self.session:
            self.session["carro"] = {}
        self.carro = self.session["carro"]


    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carro:
            self.carro[producto_id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": 1,
                "imagen": producto.foto_principal.url if producto.foto_principal else "",
        }
        else:
            self.carro[producto_id]["cantidad"] += 1
        self.guardar_carro()


    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
            
    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()
    

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            self.carro[producto_id]["cantidad"] -= 1
            if self.carro[producto_id]["cantidad"] < 1:
                self.eliminar(producto)
            else:
                self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified = True
    
    #mostrar el total en la vista:
    def total_precio(self):
        return sum(item["precio"] * item["cantidad"] for item in self.carro.values())
    
    # mostrar el número total de productos en el carrito (no el total en euros)
    def total_items(self):
        return sum(item["cantidad"] for item in self.carro.values())
    
    def total_importe(self):
        total = 0
        for key, value in self.carro.items():
            total += float(value["precio"]) * int(value["cantidad"])
        return total

    def total_carro(self):
        total = 0
        for key, value in self.carro.items():
            total += int(value["cantidad"])
        return total
        
 

