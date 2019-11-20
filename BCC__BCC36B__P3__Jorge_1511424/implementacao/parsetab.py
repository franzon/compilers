
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ABRE_COL ABRE_PAR ATE ATRIBUICAO COMENTARIO DESIGUALDADE DIVISAO DOIS_PONTOS ENTAO ESCREVA E_LOGICO FECHA_COL FECHA_PAR FIM FLUTUANTE ID IGUALDADE INTEIRO LEIA MAIOR MAIOR_IGUAL MENOR MENOR_IGUAL MULTIPLICACAO NEGACAO NUM_INTEIRO NUM_NOTACAO_CIENTIFICA NUM_PONTO_FLUTUANTE OU_LOGICO REPITA RETORNA SE SENAO SOMA SUBTRACAO VIRGULAprograma : lista_declaracoeslista_declaracoes : lista_declaracoes declaracao\n                             | declaracaodeclaracao : declaracao_variaveis\n                      | inicializacao_variaveis\n                      | declaracao_funcaodeclaracao_variaveis : tipo DOIS_PONTOS lista_variaveisinicializacao_variaveis : atribuicaolista_variaveis : lista_variaveis VIRGULA var\n                           | varvar : ID\n               | ID indiceindice : indice ABRE_COL expressao FECHA_COL\n                  | ABRE_COL expressao FECHA_COLtipo : INTEIRO\n                | FLUTUANTEdeclaracao_funcao : tipo cabecalho\n                             | cabecalhocabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIMlista_parametros : lista_parametros VIRGULA parametro\n                            | parametro\n                            | vazioparametro : tipo DOIS_PONTOS IDparametro : parametro ABRE_COL FECHA_COLcorpo : corpo acao\n                 | vazioacao : expressao\n                | declaracao_variaveis\n                | se\n                | repita\n                | leia\n                | escreva\n                | retorna\n                | errorse : SE expressao ENTAO corpo FIM\n              | SE expressao ENTAO corpo SENAO corpo FIMrepita : REPITA corpo ATE expressaoatribuicao : var ATRIBUICAO expressaoleia : LEIA ABRE_PAR var FECHA_PARescreva : ESCREVA ABRE_PAR expressao FECHA_PARretorna : RETORNA ABRE_PAR expressao FECHA_PARexpressao : expressao_logica\n                     | atribuicaoexpressao_logica : expressao_simples\n                             | expressao_logica operador_logico expressao_simplesexpressao_simples : expressao_aditiva\n                             | expressao_simples operador_relacional expressao_aditivaexpressao_aditiva : expressao_multiplicativa\n                             | expressao_aditiva operador_soma expressao_multiplicativaexpressao_multiplicativa : expressao_unaria\n                                    | expressao_multiplicativa operador_multiplicacao expressao_unariaexpressao_unaria : fator\n                            | operador_soma fator\n                            | operador_negacao fatoroperador_relacional : MENOR\n                               | MAIOR\n                               | IGUALDADE\n                               | DESIGUALDADE\n                               | MENOR_IGUAL\n                               | MAIOR_IGUALoperador_soma : SOMA\n                          | SUBTRACAOoperador_logico : E_LOGICO\n                           | OU_LOGICOoperador_negacao : NEGACAOoperador_multiplicacao : MULTIPLICACAO\n                                  | DIVISAOfator : ABRE_PAR expressao FECHA_PAR\n                 | var\n                 | chamada_funcao\n                 | numeronumero : NUM_INTEIRO\n                  | NUM_PONTO_FLUTUANTE\n                  | NUM_NOTACAO_CIENTIFICAchamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PARlista_argumentos : lista_argumentos VIRGULA expressao\n                            | expressao\n                            | vaziocomentario : COMENTARIOvazio :'
    
