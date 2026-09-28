"""Testes unitários para validação e extração de numerações CNJ e tribunais."""

import unittest
from utils.cnj_utils import (
    extract_cnj,
    extract_tribunal,
    extract_year_from_cnj,
    extract_classe_processual,
)


class TestCnjUtils(unittest.TestCase):

    def test_extract_cnj_num_formatado(self):
        reg = {"numFormatado": "DCG - 1000975-72.2026.5.00.0000"}
        self.assertEqual(extract_cnj(reg), "1000975-72.2026.5.00.0000")

    def test_extract_cnj_numeracao_unica(self):
        reg = {
            "numeracaoUnica": {
                "numero": 1000975,
                "digito": 72,
                "ano": 2026,
                "orgao": 5,
                "tribunal": 0,
                "vara": 0
            }
        }
        self.assertEqual(extract_cnj(reg), "1000975-72.2026.5.00.0000")

    def test_extract_tribunal(self):
        self.assertEqual(extract_tribunal("1000975-72.2026.5.00.0000"), "TST")
        self.assertEqual(extract_tribunal("0010500-12.2020.5.02.0000"), "TRT-02 (SP)")
        self.assertEqual(extract_tribunal("0010500-12.2020.5.15.0000"), "TRT-15 (Campinas/SP)")
        self.assertEqual(extract_tribunal("0010500-12.2020.5.10.0000"), "TRT-10 (DF/TO)")

    def test_extract_year_from_cnj(self):
        self.assertEqual(extract_year_from_cnj("1000975-72.2026.5.00.0000"), "2026")
        self.assertEqual(extract_year_from_cnj("0001234-56.2018.5.02.0000"), "2018")

    def test_extract_classe_processual(self):
        self.assertEqual(extract_classe_processual("DCG"), "Dissídio Coletivo de Greve (DCG)")
        self.assertEqual(extract_classe_processual("DC"), "Dissídio Coletivo (DC)")
        self.assertEqual(extract_classe_processual("RODC"), "Recurso Ordinário em Dissídio Coletivo (RODC)")
        self.assertEqual(extract_classe_processual("ROT"), "Recurso Ordinário Trabalhista (ROT)")
        self.assertEqual(extract_classe_processual("RO"), "Recurso Ordinário (RO)")


if __name__ == "__main__":
    unittest.main()
