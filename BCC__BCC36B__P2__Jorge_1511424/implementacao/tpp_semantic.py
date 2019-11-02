

class Symbol:
    def __init__(self, name, type_, scope):
        self.name = name
        self.type_ = type_
        self.scope = scope


class VarSymbol(Symbol):
    def __init__(self, name, type_, scope, dimensions=0):
        super().__init__(name, type_, scope)
        self.dimensions = dimensions
        self.initialized = False
        self.used = False

    def __str__(self):
        return '{} [symbol] ({}) [{}] -> {}'.format(self.scope, self.name, self.dimensions, self.type_)


class FunctionSymbol(Symbol):
    def __init__(self, name, type_, scope, parameter_list):
        super().__init__(name, type_, scope)
        self.parameter_list = parameter_list
        self.used = False

    def __str__(self):
        return '{} [function] ({}) {} -> {}'.format(self.scope, self.name, self.parameter_list, self.type_)


class MyException(Exception):
    pass


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
        self.current_scope = '@global'

    def check(self):
        try:
            self.traverse(self.tree)

            self.check_main_function()
            self.check_unused()

            return True
        except MyException as err:
            print(err)
            return False

    def check_main_function(self):
        main = self.context.get_symbol('principal', '@global')
        if main is None:
            raise MyException("Erro: Função principal não declarada")
        elif main.type_ != 'inteiro':
            raise MyException(
                "Erro: Função principal deveria retornar inteiro, mas retorna {}".format(main.type_))

    def check_unused(self):
        for symbol in self.context.symbols:
            if symbol.name != 'principal' and not symbol.used:
                if isinstance(symbol, FunctionSymbol):
                    print(
                        "Aviso: Função ‘{}’ declarada, mas não utilizada.".format(symbol.name))

                else:
                    print('Aviso: Variável ‘{}’ declarada e não utilizada.'.format(
                        symbol.name))

    def function_declaration(self, name, parameter_list, type_):
        if self.context.get_symbol(name, '@global') is None:
            sym = FunctionSymbol(
                name, type_, '@global', [])

            self.current_scope = name

            for param in parameter_list:
                sym.parameter_list.append(
                    VarSymbol(param['name'], param['type'], name, param['dimensions']))

            self.context.add_symbol(sym)
        else:
            print('repetido')

    def verify_function_call(self, name, arg_list):

        # Verifica se está chamando função principal
        if name == 'principal':
            if self.current_scope != 'principal':
                raise MyException(
                    'Erro: Chamada para a função principal não permitida.')
            else:
                print('Aviso: Chamada recursiva para principal.')

        # Verifica se função existe
        func = self.context.get_symbol(name, '@global')

        if func is None:
            raise MyException(
                'Erro: Chamada a função ‘{}’ que não foi declarada.'.format(name))

        else:

            func.used = True

            # Verifica pelo número de argumentos
            count = 0

            if arg_list.children != [None]:

                while arg_list.children[0].value == 'lista_argumentos':
                    arg_list = arg_list.children[0]
                    count += 1

                count += 1

            if len(func.parameter_list) < count:
                raise MyException(
                    'Erro: Chamada à função ‘{}’ com número de parâmetros maior que o declarado.'.format(name))
            elif len(func.parameter_list) > count:
                raise MyException(
                    'Erro: Chamada à função ‘{}’ com número de parâmetros menor que o declarado.'.format(name))

    def verify_var(self, var):
        name = var.children[0].value
        symbol = self.context.get_symbol(name, self.current_scope)

        if symbol is None:
            print('Aviso: Variável ‘{}’ não declarada.'.format(name))

        else:
            if not symbol.initialized:
                print('Aviso: Variável ‘{}’ declarada e não inicializada.'.format(name))

            symbol.used = True

    def tree_to_list(self, key, node):
        tmp = []

        while node.value == key:
            if len(node.children) == 0 or node.children == [None]:
                return []
            elif len(node.children) == 1:
                tmp.insert(0, node.children[0])
            elif len(node.children) == 2:
                tmp.insert(0, node.children[1])

            node = node.children[0]

        return tmp

    def get_function_type(self, function_declaration):
        if len(function_declaration.children) == 1:
            return 'vazio'

        node = function_declaration.children[0]
        while node.value != 'tipo':
            node = node.children[0]

        return node.children[0].value

    def get_function_name(self, function_declaration):
        for node in function_declaration.children:
            if node.value == 'cabecalho':
                return node.children[0].value

    def get_parameter(self, parameter):
        node = parameter
        count = 0
        while node.children[0].value == 'parametro':
            node = node.children[0]
            count += 1

        return {"type": node.children[0].children[0].value, "name": node.children[1].value, "dimensions": count}

    def get_function_parameter_list(self, function_declaration):
        for node in function_declaration.children:
            if node.value == 'cabecalho':
                parameter_nodes = self.tree_to_list(
                    'lista_parametros', node.children[1])

                return list(
                    map(self.get_parameter, parameter_nodes))

    def get_function_body(self, function_declaration):
        for node in function_declaration.children:
            if node.value == 'cabecalho':
                return node.children[2]

    def traverse(self, node):
        if node.value == 'programa':
            self.traverse(node.children[0])

        elif node.value == 'lista_declaracoes':
            for child in node.children:
                self.traverse(child)

        elif node.value == 'declaracao':
            self.traverse(node.children[0])

        elif node.value == 'declaracao_variaveis':
            type_ = node.children[0].children[0].value
            variable_list = self.tree_to_list(
                'lista_variaveis', node.children[1])

            for var in variable_list:
                name = var.children[0].value
                dimensions = 0

                if len(var.children) > 1:
                    index_list = self.tree_to_list('indice', var.children[1])
                    dimensions = len(index_list)

                symbol = self.context.get_symbol(
                    name, self.current_scope)

                if symbol is None:
                    self.context.add_symbol(
                        VarSymbol(name, type_, self.current_scope, dimensions))

                else:
                    print(
                        'Aviso: Variável ‘{}’ já declarada anteriormente.'.format(name))

        elif node.value == 'inicializacao_variaveis':
            pass

        elif node.value == 'declaracao_funcao':
            name = self.get_function_name(node)
            parameter_list = self.get_function_parameter_list(node)
            type_ = self.get_function_type(node)

            self.function_declaration(name, parameter_list, type_)

            self.traverse(self.get_function_body(node))

            self.current_scope = '@global'

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

        elif node.value == 'corpo':
            if len(node.children) == 2:
                self.traverse(node.children[0])
                self.traverse(node.children[1])

        elif node.value == 'acao':
            self.traverse(node.children[0])

        elif node.value == 'expressao':
            self.traverse(node.children[0])

        elif node.value == 'expressao_logica':
            if len(node.children) == 1:
                self.traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'expressao_simples':
            if len(node.children) == 1:
                self.traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'expressao_aditiva':
            if len(node.children) == 1:
                self.traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'expressao_multiplicativa':
            if len(node.children) == 1:
                self.traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'expressao_unaria':
            if len(node.children) == 1:
                self.traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'fator':
            self.traverse(node.children[0])

        elif node.value == 'chamada_funcao':
            name = node.children[0].value
            arg_list = node.children[1]

            self.verify_function_call(name, arg_list)

        elif node.value == 'var':

            self.verify_var(node)

        else:
            print(node)
