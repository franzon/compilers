#include <stdio.h>

void escrevaInteiro(int ni)
{
    printf("%d\n", ni);
}

void escrevaFlutuante(double nf)
{
    printf("%lf\n", nf);
}

int leiaInteiro()
{
    int num;
    scanf("%d", &num);
    return num;
}

double leiaFlutuante()
{
    double num;
    scanf("%lf", &num);
    return num;
}