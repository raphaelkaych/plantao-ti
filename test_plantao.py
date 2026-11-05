import unittest
from contextlib import closing

from plantao import abrir_banco, abrir_incidente, listar, resolver, status


class PlantaoTest(unittest.TestCase):
    def test_fila_prioriza_prazo_e_separa_resolvidos(self):
        with closing(abrir_banco(":memory:")) as banco:
            menor = abrir_incidente(banco, "Acesso ao relatório", "P3", 100)
            urgente = abrir_incidente(banco, "ERP indisponível", "P1", 150)
            self.assertEqual([r["id"] for r in listar(banco)], [urgente, menor])
            resolver(banco, urgente, 3750)
            self.assertEqual([r["id"] for r in listar(banco)], [menor])
            self.assertEqual(status(listar(banco, True)[1], 4000), "resolvido no prazo")
            with self.assertRaises(ValueError):
                resolver(banco, urgente, 4000)

    def test_atraso_no_limite_do_sla(self):
        with closing(abrir_banco(":memory:")) as banco:
            incidente = abrir_incidente(banco, "Fila indisponível", "P1", 100)
            registro = listar(banco)[0]
            self.assertEqual(status(registro, 3700), "em aberto")
            self.assertEqual(status(registro, 3701), "em atraso")
            resolver(banco, incidente, 3701)
            self.assertEqual(status(listar(banco, True)[0], 4000), "resolvido com atraso")


if __name__ == "__main__":
    unittest.main()
