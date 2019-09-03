inteiro fib(n)
    se n = 1 então
        retorna (0)
    senão
        se n = 2 então
            retorna (1)
        senão
            retorna (fib(n - 1) + fib(n - 2))
        fim
    fim
fim