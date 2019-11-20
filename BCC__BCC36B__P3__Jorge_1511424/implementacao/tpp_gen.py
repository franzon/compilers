from llvmlite import ir, binding
from tpp_semantic import TppSemantic, FunctionSymbol, VarSymbol


class TppGen:
    def __init__(self, tree, context):
        self.tree = tree
        self.context = context
        self.module = None
        self.engine = None
        self.binding = binding
        self.current_scope = '@global'
        self.runtime_functions = {}
        self.last_block = None

    def generate(self):

        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()

        self.binding.load_library_permanently('./io.so')

        self.module = ir.Module('module')
        self.module.triple = self.binding.get_default_triple()

        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

        self.builder = None

        self.declare_runtime_functions()

        self.declare_functions(self.tree)
        self._traverse(self.tree)

        # print(self.module)

        main = self.module.get_global("principal")
        main.name = "main"

        llvm_ir = str(self.module)

        print(llvm_ir)
        mod = self.binding.parse_assembly(llvm_ir)
        mod.verify()
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()

        with open('out.ll', 'w') as out:
            out.write(llvm_ir)

    def declare_runtime_functions(self):
        t_escrevaInteiro = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
        self.runtime_functions["escrevaInteiro"] = ir.Function(
            self.module, t_escrevaInteiro, name="escrevaInteiro")

        t_escrevaFlutuante = ir.FunctionType(ir.VoidType(), [ir.DoubleType()])
        self.runtime_functions["escrevaFlutuante"] = ir.Function(
            self.module, t_escrevaFlutuante, name="escrevaFlutuante")

        t_leiaInteiro = ir.FunctionType(ir.IntType(32), [])
        self.runtime_functions["leiaInteiro"] = ir.Function(
            self.module, t_leiaInteiro, name="leiaInteiro")

        t_leiaFlutuante = ir.FunctionType(ir.DoubleType(), [])
        self.runtime_functions["leiaFlutuante"] = ir.Function(
            self.module, t_leiaFlutuante, name="leiaFlutuante")

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
                    g.initializer = ir.Constant(type_, 0)
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

        i = 0
        for var_symbol in self.context.symbols:
            if isinstance(var_symbol, VarSymbol) and var_symbol.used and var_symbol.scope == fn.name and var_symbol.parameter:
                fn.args[i].name = var_symbol.name

                type_ = self.type_to_llvmlite_type(
                    var_symbol.type_, 0)

                a = self.builder.alloca(type_, name=var_symbol.name)
                self.builder.store(fn.args[i], a)
                a.align = 4
                var_symbol.llvm_ref = a

                i += 1

        self._traverse(body)

        fn_symbol = self.context.get_symbol(name, '@global')
        if fn_symbol.type_ == "vazio":
            self.builder.ret_void()

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

    def gen_return(self, root):
        expr = self._traverse(root.children[0])

        fn_symbol = self.context.get_symbol(self.current_scope, "@global")

        if isinstance(expr.type, ir.DoubleType) and fn_symbol.type_ == "inteiro":
            expr = self.builder.fptosi(expr, ir.IntType(32))

        elif isinstance(expr.type, ir.IntType) and fn_symbol.type_ == "flutuante":
            expr = self.builder.sitofp(expr, ir.DoubleType())

        return self.builder.ret(expr)

    def gen_if(self, root):

        if len(root.children) == 2:
            true_block = root.children[1]
            fn = self.module.get_global(self.current_scope)

            if_true = fn.append_basic_block('iftrue')
            if_end = fn.append_basic_block('ifend')

            cond_block = self._traverse(root.children[0])

            self.builder.cbranch(cond_block, if_true, if_end)

            self.builder.position_at_end(if_true)
            self._traverse(true_block)

            if not self.builder.block.is_terminated:
                self.builder.branch(if_end)

            if not self.builder.block.is_terminated:
                self.builder.branch(if_end)

            self.builder.position_at_end(if_end)
        else:

            true_block = root.children[1]
            false_block = root.children[2]

            fn = self.module.get_global(self.current_scope)

            if_true = fn.append_basic_block('iftrue')
            if_false = fn.append_basic_block('iffalse')
            if_end = fn.append_basic_block('ifend')

            self.last_block = if_end

            cond_block = self._traverse(root.children[0])

            self.builder.cbranch(cond_block, if_true, if_false)

            self.builder.position_at_end(if_true)
            self._traverse(true_block)

            if not self.builder.block.is_terminated:
                self.builder.branch(if_end)

            self.builder.position_at_end(if_false)
            self._traverse(false_block)

            if not self.builder.block.is_terminated:
                self.builder.branch(if_end)

            self.builder.position_at_start(if_end)

    def gen_rel_op(self, root, op):

        if op == '=':
            op = '=='

        elif op == '<>':
            op = '!='

        left = self._traverse(root.children[0])
        right = self._traverse(root.children[1])

        type_ = 'int'

        if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
            if isinstance(left.type, ir.IntType):
                left = self.builder.sitofp(left, ir.DoubleType())
            elif isinstance(right.type, ir.IntType):
                right = self.builder.sitofp(right, ir.DoubleType())

            type_ = 'double'

        if type_ == 'int':
            return self.builder.icmp_unsigned(op, left, right, "")

        return self.builder.fcmp_ordered(op, left, right, "")

    def gen_loop(self, root):

        body_block = root.children[0]

        fn = self.module.get_global(self.current_scope)

        loop_body = fn.append_basic_block('loop_body')
        loop_cond = fn.append_basic_block('loop_cond')
        loop_end = fn.append_basic_block('loop_end')

        self.builder.branch(loop_body)

        self.builder.position_at_end(loop_body)

        if self.last_block:
            print('gen_loop')
            current_block = self.builder.block

            self.builder.position_at_end(self.last_block)
            self.builder.branch(current_block)

            self.builder.position_at_end(current_block)
            self.last_block = None

        self._traverse(body_block)
        self.builder.branch(loop_cond)

        self.builder.position_at_end(loop_cond)
        cond_block = self._traverse(root.children[1])
        self.builder.cbranch(cond_block, loop_end, loop_body)

        self.builder.position_at_end(loop_end)

    def gen_logical_op(self, root, op):
        left = self._traverse(root.children[0])
        right = self._traverse(root.children[1])

        if op == '&&':
            return self.builder.and_(left, right)

        return self.builder.or_(left, right)

    def gen_function_call(self, root):
        name = root.children[0].value
        args_node = root.children[1]

        fn = self.module.get_global(name)

        args = []

        if len(args_node.children) > 0 and args_node.children != [None]:

            def extract_args(root):
                if root.value == 'lista_argumentos':
                    if len(root.children) == 1:
                        return [self._traverse(root.children[0])]
                    elif root.children[0].value != 'lista_argumentos':
                        return [self._traverse(root.children[0]), self._traverse(root.children[1])]
                    else:
                        return extract_args(root.children[0]) + [self._traverse(root.children[1])]

                return root

            args = extract_args(args_node)

        i = 0
        for var_symbol in self.context.symbols:
            if isinstance(var_symbol, VarSymbol) and var_symbol.scope == fn.name and var_symbol.parameter:
                if isinstance(self.type_to_llvmlite_type(var_symbol.type_, 0), ir.IntType) and isinstance(args[i].type, ir.DoubleType):
                    args[i] = self.builder.fptosi(args[i])
                elif isinstance(self.type_to_llvmlite_type(var_symbol.type_, 0), ir.DoubleType) and isinstance(args[i].type, ir.IntType):
                    args[i] = self.builder.sitofp(args[i], ir.DoubleType())
                i += 1

        return self.builder.call(fn, args)

    def gen_not_op(self, root):
        return self.builder.not_(self._traverse(root.children[0]))

    def gen_io_function(self, root):
        if root.value == 'leia':
            var = root.children[0].children[0].value
            symbol = self.context.get_symbol(var, self.current_scope)

            ret = None
            if symbol.type_ == "inteiro":
                ret = self.builder.call(
                    self.runtime_functions["leiaInteiro"], [])
            elif symbol.type_ == "flutuante":
                ret = self.builder.call(
                    self.runtime_functions["leiaFlutuante"], [])

            return self.builder.store(ret, symbol.llvm_ref)
        elif root.value == 'escreva':
            var = self._traverse(root.children[0])
            print("to escreveni", var.type)
            if str(var.type) == 'i32':
                return self.builder.call(self.runtime_functions["escrevaInteiro"], [var])
            else:
                return self.builder.call(self.runtime_functions["escrevaFlutuante"], [var])

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

            elif root.value == "<" or root.value == "<=" or root.value == '>' or root.value == '>=' or root.value == "=" or root.value == "<>":
                return self.gen_rel_op(root, root.value)

            elif root.value == '&&' or root.value == "||":
                return self.gen_logical_op(root, root.value)

            elif root.value == '!':
                return self.gen_not_op(root)

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

            elif root.value == 'retorna':
                return self.gen_return(root)

            elif root.value == 'se':
                return self.gen_if(root)

            elif root.value == 'repita':
                return self.gen_loop(root)

            elif root.value == 'chamada_funcao':
                return self.gen_function_call(root)

            elif root.value == 'escreva' or root.value == 'leia':
                return self.gen_io_function(root)

            for child in root.children:
                if child is None:
                    continue

                self._traverse(child)
