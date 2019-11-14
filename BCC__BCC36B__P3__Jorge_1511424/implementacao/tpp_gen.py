from llvmlite import ir
from tpp_semantic import TppSemantic, FunctionSymbol, VarSymbol


class TppGen:
    def __init__(self, tree, context):
        self.tree = tree
        self.context = context
        self.module = None
        self.current_scope = '@global'

    def generate(self):
        self.module = ir.Module('module')
        self.builder = None

        self.declare_functions(self.tree)
        self._traverse(self.tree)

        print(self.module)

    def declare_functions(self, node):
        for fn_symbol in self.context.symbols:
            if isinstance(fn_symbol, FunctionSymbol):

                parameters = []

                for var_symbol in self.context.symbols:
                    if isinstance(var_symbol, VarSymbol) and var_symbol.scope == fn_symbol.name and var_symbol.parameter:
                        parameters.append(self.type_to_llvmlite_type(
                            var_symbol.type_, var_symbol.dimensions))

                type_ = self.type_to_llvmlite_type(
                    fn_symbol.type_, 0)
                t_func = ir.FunctionType(type_, parameters)
                func = ir.Function(self.module, t_func, name=fn_symbol.name)

    def gen_variable_declaration(self, root):

        variable_list = TppSemantic.tree_to_list(
            "lista_variaveis", root.children[1])

        for var in variable_list:

            name = var.children[0].value
            symbol = self.context.get_symbol(name, self.current_scope)

            if symbol:
                type_ = self.type_to_llvmlite_type(
                    symbol.type_, 0)

                if symbol.scope == '@global':
                    g = ir.GlobalVariable(self.module, type_, symbol.name)
                    g.linkage = 'common'
                    g.align = 4
                else:
                    a = self.builder.alloca(type_, name=symbol.name)
                    a.align = 4

    @classmethod
    def type_to_llvmlite_type(cls, type, dimensions):

        basic_type = None
        if type == 'inteiro':
            basic_type = ir.IntType(32)
        elif type == 'flutuante':
            basic_type = ir.DoubleType()
        else:
            basic_type = ir.VoidType()

        if dimensions == 0:
            return basic_type

        else:

            i = 0
            while i < dimensions:
                basic_type = ir.PointerType(basic_type)
                i += 1

            return basic_type

    def gen_function_declaration(self, root):
        name = TppSemantic.get_function_name(root)
        body = TppSemantic.get_function_body(root)
        fn = self.module.get_global(name)

        self.current_scope = name
        entryBlock = fn.append_basic_block('entry')
        self.builder = ir.IRBuilder(entryBlock)

        self._traverse(body)

        self.current_scope = '@global'

    def _traverse(self, root):
        if root is not None:

            if root.value == 'declaracao_funcao':
                self.gen_function_declaration(root)

            elif root.value == 'declaracao_variaveis':
                self.gen_variable_declaration(root)

            for child in root.children:
                if child is None:
                    continue

                self._traverse(child)
