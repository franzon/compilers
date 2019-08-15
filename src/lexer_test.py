import unittest
from lexer import lexer


class TestLexer(unittest.TestCase):
    def test_fatorial(self):

        arq = open('./codes/fatorial.tpp')
        lexer.input(arq.read())
        arq.close()

        tokens = list(map(lambda token: (token.type, token.value),
                          [token for token in lexer]))

        self.assertSequenceEqual(
            tokens, [('INTEIRO', 'inteiro'), ('DOIS_PONTOS', ':'), ('IDENTIFICADOR', 'n'),
                     ('INTEIRO', 'inteiro'), ('IDENTIFICADOR', 'fatorial'), ('ABRE_PARENTESES',
                                                                             '('), ('INTEIRO', 'inteiro'), ('DOIS_PONTOS', ':'), ('IDENTIFICADOR', 'n'), ('FECHA_PARENTESES', ')'),
                     ('INTEIRO', 'inteiro'), ('DOIS_PONTOS',
                                              ':'), ('IDENTIFICADOR', 'fat'),
                     ('SE', 'se'), ('IDENTIFICADOR', 'n'), ('MAIOR',
                                                            '>'), ('INTEIRO_LITERAL', 0), ('ENTAO', 'então'),
                     ('IDENTIFICADOR', 'fat'), ('ATRIBUICAO',
                                                ':='), ('INTEIRO_LITERAL', 1),
                     ('REPITA', 'repita'),
                     ('IDENTIFICADOR', 'fat'), ('ATRIBUICAO', ':='), ('IDENTIFICADOR',
                                                                      'fat'), ('MULTIPLICACAO', '*'), ('IDENTIFICADOR', 'n'),
                     ('IDENTIFICADOR', 'n'), ('ATRIBUICAO', ':='), ('IDENTIFICADOR',
                                                                    'n'), ('SUBTRACAO', '-'), ('INTEIRO_LITERAL', 1),
                     ('ATE', 'até'), ('IDENTIFICADOR',
                                      'n'),  ('IGUAL', '='), ('INTEIRO_LITERAL', 0),
                     ('RETORNA', 'retorna'), ('ABRE_PARENTESES', '('), ('IDENTIFICADOR',
                                                                        'fat'), ('FECHA_PARENTESES', ')'), ('SENAO', 'senão'),
                     ('RETORNA', 'retorna'), ('ABRE_PARENTESES',
                                              '('),  ('INTEIRO_LITERAL', 0), ('FECHA_PARENTESES', ')'), ('FIM', 'fim'), ('FIM', 'fim'),
                     ('INTEIRO', 'inteiro'), ('IDENTIFICADOR',
                                              'principal'), ('ABRE_PARENTESES', '('), ('FECHA_PARENTESES', ')'),
                     ('LEIA', 'leia'), ('ABRE_PARENTESES',
                                        '('), ('IDENTIFICADOR', 'n'), ('FECHA_PARENTESES', ')'),
                     ('ESCREVA', 'escreva'), ('ABRE_PARENTESES', '('), ('IDENTIFICADOR', 'fatorial'), ('ABRE_PARENTESES',
                                                                                                       '('), ('IDENTIFICADOR', 'n'), ('FECHA_PARENTESES', ')'), ('FECHA_PARENTESES', ')'),
                     ('RETORNA', 'retorna'), ('ABRE_PARENTESES',
                                              '('), ('INTEIRO_LITERAL', 0), ('FECHA_PARENTESES', ')'),
                     ('FIM', 'fim')
                     ])

    def test_literals(self):

        arq = open('./codes/literals.tpp')
        lexer.input(arq.read())
        arq.close()

        tokens = list(map(lambda token: (token.type, token.value),
                          [token for token in lexer]))

        self.assertSequenceEqual(
            tokens, [('INTEIRO_LITERAL', 1), ('FLUTUANTE_LITERAL', 1.0), ('FLUTUANTE_LITERAL', 1.23)])


if __name__ == '__main__':
    unittest.main()
