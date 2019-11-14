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
                    symbol.llvm_ref = g
                else:
                    a = self.builder.alloca(type_, name=symbol.name)
                    a.align = 4
                    symbol.llvm_ref = a

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

    def gen_assignment(self, root):
        name = root.children[0].children[0].value
        expr = self._traverse(root.children[1])

        symbol = self.context.get_symbol(name, self.current_scope)

        if isinstance(expr.type, ir.DoubleType) and symbol.type_ == "inteiro":
            expr = self.builder.fptosi(expr, ir.IntType(32))

        elif isinstance(expr.type, ir.IntType) and symbol.type_ == "flutuante":
            expr = self.builder.sitofp(expr, ir.DoubleType())

        self.builder.store(expr, symbol.llvm_ref)

    def gen_op(self, root, op):
        left = self._traverse(root.children[0])
        right = self._traverse(root.children[1])

        type_ = 'int'

        if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
            if isinstance(left.type, ir.IntType):
                left = self.builder.sitofp(left, ir.DoubleType())
            elif isinstance(right.type, ir.IntType):
                right = self.builder.sitofp(right, ir.DoubleType())

            type_ = 'double'

        if op == '+':
            if type_ == 'int':
                return self.builder.add(left, right, "")

            return self.builder.fadd(left, right, "")

        elif op == '-':
            if type_ == 'int':
                return self.builder.sub(left, right, "")

            return self.builder.fsub(left, right, "")

        elif op == '*':
            if type_ == 'int':
                return self.builder.mul(left, right, "")

            return self.builder.fmul(left, right, "")

        elif op == '/':
            if type_ == 'int':
                return self.builder.sdiv(left, right, "")

            return self.builder.fdiv(left, right, "")

    def _traverse(self, root):
        if root is not None:

            if root.value == 'declaracao_funcao':
                return self.gen_function_declaration(root)

            elif root.value == 'declaracao_variaveis':
                return self.gen_variable_declaration(root)

            elif root.value == 'atribuicao':
                return self.gen_assignment(root)

            elif root.value == '+' or root.value == '-' or root.value == '*' or root.value == '/':
                return self.gen_op(root, root.value)

            elif root.value == 'numero':
                value = root.children[0].value
                if isinstance(value, int):
                    return ir.Constant(ir.IntType(32), value)
                elif isinstance(value, float):
                    return ir.Constant(ir.DoubleType(), value)

            elif root.value == 'var':
                name = root.children[0].value
                symbol = self.context.get_symbol(name, self.current_scope)

                return self.builder.load(symbol.llvm_ref, "")

            for child in root.children:
                if child is None:
                    continue

                self._traverse(child)
