import ply.yacc as yacc
from tpp_lexer import TppLexer
from graphviz import Digraph


class Node:
    counter = 0

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
        self.id = Node.counter
        Node.counter += 1

    def __str__(self):
        return '{}\n{}'.format(self.id, self.value)


class TppParser():
    tokens = TppLexer.tokens

    def __init__(self, **kwargs):
        self.lexer = TppLexer()
        self.parser = yacc.yacc(module=self, debug=True, **kwargs)
        self.graph = Digraph(comment='Análise sintática')

    def p_programa(self, p):
        '''programa : lista_declaracoes'''
        p[0] = Node('programa', [p[1]])

    def p_lista_declaracoes(self, p):
        '''lista_declaracoes : lista_declaracoes declaracao
                             | declaracao'''
        if len(p) == 3:
            p[0] = Node('lista_declaracoes', [p[1], p[2]])
        else:
            p[0] = Node('lista_declaracoes', [p[1]])

    def p_declaracao(self, p):
        '''declaracao : declaracao_variaveis
                      | inicializacao_variaveis
                      | declaracao_funcao'''
        p[0] = Node('declaracao', [p[1]])

    def p_declaracao_variaveis(self, p):
        '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
        p[0] = Node('declaracao_variaveis', [p[1], p[3]])

    def p_inicializacao_variaveis(self, p):
        '''inicializacao_variaveis : atribuicao'''
        p[0] = Node('inicializacao_variaveis', [p[1]])

    def p_lista_variaveis(self, p):
        '''lista_variaveis : lista_variaveis VIRGULA var
                           | var'''
        if len(p) == 4:
            p[0] = Node('lista_variaveis', [p[1], p[3]])
        else:
            p[0] = Node('lista_variaveis', [p[1]])

    def p_var(self, p):
        '''var : ID
               | ID indice'''

        if len(p) == 2:
            p[0] = Node('var', [Node(p[1])])
        else:
            p[0] = Node('var', [Node(p[1]), p[2]])

    def p_indice(self, p):
        '''indice : indice ABRE_COL expressao FECHA_COL
                  | ABRE_COL expressao FECHA_COL'''
        if len(p) == 5:
            p[0] = Node('indice', [p[1], p[3]])
        else:
            p[0] = Node('indice', [p[2]])

    def p_tipo(self, p):
        '''tipo : INTEIRO
                | FLUTUANTE'''
        p[0] = Node('tipo', [Node(p[1])])

    def p_declaracao_funcao(self, p):
        '''declaracao_funcao : tipo cabecalho
                             | cabecalho'''
        if len(p) == 3:
            p[0] = Node('declaracao_funcao', [p[1], p[2]])
        else:
            p[0] = Node('declaracao_funcao', [p[1]])

    def p_cabecalho(self, p):
        '''cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM'''
        p[0] = Node('cabecalho', [Node(p[1]), p[3], p[5]])

    def p_lista_parametros(self, p):
        '''lista_parametros : lista_parametros VIRGULA parametro
                            | parametro
                            | vazio'''
        if len(p) == 4:
            p[0] = Node('lista_parametros', [p[1], p[3]])
        else:
            p[0] = Node('lista_parametro', [p[1]])

    def p_parametro_1(self, p):
        '''parametro : tipo DOIS_PONTOS ID'''
        p[0] = Node('parametro', [p[1], Node(p[3])])

    def p_parametro_2(self, p):
        '''parametro : parametro ABRE_COL FECHA_COL'''
        p[0] = Node('parametro', [p[1]])

    def p_corpo(self, p):
        '''corpo : corpo acao
                 | vazio'''
        if len(p) == 3:
            p[0] = Node('corpo', [p[1], p[2]])
        else:
            p[0] = Node('corpo', [p[1]])

    def p_acao(self, p):
        '''acao : expressao
                | declaracao_variaveis
                | se
                | repita
                | leia
                | escreva
                | retorna
                | error'''
        p[0] = Node('acao', [p[1]])

    def p_se(self, p):
        '''se : SE expressao ENTAO corpo FIM
              | SE expressao ENTAO corpo SENAO corpo FIM'''
        if len(p) == 6:
            p[0] = Node('se', [p[2], p[4]])
        else:
            p[0] = Node('se', [p[2], p[4], p[6]])

    def p_repita(self, p):
        '''repita : REPITA corpo ATE expressao'''
        p[0] = Node('repita', [p[2], p[4]])

    def p_atribuicao(self, p):
        '''atribuicao : var ATRIBUICAO expressao'''
        p[0] = Node('atribuicao', [p[1], p[3]])

    def p_leia(self, p):
        '''leia : LEIA ABRE_PAR var FECHA_PAR'''
        p[0] = Node('leia', [p[3]])

    def p_escreva(self, p):
        '''escreva : ESCREVA ABRE_PAR expressao FECHA_PAR'''
        p[0] = Node('escreva', [p[3]])

    def p_retorna(self, p):
        '''retorna : RETORNA ABRE_PAR expressao FECHA_PAR'''
        p[0] = Node('retorna', [p[3]])

    def p_expressao(self, p):
        '''expressao : expressao_logica
                     | atribuicao'''
        p[0] = Node('expressao', [p[1]])

    def p_expressao_logica(self, p):
        '''expressao_logica : expressao_simples
                             | expressao_logica operador_logico expressao_simples'''
        if len(p) == 2:
            p[0] = Node('expressao_logica', [p[1]])
        else:
            p[0] = Node('expressao_logica', [p[1], p[2], p[3]])

    def p_expressao_simples(self, p):
        '''expressao_simples : expressao_aditiva
                             | expressao_simples operador_relacional expressao_aditiva'''
        if len(p) == 2:
            p[0] = Node('expressao_simples', [p[1]])
        else:
            p[0] = Node('expressao_simples', [p[1], p[2], p[3]])

    def p_expressao_aditiva(self, p):
        '''expressao_aditiva : expressao_multiplicativa
                             | expressao_aditiva operador_soma expressao_multiplicativa'''
        if len(p) == 2:
            p[0] = Node('expressao_aditiva', [p[1]])
        else:
            p[0] = Node('expressao_aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        '''expressao_multiplicativa : expressao_unaria
                                    | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
        if len(p) == 2:
            p[0] = Node('expressao_multiplicativa', [p[1]])
        else:
            p[0] = Node('expressao_multiplicativa', [p[1], p[2], p[3]])

    def p_expressao_unaria(self, p):
        '''expressao_unaria : fator
                            | operador_soma fator
                            | operador_negacao fator'''
        if len(p) == 2:
            p[0] = Node('expressao_unaria', [p[1]])
        else:
            p[0] = Node('expressao_unaria', [p[1], p[2]])

    def p_operador_relacional(self, p):
        '''operador_relacional : MENOR
                               | MAIOR
                               | IGUALDADE
                               | DESIGUALDADE
                               | MENOR_IGUAL
                               | MAIOR_IGUAL'''
        p[0] = Node('operador_relacional', [Node(p[1])])

    def p_operador_soma(self, p):
        '''operador_soma : SOMA
                          | SUBTRACAO'''
        p[0] = Node('operador_soma', [Node(p[1])])

    def p_operador_logico(self, p):
        '''operador_logico : E_LOGICO
                           | OU_LOGICO'''
        p[0] = Node('operador_logico', [Node(p[1])])

    def p_operador_negacao(self, p):
        '''operador_negacao : NEGACAO'''
        p[0] = Node('operador_negacao', [Node(p[1])])

    def p_operador_multiplicacao(self, p):
        '''operador_multiplicacao : MULTIPLICACAO
                                  | DIVISAO'''
        p[0] = Node('operador_multiplicacao', [Node(p[1])])

    def p_fator(self, p):
        '''fator : ABRE_PAR expressao FECHA_PAR
                 | var
                 | chamada_funcao
                 | numero'''
        if len(p) == 4:
            p[0] = Node('fator', [p[2]])
        else:
            p[0] = Node('fator', [p[1]])

    def p_numero(self, p):
        '''numero : NUM_INTEIRO
                  | NUM_PONTO_FLUTUANTE
                  | NUM_NOTACAO_CIENTIFICA'''
        p[0] = Node('numero', [Node(p[1])])

    def p_chamada_funcao(self, p):
        '''chamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PAR'''
        p[0] = Node('chamada_funcao', [Node(p[1]), p[3]])

    def p_lista_argumentos(self, p):
        '''lista_argumentos : lista_argumentos VIRGULA expressao
                            | expressao
                            | vazio'''

        if len(p) == 4:
            p[0] = Node('lista_argumentos', [p[1], p[3]])
        else:
            p[0] = Node('lista_argumentos', [p[1]])

    def p_comentario(self, p):
        '''comentario : COMENTARIO'''
        p[0] = Node('comentario', [p[1]])

    def p_vazio(self, p):
        '''vazio :'''
        pass

    def p_error(self, p):
        print('Erro de sintaxe ({}) na linha {}, coluna {}'.format(
            p.type, p.lineno, self.find_column(self.input, p)))

    def input_data(self, data):
        self.input = data
        self.result = self.parser.parse(data)

    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def build_graph(self):
        def traverse(root, i):
            if root is not None:
                for child in root.children:
                    if child is None:
                        continue
                    self.graph.node(str(child))
                    self.graph.edge(str(root), str(child))
                    if isinstance(child, Node):
                        traverse(child, i+1)

        self.graph.node(str(self.result))
        traverse(self.result, 0)

        self.graph.render()
