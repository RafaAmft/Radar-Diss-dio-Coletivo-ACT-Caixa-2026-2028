import unittest
import os
import sys
import json
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdc_ministers_profile import analyze_decision_content, normalize_relator, build_sdc_ministers_profile

class TestSDCMinistersProfile(unittest.TestCase):

    def test_normalize_relator(self):
        self.assertEqual(normalize_relator("mauricio godinho delgado"), "Mauricio Godinho Delgado")
        self.assertEqual(normalize_relator("IVES GANDRA MARTINS FILHO"), "Ives Gandra Martins Filho")
        self.assertEqual(normalize_relator("katia magalhaes arruda"), "Kátia Magalhães Arruda")
        self.assertEqual(normalize_relator("maria cristina irigoyen peduzzi"), "Maria Cristina Irigoyen Peduzzi")
        self.assertEqual(normalize_relator("guilherme augusto caputo bastos"), "Guilherme Augusto Caputo Bastos")

    def test_analyze_decision_abusividade(self):
        text_abusiva = "Ante o exposto, acordam os Ministros em julgar e declarar a abusividade da greve deflagrada pelo sindicato..."
        res_abusiva = analyze_decision_content(text_abusiva)
        self.assertEqual(res_abusiva['abusividade'], "Abusiva")

        text_nao_abusiva = "Diante do cumprimento dos requisitos legais da Lei 7.783/89, declara-se a não abusividade da greve..."
        res_nao_abusiva = analyze_decision_content(text_nao_abusiva)
        self.assertEqual(res_nao_abusiva['abusividade'], "Não Abusiva")

    def test_analyze_decision_dias_parados(self):
        text_desconto = "Com base na OJ nº 10 da SDC do TST, determina-se o desconto dos dias parados em decorrência da paralisação."
        res_desconto = analyze_decision_content(text_desconto)
        self.assertEqual(res_desconto['dias_parados'], "Desconto Integral dos Dias Parados")

        text_comp = "Acordam os Ministros em autorizar a compensação de horas e dias parados mediante acordo entre as partes."
        res_comp = analyze_decision_content(text_comp)
        self.assertEqual(res_comp['dias_parados'], "Compensação de Horas/Dias")

    def test_analyze_decision_desfecho(self):
        text_acordo = "Homologa-se o acordo coletivo firmado entre a empresa pública e a federação sindical para todos os efeitos."
        res_acordo = analyze_decision_content(text_acordo)
        self.assertEqual(res_acordo['desfecho'], "Homologação de Acordo")

        text_ext = "Acolhe-se a preliminar patronal para extinguir o processo sem resolução do mérito com base no artigo 485 do CPC."
        res_ext = analyze_decision_content(text_ext)
        self.assertEqual(res_ext['desfecho'], "Extinção sem Resolução do Mérito")

    def test_pipeline_execution_and_files(self):
        df_summary, df_cases = build_sdc_ministers_profile()
        self.assertGreater(len(df_cases), 500, "Deveria haver mais de 500 casos de estatais analisados na SDC")
        self.assertGreater(len(df_summary), 5, "Deveria haver pelo menos 5 ministros relatores agregados")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "perfil_ministros_sdc_tst.xlsx")
        json_path = os.path.join(base_dir, "perfil_ministros_sdc_tst.json")
        
        self.assertTrue(os.path.exists(excel_path), f"Arquivo {excel_path} não foi gerado")
        self.assertTrue(os.path.exists(json_path), f"Arquivo {json_path} não foi gerado")
        
        # Verify columns in summary
        required_cols = [
            "Ministro(a) Relator(a)", "Total Julgamentos Estatais",
            "Taxa de Abusividade (%)", "Taxa de Aplicação de Desconto (%)",
            "Perfil / Tendência Decisória"
        ]
        for col in required_cols:
            self.assertIn(col, df_summary.columns)

if __name__ == '__main__':
    unittest.main()
