class Graph:
    
    def __init__(self, es_dirigido, es_pesado, vertices_iniciales = None):

        self.dirigido = es_dirigido
        self.pesado = es_pesado
        self.adyacencias = {}

        if vertices_iniciales:
            for vertice in vertices_iniciales:
                self.adyacencias[vertice] = {}

    def agregar_vertice(self, vertice):
        if not vertice in self.adyacencias:
            self.adyacencias[vertice] = {}

    def borrar_vertice(self, vertice):
        if not vertice in self.adyacencias: return
        
        self.adyacencias.pop(vertice, None)
        for v in self.adyacencias:
            if vertice in self.adyacencias[v]:
                self.adyacencias[v].pop(vertice, None)

    def agregar_arista(self, v1, v2, peso = 0):
        if not v1 in self.adyacencias or not v2 in self.adyacencias: return
        
        self.adyacencias[v1][v2] = peso
        if not self.dirigido:
            self.adyacencias[v2][v1] = peso

    def borrar_arista(self, v1, v2):
        if not v1 in self.adyacencias or not v2 in self.adyacencias: return
        
        self.adyacencias[v1].pop(v2, None)
        if not self.dirigido:
            self.adyacencias[v2].pop(v1, None)
    
    def existe_arista(self, v1, v2):
        if v2 in self.adyacencias[v1]:
            return True
        return False
    
    def peso_arista(self, v1, v2):
        if self.existe_arista(v1, v2):
            return self.adyacencias[v1][v2]
    
    def obtener_vertices(self):
        return self.adyacencias.keys()

    def adyacentes(self, vertice):
        if vertice not in self.adyacencias: return []

        return self.adyacencias[vertice].keys()