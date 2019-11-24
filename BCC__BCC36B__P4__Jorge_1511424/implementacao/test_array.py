from llvmlite import ir, binding

binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()


module = ir.Module('module')
module.triple = binding.get_default_triple()

target = binding.Target.from_default_triple()
target_machine = target.create_target_machine()
backing_mod = binding.parse_assembly("")
engine = binding.create_mcjit_compiler(backing_mod, target_machine)

# int a[2][4][6]

# t = ir.ArrayType(ir.ArrayType(ir.ArrayType(ir.IntType(32), 6), 4), 2)
# i = [ir.Constant.literal_array([
#     ir.Constant.literal_array([ir.Constant(ir.IntType(32), 0)] * 6)
# ] * 4)
# ] * 2


# int a[2]

t = ir.ArrayType(ir.IntType(32), 2)
i = [ir.Constant(ir.IntType(32), 0)] * 2

g = ir.GlobalVariable(module, t, "array")
g.linkage = 'common'
g.initializer = ir.Constant.literal_array(i)
g.align = 4


# a[0] = 5
t_func = ir.FunctionType(ir.IntType(32), [])
func = ir.Function(module, t_func, name="main")
entryBlock = func.append_basic_block('entry')
builder = ir.IRBuilder(entryBlock)

print(type(g))


ptr = builder.gep(g, [ir.Constant(ir.IntType(32), 0),
                      ir.Constant(ir.IntType(32), 0)], True)
builder.store(ir.Constant(ir.IntType(32), 5), ptr)


builder.ret(ir.Constant(ir.IntType(32), 0))

llvm_ir = str(module)

print(llvm_ir)

mod = binding.parse_assembly(llvm_ir)
mod.verify()
engine.add_module(mod)
engine.finalize_object()
engine.run_static_constructors()
