

class Symbol:
    def __init__(self, kind, _type, name, parameters=None):
        self.kind = kind
        self._type = _type
        self.name = name

        if kind == 'function':
            self.parameters = parameters

    def __str__(self):
        return 'kind: ' + self.kind + ' type: ' + self._type + ' name: ' + self.name


class TppSemantic:
    def __init__(self, tree):
        self.tree = tree

        self.global_symbols = {}
        self.symbols = {}

    def check(self):
        self.traverse()

        self.check_for_main()

    def check_for_main(self):
        if 'principal' not in self.global_symbols.keys():
            print('Função principal não existe')

        else:
            if self.global_symbols['principal']._type != 'inteiro':
                print('Função principal deve ser inteiro')

    def add_function(self, _type, name):
        if name in self.global_symbols.keys():
            print('função já existe')
        else:
            self.global_symbols[name] = Symbol('function', _type, name)
            self.symbols[name] = {}

    def traverse(self):

        def _traverse(root):
            if root.value == 'programa':
                return _traverse(root.children[0])
            elif root.value == 'lista_declaracoes':
                _traverse(root.children[0])
                if len(root.children) > 1:
                    _traverse(root.children[1])
            elif root.value == 'declaracao':
                _traverse(root.children[0])
            elif root.value == 'declaracao_funcao':

                if len(root.children) == 1:

                    _type = 'void'
                    header = _traverse(root.children[0])
                    name = header["name"]
                    self.add_function(_type, name)

                else:

                    _type = _traverse(root.children[0]).value
                    header = _traverse(root.children[1])
                    name = header["name"]

                    self.add_function(_type, name)

            elif root.value == 'cabecalho':
                name = root.children[0].value
                parameter_list = _traverse(root.children[1])

                return {"name": name, "parameter_list": parameter_list}

            elif root.value == 'tipo':
                return root.children[0]

        _traverse(self.tree)
