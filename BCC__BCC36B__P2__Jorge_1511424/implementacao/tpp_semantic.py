from tabulate import tabulate
from graphviz import Digraph
from tpp_parser import Node


class Symbol:
    def __init__(self, name, type_, scope):
        self.name = name
        self.type_ = type_
        self.scope = scope
        self.error = False


class VarSymbol(Symbol):
    def __init__(self, name, type_, scope, dimensions=0, parameter=False):
        super().__init__(name, type_, scope)
        self.dimensions = dimensions
        self.initialized = False
        self.used = False
        self.parameter = parameter

    def __str__(self):
        return '{} [symbol] ({}) [{}] -> {}'.format(self.scope, self.name, self.dimensions, self.type_)


class FunctionSymbol(Symbol):
    def __init__(self, name, type_, scope):
        super().__init__(name, type_, scope)
        self.used = False if name != 'principal' else True
        self.returned = False

    def __str__(self):
        return '{} [function] ({}) {} -> {}'.format(self.scope, self.name, self.type_)


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
            symbol = next(filter(
                lambda k: k.scope == '@global' and k.name == name, self.symbols), None)

        return symbol


class TppSemantic:
    def __init__(self, tree):
        self.tree = tree
        self.context = Context()
        self.current_scope = '@global'
        self.graph = Digraph(comment='Análise sintática')

    def traverse(self):
        print('\n====================\nExecutando análise semântica...\n')
        try:
            self.declare_functions(self.tree)
            self._traverse(self.tree)

            self.check_main_function()
            self.check_unused()
            self.check_no_returns()

            return True
        except MyException as err:
            print(err)
            return False

    def prune(self):
        self._prune(self.tree)
        self.build_graph()

    def print_symbols(self):
        functions = list(filter(lambda k: isinstance(
            k, FunctionSymbol), self.context.symbols))
        functions = list(
            map(lambda k: [k.scope, k.type_, k.name, k.used], functions))

        variables = list(filter(lambda k: isinstance(
            k, VarSymbol), self.context.symbols))
        variables = list(
            map(lambda k: [k.scope, k.type_, k.name, k.dimensions, k.initialized, k.used, k.parameter], variables))

        print('\nFunções: \n')
        print(tabulate(functions, headers=[
              'Escopo', 'Tipo', 'Nome', 'Utilizado']))

        print('\nVariáveis: \n')
        print(tabulate(variables, headers=[
              'Escopo', 'Tipo', 'Nome', 'Dimensões', 'Inicializado', 'Utilizado', 'Parâmetro']))

    def check_main_function(self):
        main = self.context.get_symbol('principal', '@global')
        if main is None:
            print("Erro: Função principal não declarada")
        elif main.type_ != 'inteiro':
            print(
                "Erro: Função principal deveria retornar inteiro, mas retorna {}".format(main.type_))

    def check_unused(self):
        for symbol in self.context.symbols:
            if symbol.name != 'principal' and not symbol.used:
                if isinstance(symbol, FunctionSymbol):
                    if not symbol.error:
                        print(
                            "Aviso: Função ‘{}’ declarada, mas não utilizada.".format(symbol.name))
                        symbol.error = True
                else:
                    if not symbol.error:
                        print('Aviso: Variável ‘{}’ declarada e não utilizada.'.format(
                            symbol.name))
                        symbol.error = True

    def check_no_returns(self):
        for symbol in self.context.symbols:
            if isinstance(symbol, FunctionSymbol) and symbol.type_ != 'vazio' and not symbol.returned:
                print('Erro: Função ‘{}’ deveria retornar {}, mas retorna vazio.'.format(
                    symbol.name, symbol.type_))

    def function_declaration(self, name, parameter_list, type_):
        if self.context.get_symbol(name, '@global') is None:
            sym = FunctionSymbol(
                name, type_, '@global')

            # self.current_scope = name

            for param in parameter_list:
                var_symbol = VarSymbol(
                    param['name'], param['type'], name, param['dimensions'], parameter=True)
                self.context.add_symbol(var_symbol)

            self.context.add_symbol(sym)
        else:
            print(
                'Erro: Função ‘{}’ já foi declarada.'.format(name))

    def declare_functions(self, node):
        if node.value == 'programa':
            declaration_list = self.tree_to_list(
                'lista_declaracoes', node.children[0])

            function_declaration_list = list(
                map(lambda k: k.children[0], declaration_list))

            function_declaration_list = list(
                filter(lambda k: k.value == 'declaracao_funcao', function_declaration_list))

            for declaration_node in function_declaration_list:

                name = self.get_function_name(declaration_node)
                parameter_list = self.get_function_parameter_list(
                    declaration_node)
                type_ = self.get_function_type(declaration_node)

                self.function_declaration(name, parameter_list, type_)

    def verify_function_call(self, name, arg_list):

        # Verifica se está chamando função principal
        if name == 'principal':
            if self.current_scope != 'principal':
                print(
                    'Erro: Chamada para a função principal não permitida.')
            else:
                print('Aviso: Chamada recursiva para principal.')

        # Verifica se função existe
        func = self.context.get_symbol(name, '@global')

        if func is None:
            print(
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

            parameter_list = list(filter(lambda k: k.scope == name and isinstance(
                k, VarSymbol) and k.parameter, self.context.symbols))

            if len(parameter_list) < count:
                print(
                    'Erro: Chamada à função ‘{}’     com número de parâmetros maior que o declarado.'.format(name))
            elif len(parameter_list) > count:
                print(
                    'Erro: Chamada à função ‘{}’ com número de parâmetros menor que o declarado.'.format(name))

    def verify_var(self, var, assigning=False):

        name = var.children[0].value
        symbol = self.context.get_symbol(name, self.current_scope)

        if symbol is None:
            print(
                'Erro: Variável ‘{}’ não declarada.'.format(name))

        else:
            symbol.used = True

            if assigning:
                symbol.initialized = True

            else:
                if not symbol.initialized and not symbol.parameter:
                    if not symbol.error:
                        print(
                            'Aviso: Variável ‘{}’ declarada e não inicializada.'.format(name))
                        symbol.error = True

            if len(var.children) == 1:
                if symbol.dimensions > 0:
                    print(
                        "Erro: Não é possível utilizar variável ‘{}’ como escalar.".format(name))

            elif len(var.children) == 2:

                self._traverse(var.children[1])

                index_list = self.tree_to_list('indice', var.children[1])
                index_types = list(map(self.get_expression_type, index_list))

                if symbol.dimensions == 0:
                    print(
                        "Erro: Variável ‘{}’ é escalar.".format(name))

                elif symbol.dimensions != len(index_list):
                    print("Erro: Arranjo ‘{}’ de dimensão {} não pode ser acessado como um arranjo de dimensão {}.".format(
                        name, symbol.dimensions, len(index_list)))

                for index_type in index_types:
                    if index_type != 'inteiro':
                        print(
                            'Erro: Índice de array ‘{}’ não inteiro.'.format(name))

            return symbol

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

    def get_expression_type(self, node):
        if node.value == 'expressao':
            return self.get_expression_type(node.children[0])

        elif node.value == 'expressao_logica':
            return self.get_expression_type(node.children[0])

        elif node.value == 'expressao_simples':
            return self.get_expression_type(node.children[0])

        elif node.value == 'expressao_aditiva':
            if len(node.children) == 1:
                return self.get_expression_type(node.children[0])
            else:
                expr_left_type = self.get_expression_type(node.children[0])
                expr_right_type = self.get_expression_type(node.children[2])

                if expr_left_type == 'flutuante' or expr_right_type == 'flutuante':
                    return 'flutuante'

                return 'inteiro'

        elif node.value == 'expressao_multiplicativa':
            if len(node.children) == 1:
                return self.get_expression_type(node.children[0])
            else:
                expr_left_type = self.get_expression_type(node.children[0])
                expr_right_type = self.get_expression_type(node.children[2])

                if expr_left_type == 'flutuante' or expr_right_type == 'flutuante':
                    return 'flutuante'

                return 'inteiro'

        elif node.value == 'expressao_unaria':
            if len(node.children) == 1:
                return self.get_expression_type(node.children[0])
            else:
                return self.get_expression_type(node.children[1])

        elif node.value == 'fator':
            child = node.children[0]
            if child.value == 'expressao':
                return self.get_expression_type(child)
            elif child.value == 'var':
                # todo: ver se chama check_var
                symbol = self.context.get_symbol(
                    child.children[0].value, self.current_scope)
                if symbol is not None:
                    return symbol.type_

            elif child.value == 'chamada_funcao':
                # todo: ver se chama check_function_call
                symbol = self.context.get_symbol(
                    child.children[0].value, '@global')
                if symbol is not None:
                    return symbol.type_

            elif child.value == 'numero':
                if isinstance(child.children[0].value, float):
                    return 'flutuante'
                elif isinstance(child.children[0].value, int):
                    return 'inteiro'

    def _traverse(self, node):
        if node.value == 'programa':
            self._traverse(node.children[0])

        elif node.value == 'lista_declaracoes':
            for child in node.children:
                self._traverse(child)

        elif node.value == 'declaracao':
            self._traverse(node.children[0])

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
                    if not symbol.error:
                        print(
                            'Aviso: Variável ‘{}’ já declarada anteriormente.'.format(name))
                        symbol.error = True

        elif node.value == 'inicializacao_variaveis':
            pass

        elif node.value == 'declaracao_funcao':
            name = self.get_function_name(node)

            self.current_scope = name
            self._traverse(self.get_function_body(node))
            self.current_scope = '@global'

        elif node.value == 'tipo':
            return node.children[0]

        elif node.value == 'cabecalho':
            name = node.children[0].value
            parameter_list = self._traverse(node.children[1])
            body = self._traverse(node.children[2])

            return {"name": name, "parameter_list": parameter_list, "body": body}

        elif node.value == 'lista_parametros':
            params = []

            if node.children != [None]:
                if len(node.children) > 1:
                    params.append(self._traverse(node.children[0])[0])
                    params.append(self._traverse(node.children[1]))
                else:
                    params.append(self._traverse(node.children[0]))
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
                type_ = self._traverse(p.children[0]).value
                name = p.children[1].value

                return {"name": name, "type": type_, "dimensions": dim + 1}
            else:
                type_ = self._traverse(node.children[0]).value
                name = node.children[1].value

                return {"name": name, "type": type_, "dimensions": 0}

        elif node.value == 'corpo':
            if len(node.children) == 2:
                self._traverse(node.children[0])
                self._traverse(node.children[1])

        elif node.value == 'acao':
            self._traverse(node.children[0])

        elif node.value == 'expressao':
            self._traverse(node.children[0])

        elif node.value == 'expressao_logica':
            if len(node.children) == 1:
                self._traverse(node.children[0])
            else:
                pass  # todo

        elif node.value == 'atribuicao':
            var = node.children[0]
            expression = node.children[1]

            self._traverse(expression)
            symbol = self.verify_var(var, True)

            if symbol is not None:

                type_ = self.get_expression_type(expression)

                if symbol.type_ != type_:
                    print('Aviso: Atribuição de tipos distintos ‘{}’ {} e ‘expressão’ {}'.format(
                        symbol.name, symbol.type_, type_))

        elif node.value == 'expressao_simples':
            # if len(node.children) == 1:
            #     self.traverse(node.children[0])
            # else:
            #     pass  # todo
            for child in node.children:
                self._traverse(child)

        elif node.value == 'expressao_aditiva':
            # if len(node.children) == 1:
            #     self.traverse(node.children[0])
            # else:
            #     pass  # todo
            for child in node.children:
                self._traverse(child)

        elif node.value == 'expressao_multiplicativa':
            # if len(node.children) == 1:
            #     self.traverse(node.children[0])
            # else:
            #     pass  # todo
            for child in node.children:
                self._traverse(child)

        elif node.value == 'expressao_unaria':
            # if len(node.children) == 1:
            #     self.traverse(node.children[0])
            # else:
            #     pass  # todo
            for child in node.children:
                self._traverse(child)

        elif node.value == 'fator':
            self._traverse(node.children[0])

        elif node.value == 'chamada_funcao':
            name = node.children[0].value
            arg_list = node.children[1]

            self.verify_function_call(name, arg_list)

        elif node.value == 'var':
            self.verify_var(node)

        elif node.value == 'indice':
            for child in node.children:
                self._traverse(child)

        elif node.value == 'retorna':

            self._traverse(node.children[0])
            type_ = self.get_expression_type(node.children[0])

            symbol = self.context.get_symbol(self.current_scope, '@global')
            symbol.returned = True

            if type_ is not None and symbol.type_ != type_:  # Função retorna tipo diferente do definido
                print('Erro: Função ‘{}‘ deveria retornar {}, mas retorna {}.'.format(
                    self.current_scope, symbol.type_, type_))

        elif node.value == 'escreva':
            self._traverse(node.children[0])

        elif node.value == 'leia':
            self._traverse(node.children[0])
        # else:
        #     print(node)

    def _prune(self, node):

        expressions = ['expressao_logica', 'expressao_simples',
                       'expressao_aditiva', 'expressao_multiplicativa']

        operators = ['operador_logico', 'operador_relacional',
                     'operador_soma', 'operador_multiplicacao', 'operador_negacao']

        if node is not None and node.children != [None]:

            if node.value in expressions:
                if len(node.children) == 1:
                    return self._prune(node.children[0])

                left = self._prune(node.children[0])
                op = self._prune(node.children[1])
                right = self._prune(node.children[2])

                node.value = op.value
                node.children = [left, right]
                return node

            elif node.value == 'lista_argumentos':
                if len(node.children) == 1:
                    expr = self._prune(node.children[0])
                    node.children = [expr]
                    return node

                else:
                    left = self._prune(node.children[0])
                    expr = self._prune(node.children[1])

                    node.children = [left, expr]

                    return node

            elif node.value == 'atribuicao':
                var = self._prune(node.children[0])
                expr = self._prune(node.children[1])

                node.children = [var, expr]
                return node

            elif node.value == 'fator':
                child = node.children[0]
                if child.value == 'chamada_funcao':
                    func = child.children[0]
                    args = self._prune(child.children[1])

                    child.children[1] = args
                    return child

                return node.children[0]

            elif node.value == 'var':
                return node.children[0]

            elif node.value == 'expressao':
                return self._prune(node.children[0])

            elif node.value == 'expressao_unaria':
                if len(node.children) == 1:
                    return self._prune(node.children[0])

                op = self._prune(node.children[0])
                expr = self._prune(node.children[1])

                node.value = op.value
                node.children = [expr]

                return node

            elif node.value in operators:
                return node.children[0]

            else:

                for child in node.children:
                    self._prune(child)
        # if node is not None and node.children != [None]:

        #     if node.value in expressions:
        #         if len(node.children) == 1:
        #             return self._prune(node.children[0])
        #         else:
        #             expr_left = self._prune(node.children[0])
        #             op = self._prune(node.children[1])
        #             expr_right = self._prune(node.children[2])

        #             op.children = [expr_left, expr_right]

        #             return op

        #     elif node.value in leafs:
        #         return node.children[0]

        #     else:
        #         if len(node.children) == 1:
        #             return self._prune(node.children[0])

        #         for child in node.children:
        #             self._prune(child)

    def build_graph(self):
        def traverse(root, i):
            if root is not None:
                for child in root.children:
                    if child is None:
                        continue
                    self.graph.node(str(child))
                    self.graph.edge(str(root), str(child))
                    if isinstance(child, Node):
                        traverse(child, i+1)

        self.graph.node(str(self.tree))
        traverse(self.tree, 0)

        self.graph.render('pruned')