_lr_action_items = {'INTEIRO':([0,2,3,4,5,6,8,9,14,16,19,20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,73,77,78,79,80,81,85,86,87,88,92,93,95,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[10,10,-3,-4,-5,-6,-8,-18,-2,-17,10,-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,10,-14,-9,-45,-47,-49,-51,-68,10,-26,-13,-75,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,10,-80,10,-37,-39,-40,-41,-35,-80,10,-36,]),'FLUTUANTE':([0,2,3,4,5,6,8,9,14,16,19,20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,73,77,78,79,80,81,85,86,87,88,92,93,95,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[11,11,-3,-4,-5,-6,-8,-18,-2,-17,11,-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,11,-14,-9,-45,-47,-49,-51,-68,11,-26,-13,-75,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,11,-80,11,-37,-39,-40,-41,-35,-80,11,-36,]),'ID':([0,2,3,4,5,6,7,8,9,10,11,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,75,77,78,79,80,81,85,86,87,88,92,93,94,95,96,97,98,99,100,101,102,103,104,106,107,113,114,115,116,117,118,122,123,124,125,126,127,128,129,130,],[13,13,-3,-4,-5,-6,17,-8,-18,-15,-16,-2,24,-17,31,-12,31,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,31,-50,-52,31,31,-70,-71,-61,-62,-65,-72,-73,-74,31,24,31,-63,-64,31,-55,-56,-57,-58,-59,-60,31,31,31,-66,-67,-53,-69,-54,-80,91,-14,-9,-45,-47,-49,-51,-68,31,-26,-13,-75,31,-19,-25,-27,-28,-29,-30,-31,-32,-33,-34,31,-80,31,24,31,31,-80,31,31,-37,-39,-40,-41,-35,-80,31,-36,]),'$end':([1,2,3,4,5,6,8,9,14,16,20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,78,79,80,81,85,86,92,93,95,],[0,-1,-3,-4,-5,-6,-8,-18,-2,-17,-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-9,-45,-47,-49,-51,-68,-13,-75,-19,]),'DOIS_PONTOS':([7,10,11,49,105,],[15,-15,-16,75,15,]),'ATRIBUICAO':([12,13,20,25,31,77,92,],[18,-11,-12,18,-11,-14,-13,]),'ABRE_PAR':([13,17,18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,108,109,110,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[19,19,37,-12,37,-7,-10,-11,-69,-38,-42,-43,-44,-46,64,-48,37,-50,-52,37,37,-70,-71,-61,-62,-65,-72,-73,-74,37,37,-63,-64,37,-55,-56,-57,-58,-59,-60,37,37,37,-66,-67,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,37,-26,-13,-75,37,-25,-27,-28,-29,-30,-31,-32,-33,-34,37,-80,114,115,116,37,37,37,-80,37,37,-37,-39,-40,-41,-35,-80,37,-36,]),'ABRE_COL':([13,20,24,31,47,77,89,90,91,92,],[21,50,21,21,74,-14,74,-24,-23,-13,]),'SOMA':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,38,39,40,41,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[40,-12,40,-7,-10,-11,-69,-38,-42,-43,-44,40,-11,-48,-50,-52,40,-70,-71,-61,-62,-72,-73,-74,40,40,-63,-64,40,-55,-56,-57,-58,-59,-60,40,40,40,-66,-67,-53,-69,-54,-80,-14,-9,-45,40,-49,-51,-68,40,-26,-13,-75,40,-25,-27,-28,-29,-30,-31,-32,-33,-34,40,-80,40,40,40,-80,40,40,-37,-39,-40,-41,-35,-80,40,-36,]),'SUBTRACAO':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,38,39,40,41,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[41,-12,41,-7,-10,-11,-69,-38,-42,-43,-44,41,-11,-48,-50,-52,41,-70,-71,-61,-62,-72,-73,-74,41,41,-63,-64,41,-55,-56,-57,-58,-59,-60,41,41,41,-66,-67,-53,-69,-54,-80,-14,-9,-45,41,-49,-51,-68,41,-26,-13,-75,41,-25,-27,-28,-29,-30,-31,-32,-33,-34,41,-80,41,41,41,-80,41,41,-37,-39,-40,-41,-35,-80,41,-36,]),'NEGACAO':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,38,39,40,41,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[42,-12,42,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,42,-70,-71,-61,-62,-72,-73,-74,42,42,-63,-64,42,-55,-56,-57,-58,-59,-60,42,42,42,-66,-67,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,42,-26,-13,-75,42,-25,-27,-28,-29,-30,-31,-32,-33,-34,42,-80,42,42,42,-80,42,42,-37,-39,-40,-41,-35,-80,42,-36,]),'NUM_INTEIRO':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[43,-12,43,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,43,-50,-52,43,43,-70,-71,-61,-62,-65,-72,-73,-74,43,43,-63,-64,43,-55,-56,-57,-58,-59,-60,43,43,43,-66,-67,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,43,-26,-13,-75,43,-25,-27,-28,-29,-30,-31,-32,-33,-34,43,-80,43,43,43,-80,43,43,-37,-39,-40,-41,-35,-80,43,-36,]),'NUM_PONTO_FLUTUANTE':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[44,-12,44,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,44,-50,-52,44,44,-70,-71,-61,-62,-65,-72,-73,-74,44,44,-63,-64,44,-55,-56,-57,-58,-59,-60,44,44,44,-66,-67,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,44,-26,-13,-75,44,-25,-27,-28,-29,-30,-31,-32,-33,-34,44,-80,44,44,44,-80,44,44,-37,-39,-40,-41,-35,-80,44,-36,]),'NUM_NOTACAO_CIENTIFICA':([18,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,94,96,97,98,99,100,101,102,103,104,106,107,113,115,116,117,118,122,123,124,125,126,127,128,129,130,],[45,-12,45,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,45,-50,-52,45,45,-70,-71,-61,-62,-65,-72,-73,-74,45,45,-63,-64,45,-55,-56,-57,-58,-59,-60,45,45,45,-66,-67,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,45,-26,-13,-75,45,-25,-27,-28,-29,-30,-31,-32,-33,-34,45,-80,45,45,45,-80,45,45,-37,-39,-40,-41,-35,-80,45,-36,]),'FECHA_PAR':([19,20,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,46,47,48,64,68,69,70,71,77,79,80,81,82,83,84,85,86,89,90,91,92,93,111,119,120,121,],[-80,-12,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,72,-21,-22,-80,-53,-69,-54,86,-14,-45,-47,-49,93,-77,-78,-51,-68,-20,-24,-23,-13,-75,-76,124,125,126,]),'VIRGULA':([19,20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,46,47,48,64,68,69,70,77,78,79,80,81,82,83,84,85,86,89,90,91,92,93,111,],[-80,-12,52,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,73,-21,-22,-80,-53,-69,-54,-14,-9,-45,-47,-49,94,-77,-78,-51,-68,-20,-24,-23,-13,-75,-76,]),'FIM':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,95,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,127,-37,-39,-40,-41,-35,-80,130,-36,]),'error':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,104,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,104,-80,104,-37,-39,-40,-41,-35,-80,104,-36,]),'SE':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,106,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,106,-80,106,-37,-39,-40,-41,-35,-80,106,-36,]),'REPITA':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,107,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,107,-80,107,-37,-39,-40,-41,-35,-80,107,-36,]),'LEIA':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,108,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,108,-80,108,-37,-39,-40,-41,-35,-80,108,-36,]),'ESCREVA':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,109,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,109,-80,109,-37,-39,-40,-41,-35,-80,109,-36,]),'RETORNA':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,72,77,78,79,80,81,85,86,87,88,92,93,96,97,98,99,100,101,102,103,104,107,113,117,122,123,124,125,126,127,128,129,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-80,-14,-9,-45,-47,-49,-51,-68,110,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,110,-80,110,-37,-39,-40,-41,-35,-80,110,-36,]),'ATE':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,78,79,80,81,85,86,88,92,93,96,97,98,99,100,101,102,103,104,107,113,123,124,125,126,127,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-9,-45,-47,-49,-51,-68,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,118,-37,-39,-40,-41,-35,-36,]),'SENAO':([20,22,23,24,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,78,79,80,81,85,86,88,92,93,96,97,98,99,100,101,102,103,104,117,122,123,124,125,126,127,130,],[-12,-7,-10,-11,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-9,-45,-47,-49,-51,-68,-26,-13,-75,-25,-27,-28,-29,-30,-31,-32,-33,-34,-80,128,-37,-39,-40,-41,-35,-36,]),'MULTIPLICACAO':([20,25,31,32,34,35,38,39,43,44,45,68,69,70,77,81,85,86,92,93,],[-12,-69,-11,66,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,66,-51,-68,-13,-75,]),'DIVISAO':([20,25,31,32,34,35,38,39,43,44,45,68,69,70,77,81,85,86,92,93,],[-12,-69,-11,67,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,67,-51,-68,-13,-75,]),'MENOR':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,57,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,57,-47,-49,-51,-68,-13,-75,]),'MAIOR':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,58,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,58,-47,-49,-51,-68,-13,-75,]),'IGUALDADE':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,59,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,59,-47,-49,-51,-68,-13,-75,]),'DESIGUALDADE':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,60,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,60,-47,-49,-51,-68,-13,-75,]),'MENOR_IGUAL':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,61,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,61,-47,-49,-51,-68,-13,-75,]),'MAIOR_IGUAL':([20,25,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,62,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,62,-47,-49,-51,-68,-13,-75,]),'E_LOGICO':([20,25,27,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,54,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-45,-47,-49,-51,-68,-13,-75,]),'OU_LOGICO':([20,25,27,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,],[-12,-69,55,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-45,-47,-49,-51,-68,-13,-75,]),'FECHA_COL':([20,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,51,68,69,70,74,76,77,79,80,81,85,86,92,93,],[-12,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,77,-53,-69,-54,90,92,-14,-45,-47,-49,-51,-68,-13,-75,]),'ENTAO':([20,25,26,27,28,29,30,31,32,34,35,38,39,43,44,45,68,69,70,77,79,80,81,85,86,92,93,112,],[-12,-69,-38,-42,-43,-44,-46,-11,-48,-50,-52,-70,-71,-72,-73,-74,-53,-69,-54,-14,-45,-47,-49,-51,-68,-13,-75,117,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'lista_declaracoes':([0,],[2,]),'declaracao':([0,2,],[3,14,]),'declaracao_variaveis':([0,2,87,113,122,129,],[4,4,98,98,98,98,]),'inicializacao_variaveis':([0,2,],[5,5,]),'declaracao_funcao':([0,2,],[6,6,]),'tipo':([0,2,19,73,87,113,122,129,],[7,7,49,49,105,105,105,105,]),'atribuicao':([0,2,18,21,37,50,64,87,94,106,113,115,116,118,122,129,],[8,8,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'cabecalho':([0,2,7,],[9,9,16,]),'var':([0,2,15,18,21,33,36,37,50,52,53,56,63,64,65,87,94,106,113,114,115,116,118,122,129,],[12,12,23,25,25,69,69,25,25,78,69,69,69,25,69,25,25,25,25,119,25,25,25,25,25,]),'indice':([13,24,31,],[20,20,20,]),'lista_variaveis':([15,],[22,]),'expressao':([18,21,37,50,64,87,94,106,113,115,116,118,122,129,],[26,51,71,76,83,97,111,112,97,120,121,123,97,97,]),'expressao_logica':([18,21,37,50,64,87,94,106,113,115,116,118,122,129,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'expressao_simples':([18,21,37,50,53,64,87,94,106,113,115,116,118,122,129,],[29,29,29,29,79,29,29,29,29,29,29,29,29,29,29,]),'expressao_aditiva':([18,21,37,50,53,56,64,87,94,106,113,115,116,118,122,129,],[30,30,30,30,30,80,30,30,30,30,30,30,30,30,30,30,]),'expressao_multiplicativa':([18,21,37,50,53,56,63,64,87,94,106,113,115,116,118,122,129,],[32,32,32,32,32,32,81,32,32,32,32,32,32,32,32,32,32,]),'operador_soma':([18,21,30,37,50,53,56,63,64,65,80,87,94,106,113,115,116,118,122,129,],[33,33,63,33,33,33,33,33,33,33,63,33,33,33,33,33,33,33,33,33,]),'expressao_unaria':([18,21,37,50,53,56,63,64,65,87,94,106,113,115,116,118,122,129,],[34,34,34,34,34,34,34,34,85,34,34,34,34,34,34,34,34,34,]),'fator':([18,21,33,36,37,50,53,56,63,64,65,87,94,106,113,115,116,118,122,129,],[35,35,68,70,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'operador_negacao':([18,21,37,50,53,56,63,64,65,87,94,106,113,115,116,118,122,129,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'chamada_funcao':([18,21,33,36,37,50,53,56,63,64,65,87,94,106,113,115,116,118,122,129,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'numero':([18,21,33,36,37,50,53,56,63,64,65,87,94,106,113,115,116,118,122,129,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'lista_parametros':([19,],[46,]),'parametro':([19,73,],[47,89,]),'vazio':([19,64,72,107,117,128,],[48,84,88,88,88,88,]),'operador_logico':([27,],[53,]),'operador_relacional':([29,79,],[56,56,]),'operador_multiplicacao':([32,81,],[65,65,]),'lista_argumentos':([64,],[82,]),'corpo':([72,107,117,128,],[87,113,122,129,]),'acao':([87,113,122,129,],[96,96,96,96,]),'se':([87,113,122,129,],[99,99,99,99,]),'repita':([87,113,122,129,],[100,100,100,100,]),'leia':([87,113,122,129,],[101,101,101,101,]),'escreva':([87,113,122,129,],[102,102,102,102,]),'retorna':([87,113,122,129,],[103,103,103,103,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> lista_declaracoes','programa',1,'p_programa','tpp_parser.py',28),
  ('lista_declaracoes -> lista_declaracoes declaracao','lista_declaracoes',2,'p_lista_declaracoes','tpp_parser.py',32),
  ('lista_declaracoes -> declaracao','lista_declaracoes',1,'p_lista_declaracoes','tpp_parser.py',33),
  ('declaracao -> declaracao_variaveis','declaracao',1,'p_declaracao','tpp_parser.py',40),
  ('declaracao -> inicializacao_variaveis','declaracao',1,'p_declaracao','tpp_parser.py',41),
  ('declaracao -> declaracao_funcao','declaracao',1,'p_declaracao','tpp_parser.py',42),
  ('declaracao_variaveis -> tipo DOIS_PONTOS lista_variaveis','declaracao_variaveis',3,'p_declaracao_variaveis','tpp_parser.py',46),
  ('inicializacao_variaveis -> atribuicao','inicializacao_variaveis',1,'p_inicializacao_variaveis','tpp_parser.py',50),
  ('lista_variaveis -> lista_variaveis VIRGULA var','lista_variaveis',3,'p_lista_variaveis','tpp_parser.py',54),
  ('lista_variaveis -> var','lista_variaveis',1,'p_lista_variaveis','tpp_parser.py',55),
  ('var -> ID','var',1,'p_var','tpp_parser.py',62),
  ('var -> ID indice','var',2,'p_var','tpp_parser.py',63),
  ('indice -> indice ABRE_COL expressao FECHA_COL','indice',4,'p_indice','tpp_parser.py',71),
  ('indice -> ABRE_COL expressao FECHA_COL','indice',3,'p_indice','tpp_parser.py',72),
  ('tipo -> INTEIRO','tipo',1,'p_tipo','tpp_parser.py',79),
  ('tipo -> FLUTUANTE','tipo',1,'p_tipo','tpp_parser.py',80),
  ('declaracao_funcao -> tipo cabecalho','declaracao_funcao',2,'p_declaracao_funcao','tpp_parser.py',84),
  ('declaracao_funcao -> cabecalho','declaracao_funcao',1,'p_declaracao_funcao','tpp_parser.py',85),
  ('cabecalho -> ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM','cabecalho',6,'p_cabecalho','tpp_parser.py',92),
  ('lista_parametros -> lista_parametros VIRGULA parametro','lista_parametros',3,'p_lista_parametros','tpp_parser.py',101),
  ('lista_parametros -> parametro','lista_parametros',1,'p_lista_parametros','tpp_parser.py',102),
  ('lista_parametros -> vazio','lista_parametros',1,'p_lista_parametros','tpp_parser.py',103),
  ('parametro -> tipo DOIS_PONTOS ID','parametro',3,'p_parametro_1','tpp_parser.py',110),
  ('parametro -> parametro ABRE_COL FECHA_COL','parametro',3,'p_parametro_2','tpp_parser.py',114),
  ('corpo -> corpo acao','corpo',2,'p_corpo','tpp_parser.py',118),
  ('corpo -> vazio','corpo',1,'p_corpo','tpp_parser.py',119),
  ('acao -> expressao','acao',1,'p_acao','tpp_parser.py',126),
  ('acao -> declaracao_variaveis','acao',1,'p_acao','tpp_parser.py',127),
  ('acao -> se','acao',1,'p_acao','tpp_parser.py',128),
  ('acao -> repita','acao',1,'p_acao','tpp_parser.py',129),
  ('acao -> leia','acao',1,'p_acao','tpp_parser.py',130),
  ('acao -> escreva','acao',1,'p_acao','tpp_parser.py',131),
  ('acao -> retorna','acao',1,'p_acao','tpp_parser.py',132),
  ('acao -> error','acao',1,'p_acao','tpp_parser.py',133),
  ('se -> SE expressao ENTAO corpo FIM','se',5,'p_se','tpp_parser.py',137),
  ('se -> SE expressao ENTAO corpo SENAO corpo FIM','se',7,'p_se','tpp_parser.py',138),
  ('repita -> REPITA corpo ATE expressao','repita',4,'p_repita','tpp_parser.py',145),
  ('atribuicao -> var ATRIBUICAO expressao','atribuicao',3,'p_atribuicao','tpp_parser.py',149),
  ('leia -> LEIA ABRE_PAR var FECHA_PAR','leia',4,'p_leia','tpp_parser.py',153),
  ('escreva -> ESCREVA ABRE_PAR expressao FECHA_PAR','escreva',4,'p_escreva','tpp_parser.py',157),
  ('retorna -> RETORNA ABRE_PAR expressao FECHA_PAR','retorna',4,'p_retorna','tpp_parser.py',161),
  ('expressao -> expressao_logica','expressao',1,'p_expressao','tpp_parser.py',165),
  ('expressao -> atribuicao','expressao',1,'p_expressao','tpp_parser.py',166),
  ('expressao_logica -> expressao_simples','expressao_logica',1,'p_expressao_logica','tpp_parser.py',170),
  ('expressao_logica -> expressao_logica operador_logico expressao_simples','expressao_logica',3,'p_expressao_logica','tpp_parser.py',171),
  ('expressao_simples -> expressao_aditiva','expressao_simples',1,'p_expressao_simples','tpp_parser.py',178),
  ('expressao_simples -> expressao_simples operador_relacional expressao_aditiva','expressao_simples',3,'p_expressao_simples','tpp_parser.py',179),
  ('expressao_aditiva -> expressao_multiplicativa','expressao_aditiva',1,'p_expressao_aditiva','tpp_parser.py',186),
  ('expressao_aditiva -> expressao_aditiva operador_soma expressao_multiplicativa','expressao_aditiva',3,'p_expressao_aditiva','tpp_parser.py',187),
  ('expressao_multiplicativa -> expressao_unaria','expressao_multiplicativa',1,'p_expressao_multiplicativa','tpp_parser.py',194),
  ('expressao_multiplicativa -> expressao_multiplicativa operador_multiplicacao expressao_unaria','expressao_multiplicativa',3,'p_expressao_multiplicativa','tpp_parser.py',195),
  ('expressao_unaria -> fator','expressao_unaria',1,'p_expressao_unaria','tpp_parser.py',202),
  ('expressao_unaria -> operador_soma fator','expressao_unaria',2,'p_expressao_unaria','tpp_parser.py',203),
  ('expressao_unaria -> operador_negacao fator','expressao_unaria',2,'p_expressao_unaria','tpp_parser.py',204),
  ('operador_relacional -> MENOR','operador_relacional',1,'p_operador_relacional','tpp_parser.py',211),
  ('operador_relacional -> MAIOR','operador_relacional',1,'p_operador_relacional','tpp_parser.py',212),
  ('operador_relacional -> IGUALDADE','operador_relacional',1,'p_operador_relacional','tpp_parser.py',213),
  ('operador_relacional -> DESIGUALDADE','operador_relacional',1,'p_operador_relacional','tpp_parser.py',214),
  ('operador_relacional -> MENOR_IGUAL','operador_relacional',1,'p_operador_relacional','tpp_parser.py',215),
  ('operador_relacional -> MAIOR_IGUAL','operador_relacional',1,'p_operador_relacional','tpp_parser.py',216),
  ('operador_soma -> SOMA','operador_soma',1,'p_operador_soma','tpp_parser.py',220),
  ('operador_soma -> SUBTRACAO','operador_soma',1,'p_operador_soma','tpp_parser.py',221),
  ('operador_logico -> E_LOGICO','operador_logico',1,'p_operador_logico','tpp_parser.py',225),
  ('operador_logico -> OU_LOGICO','operador_logico',1,'p_operador_logico','tpp_parser.py',226),
  ('operador_negacao -> NEGACAO','operador_negacao',1,'p_operador_negacao','tpp_parser.py',230),
  ('operador_multiplicacao -> MULTIPLICACAO','operador_multiplicacao',1,'p_operador_multiplicacao','tpp_parser.py',234),
  ('operador_multiplicacao -> DIVISAO','operador_multiplicacao',1,'p_operador_multiplicacao','tpp_parser.py',235),
  ('fator -> ABRE_PAR expressao FECHA_PAR','fator',3,'p_fator','tpp_parser.py',239),
  ('fator -> var','fator',1,'p_fator','tpp_parser.py',240),
  ('fator -> chamada_funcao','fator',1,'p_fator','tpp_parser.py',241),
  ('fator -> numero','fator',1,'p_fator','tpp_parser.py',242),
  ('numero -> NUM_INTEIRO','numero',1,'p_numero','tpp_parser.py',249),
  ('numero -> NUM_PONTO_FLUTUANTE','numero',1,'p_numero','tpp_parser.py',250),
  ('numero -> NUM_NOTACAO_CIENTIFICA','numero',1,'p_numero','tpp_parser.py',251),
  ('chamada_funcao -> ID ABRE_PAR lista_argumentos FECHA_PAR','chamada_funcao',4,'p_chamada_funcao','tpp_parser.py',255),
  ('lista_argumentos -> lista_argumentos VIRGULA expressao','lista_argumentos',3,'p_lista_argumentos','tpp_parser.py',259),
  ('lista_argumentos -> expressao','lista_argumentos',1,'p_lista_argumentos','tpp_parser.py',260),
  ('lista_argumentos -> vazio','lista_argumentos',1,'p_lista_argumentos','tpp_parser.py',261),
  ('comentario -> COMENTARIO','comentario',1,'p_comentario','tpp_parser.py',269),
  ('vazio -> <empty>','vazio',0,'p_vazio','tpp_parser.py',273),
]
