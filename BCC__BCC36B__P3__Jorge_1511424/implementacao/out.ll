; ModuleID = "module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(double %".1") 

declare i32 @"leiaInteiro"() 

declare double @"leiaFlutuante"() 

define i32 @"fatorial"(i32 %"n") 
{
entry:
  %"n.1" = alloca i32, align 4
  store i32 %"n", i32* %"n.1"
  %"fat" = alloca i32, align 4
  %".4" = load i32, i32* %"n.1"
  %".5" = icmp ugt i32 %".4", 0
  br i1 %".5", label %"iftrue", label %"iffalse"
iftrue:
  store i32 1, i32* %"fat"
  br label %"loop_body"
iffalse:
  ret i32 0
ifend:
  store i32 2, i32* %"n.1"
  br label %"loop_body"
loop_body:
  %".10" = load i32, i32* %"fat"
  %".11" = load i32, i32* %"n.1"
  %".12" = mul i32 %".10", %".11"
  store i32 %".12", i32* %"fat"
  %".14" = load i32, i32* %"n.1"
  %".15" = sub i32 %".14", 1
  store i32 %".15", i32* %"n.1"
  br label %"loop_cond"
loop_cond:
  %".18" = load i32, i32* %"n.1"
  %".19" = icmp eq i32 %".18", 0
  br i1 %".19", label %"loop_end", label %"loop_body"
loop_end:
  %".21" = load i32, i32* %"fat"
  ret i32 %".21"
}

define i32 @"main"() 
{
entry:
  %".2" = call i32 @"leiaInteiro"()
  store i32 %".2", i32* @"n"
  %".4" = load i32, i32* @"n"
  %".5" = call i32 @"fatorial"(i32 %".4")
  call void @"escrevaInteiro"(i32 %".5")
  ret i32 0
}

@"n" = common global i32 0, align 4