; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

declare void @escrevaInteiro(i32) local_unnamed_addr

declare void @escrevaFlutuante(double) local_unnamed_addr

declare i32 @leiaInteiro() local_unnamed_addr

declare double @leiaFlutuante() local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  %.4 = call i32 @leiaInteiro()
  %.6 = call double @leiaFlutuante()
  call void @escrevaInteiro(i32 %.4)
  call void @escrevaFlutuante(double %.6)
  ret i32 0
}

; Function Attrs: nounwind
declare void @llvm.stackprotector(i8*, i8**) #0

attributes #0 = { nounwind }
