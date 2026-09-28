"""Testes unitários para correspondência de entidades estatais e sanitização de planilhas."""

import unittest
from utils.entity_matching import check_entity_match, clean_party, sanitize_excel_cell


class TestEntityMatching(unittest.TestCase):

    def test_check_entity_match_principais_estatais(self):
        self.assertEqual(
            check_entity_match("CAIXA ECONOMICA FEDERAL"),
            "Caixa Econômica Federal (CEF)"
        )
        self.assertEqual(
            check_entity_match("Empresa Brasileira de Correios e Telégrafos - ECT"),
            "Empresa Brasileira de Correios e Telégrafos (ECT)"
        )
        self.assertEqual(
            check_entity_match("Petróleo Brasileiro S.A. - Petrobras"),
            "Petróleo Brasileiro S.A. - Petrobras"
        )
        self.assertEqual(
            check_entity_match("Banco do Brasil S.A."),
            "Banco do Brasil S.A."
        )
        self.assertEqual(
            check_entity_match("Companhia do Metropolitano de São Paulo"),
            "Companhia do Metropolitano de São Paulo (Metrô SP)"
        )
        self.assertEqual(
            check_entity_match("Empresa de Gestão de Recursos do Piauí"),
            "Emgerpi"
        )

    def test_clean_party(self):
        raw = "A Caixa Econômica Federal Advogado(a) Fulano de Tal OAB/DF 1234"
        res = clean_party(raw)
        self.assertNotIn("Advogado", res)
        self.assertNotIn("OAB", res)
        self.assertEqual(res, "Caixa Econômica Federal")

    def test_sanitize_excel_cell(self):
        # Caracteres de controle ASCII < 32 que quebram o openpyxl
        bad_str = "Texto com caracter de controle \x00\x01\x02\x08 e quebra válida\n"
        cleaned = sanitize_excel_cell(bad_str)
        self.assertNotIn("\x00", cleaned)
        self.assertNotIn("\x01", cleaned)
        self.assertIn("Texto com caracter de controle", cleaned)


if __name__ == "__main__":
    unittest.main()
