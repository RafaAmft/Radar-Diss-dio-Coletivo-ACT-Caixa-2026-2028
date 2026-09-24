import unittest
import os
import sys
import json
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from turmas_behavior_analysis import classify_turma_decision, analyze_turmas_behavior

class TestTurmasBehavior(unittest.TestCase):

    def test_classify_turma_name(self):
        rec1 = {
            'numFormatado': 'AIRR - 100-20.2020.5.01.0001',
            'orgaoJudicante': {'descricao': '3ª Turma'},
            'nomRelator': 'Mauricio Godinho Delgado',
            'tipo': {'nome': 'Agravo de Instrumento'},
            'txtConteudoDecisao': 'licitude do desconto salarial decorrente dos dias parados em greve tema 435 STF'
        }
        res1 = classify_turma_decision(rec1)
        self.assertEqual(res1['turma'], '3ª Turma')
        self.assertEqual(res1['tema_central'], 'Desconto de Dias Parados')
        self.assertEqual(res1['desfecho_julgamento'], 'Desconto Válido / Mantido (Pró-Empregador)')

    def test_classify_turma_reintegracao(self):
        rec2 = {
            'numFormatado': 'RR - 200-30.2021.5.02.0002',
            'orgaoJudicante': {'descricao': '6ª Turma'},
            'nomRelator': 'Kátia Magalhães Arruda',
            'tipo': {'nome': 'Recurso de Revista'},
            'txtConteudoDecisao': 'nulidade da dispensa de trabalhador grevista e determinar a reintegração ao emprego'
        }
        res2 = classify_turma_decision(rec2)
        self.assertEqual(res2['turma'], '6ª Turma')
        self.assertEqual(res2['tema_central'], 'Estabilidade / Reintegração de Grevista')
        self.assertEqual(res2['desfecho_julgamento'], 'Reintegração Deferida / Dispensa Nula')

    def test_classify_sumula_126(self):
        rec3 = {
            'numFormatado': 'Ag-AIRR - 300-40.2022.5.03.0003',
            'orgaoJudicante': {'descricao': '4ª Turma'},
            'nomRelator': 'Ives Gandra Martins Filho',
            'tipo': {'nome': 'Agravo'},
            'txtConteudoDecisao': 'Incide o óbice da Súmula nº 126 do TST ante a necessidade de revolvimento do acervo fático'
        }
        res3 = classify_turma_decision(rec3)
        self.assertEqual(res3['incidencia_sumula_126'], 'Sim')

    def test_pipeline_execution_and_artifacts(self):
        df_summary, df_cases = analyze_turmas_behavior()
        self.assertGreater(len(df_cases), 50, "Deveria haver acórdãos de Turmas coletados")
        self.assertGreater(len(df_summary), 4, "Deveria haver pelo menos 4 das 8 turmas representadas")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "comportamento_turmas_tst.xlsx")
        json_path = os.path.join(base_dir, "comportamento_turmas_tst.json")
        
        self.assertTrue(os.path.exists(excel_path), f"Arquivo {excel_path} não encontrado")
        self.assertTrue(os.path.exists(json_path), f"Arquivo {json_path} não encontrado")
        
        # Verify columns
        required_cols = [
            "Turma do TST", "Total de Julgamentos Analisados",
            "Taxa Desconto Mantido / Pró-Empresa (%)",
            "Aplicação da Súmula 126 / Óbice Fático (%)",
            "Perfil Doutrinário e Tendência da Turma"
        ]
        for col in required_cols:
            self.assertIn(col, df_summary.columns)

if __name__ == '__main__':
    unittest.main()
