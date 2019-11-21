; ModuleID = "module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(double %".1") 

declare i32 @"leiaInteiro"() 

declare double @"leiaFlutuante"() 

define i32 @"soma"(i32 %"x", i32 %"y") 
{
entry:
  %"x.1" = alloca i32, align 4
  store i32 %"x", i32* %"x.1"
  %"y.1" = alloca i32, align 4
  store i32 %"y", i32* %"y.1"
  %".6" = load i32, i32* %"x.1"
  %".7" = load i32, i32* %"y.1"
  %".8" = add i32 %".6", %".7"
  ret i32 %".8"
}

define i32 @"sub"(i32 %"z", i32 %"t") 
{
entry:
  %"z.1" = alloca i32, align 4
  store i32 %"z", i32* %"z.1"
  %"t.1" = alloca i32, align 4
  store i32 %"t", i32* %"t.1"
  %".6" = load i32, i32* %"z.1"
  %".7" = load i32, i32* %"t.1"
  %".8" = add i32 %".6", %".7"
  ret i32 %".8"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"loop_body"
loop_body:
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"a"
  %".6" = call i32 @"leiaInteiro"()
  store i32 %".6", i32* %"b"
  %".8" = load i32, i32* %"a"
  %".9" = load i32, i32* %"b"
  %".10" = call i32 @"soma"(i32 %".8", i32 %".9")
  %".11" = load i32, i32* %"a"
  %".12" = load i32, i32* %"b"
  %".13" = call i32 @"sub"(i32 %".11", i32 %".12")
  %".14" = call i32 @"soma"(i32 %".10", i32 %".13")
  store i32 %".14", i32* %"c"
  %".16" = load i32, i32* %"c"
  call void @"escrevaInteiro"(i32 %".16")
  %".18" = load i32, i32* %"i"
  %".19" = add i32 %".18", 1
  store i32 %".19", i32* %"i"
  br label %"loop_cond"
loop_cond:
  %".22" = load i32, i32* %"i"
  %".23" = icmp eq i32 %".22", 5
  br i1 %".23", label %"loop_end", label %"loop_body"
loop_end:
  ret i32 0
}
