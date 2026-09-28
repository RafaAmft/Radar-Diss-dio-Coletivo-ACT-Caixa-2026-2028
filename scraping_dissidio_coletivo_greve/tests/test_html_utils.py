"""Testes unitários para utilitários de limpeza de HTML e extração documental."""

import unittest
from utils.html_utils import clean_html, extract_clean_document


class TestHtmlUtils(unittest.TestCase):

    def test_clean_html_basic(self):
        html_input = "<p>Decis&atilde;o <b>procedente</b> em parte.</p><script>alert('x');</script>"
        res = clean_html(html_input)
        self.assertIn("Decisão", res)
        self.assertIn("procedente em parte.", res)
        self.assertNotIn("<p>", res)
        self.assertNotIn("alert", res)

    def test_clean_html_none_or_empty(self):
        self.assertEqual(clean_html(None), "")
        self.assertEqual(clean_html(""), "")

    def test_extract_clean_document_ementa(self):
        reg = {
            "ementa": "<p>RECURSO ORDINÁRIO EM DISSÍDIO COLETIVO DE GREVE.</p>",
            "dispositivo": "<p>Acordam os Ministros da SDC em homologar o acordo.</p>"
        }
        doc_type, text = extract_clean_document(reg)
        self.assertEqual(doc_type, "Ementa do Acórdão")
        self.assertIn("EMENTA OFICIAL", text)
        self.assertIn("DISPOSITIVO", text)
        self.assertIn("homologar o acordo", text)

    def test_extract_clean_document_despacho_filtering(self):
        raw = """
        PODER JUDICIÁRIO
        JUSTIÇA DO TRABALHO
        TRIBUNAL SUPERIOR DO TRABALHO
        PROCESSO Nº 1000975-72.2026.5.00.0000
        SUSCITANTE: CAIXA ECONÔMICA FEDERAL
        ADVOGADO: FULANO DE TAL
        
        Trata-se de dissídio coletivo de greve instaurado pela Caixa em face da CONTRAF.
        Defiro a liminar para fixar 60% de contingente.
        """
        reg = {
            "tipo": {"nome": "Decisão Liminar"},
            "txtConteudoDecisao": raw
        }
        doc_type, text = extract_clean_document(reg)
        self.assertEqual(doc_type, "Decisão Liminar do Relator")
        self.assertNotIn("PODER JUDICIÁRIO", text)
        self.assertIn("Trata-se de dissídio coletivo", text)
        self.assertIn("Defiro a liminar", text)


if __name__ == "__main__":
    unittest.main()
