

class Symbol:
    def __init__(self, name, type_, scope):
        self.name = name
        self.type_ = type_
        self.scope = scope


class VarSymbol(Symbol):
    def __init__(self, name, type_, scope, dimensions=0):
        super().__init__(name, type_, scope)
        self.dimensions = dimensions


class FunctionSymbol(Symbol):
    def __init__(self, name, type_, scope, parameter_list):
        super().__init__(name, type_, scope)
        self.parameter_list = parameter_list


class Context:
    def __init__(self):
        self.symbols = []

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def get_symbol(self, name, scope):
        symbol = next(filter(
            lambda k: k.scope == scope and k.name == name, self.symbols), None)

        if symbol is None:
            scope_symbols = next(filter(
                lambda k: k.scope == '@global' and k.name == name, self.symbols), None)

        return symbol


class TppSemantic:
    def __init__(self, tree):
        self.tree = tree
        self.context = Context()

        self.current_function = None

    def check(self):
        try:
            self.traverse(self.tree)
            self.check_main_function()

            return True
        except BaseException as err:
            print(err)
            return False

    def check_main_function(self):
        main = self.context.get_symbol('principal', '@global')
        if main is None:
            raise BaseException("Função principal não declarada")
        elif main.type_ != 'inteiro':
            raise BaseException(
                "Função principal deveria retornar inteiro, mas retorna vazio")

    def function_declaration(self, name, parameter_list, type_):
        if self.context.get_symbol(name, '@global') is None:
            sym = FunctionSymbol(
                name, type_, '@global', parameter_list)

            self.current_function = sym
            print('entrou na ', parameter_list)
            self.context.add_symbol(sym)
        else:
            print('repetido')

    def traverse(self, node):
        if node.value == 'programa':
            self.traverse(node.children[0])

        elif node.value == 'lista_declaracoes':
            for child in node.children:
                self.traverse(child)

        elif node.value == 'declaracao':
            self.traverse(node.children[0])

        elif node.value == 'declaracao_variaveis':
            pass

        elif node.value == 'inicializacao_variaveis':
            pass

        elif node.value == 'declaracao_funcao':

            if len(node.children) == 1:
                header = self.traverse(node.children[0])
                self.function_declaration(
                    header["name"], header["parameter_list"], 'void')
            else:
                type_ = self.traverse(node.children[0]).value
                header = self.traverse(node.children[1])
                self.function_declaration(
                    header["name"], header["parameter_list"], type_)

        elif node.value == 'tipo':
            return node.children[0]

        elif node.value == 'cabecalho':
            name = node.children[0].value
            parameter_list = self.traverse(node.children[1])
            body = self.traverse(node.children[2])

            return {"name": name, "parameter_list": parameter_list, "body": body}

        elif node.value == 'lista_parametros':
            params = []

            if node.children != [None]:
                if len(node.children) > 1:
                    params.append(self.traverse(node.children[0])[0])
                    params.append(self.traverse(node.children[1]))
                else:
                    params.append(self.traverse(node.children[0]))
            return params

        elif node.value == 'parametro':

            def count_parameter_depth(p):
                if p.children[0].value == 'parametro':
                    dim, tmp = count_parameter_depth(p.children[0])
                    return (dim+1, tmp)
                return (0, p)

            if len(node.children) == 1:
                # é um vetor
                dim, p = count_parameter_depth(node.children[0])
                type_ = self.traverse(p.children[0]).value
                name = p.children[1].value

                return {"name": name, "type": type_, "dimensions": dim + 1}
            else:
                type_ = self.traverse(node.children[0]).value
                name = node.children[1].value

                return {"name": name, "type": type_, "dimensions": 0}
