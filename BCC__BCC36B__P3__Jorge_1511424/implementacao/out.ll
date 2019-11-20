; ModuleID = "module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(double %".1") 

declare i32 @"leiaInteiro"() 

declare double @"leiaFlutuante"() 

define i32 @"main"() 
{
entry:
  %"x" = alloca i32, align 4
  %"y" = alloca double, align 4
  store i32 0, i32* %"x"
  store double              0x0, double* %"y"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"x"
  %".6" = call double @"leiaFlutuante"()
  store double %".6", double* %"y"
  %".8" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %".8")
  %".10" = load double, double* %"y"
  call void @"escrevaFlutuante"(double %".10")
  ret i32 0
}
