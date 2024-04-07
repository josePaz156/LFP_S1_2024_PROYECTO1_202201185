from graphviz import Digraph

class AFD:
    def __init__(self, estados, alfabeto, estado_inicial, estados_aceptacion, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = transiciones

    def generar_diagrama(self):
        dot = Digraph()

        for estado in self.estados:
            if estado in self.estados_aceptacion:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)

        dot.edge('', self.estado_inicial)

        for transicion in self.transiciones:
            origen, destino, simbolo = transicion
            dot.edge(origen, destino, label=simbolo)

        dot.render('afd_lexemas', format='png', cleanup=True)

# Definir los estados, alfabeto, estado inicial, estados de aceptación y transiciones del AFD
estados = ['q0', 'q1', 'q2', 'q3']
alfabeto = ['a', 'b']
estado_inicial = 'q0'
estados_aceptacion = ['q1', 'q2']
transiciones = [('q0', 'q1', 'a'), ('q0', 'q3', 'b'), ('q1', 'q2', 'a'), ('q2', 'q2', 'b'), ('q2', 'q3', 'a')]

# Crear una instancia del AFD
afd = AFD(estados, alfabeto, estado_inicial, estados_aceptacion, transiciones)

# Generar el diagrama
afd.generar_diagrama()