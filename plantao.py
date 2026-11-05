import argparse
import sqlite3
from contextlib import closing
from datetime import datetime, timezone


# Prazos de resolução em minutos corridos neste laboratório.
PRAZOS = {"P1": 60, "P2": 240, "P3": 1440}


def abrir_banco(caminho):
    banco = sqlite3.connect(caminho)
    banco.row_factory = sqlite3.Row
    banco.execute("""
        CREATE TABLE IF NOT EXISTS incidente (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            prioridade TEXT NOT NULL CHECK (prioridade IN ('P1', 'P2', 'P3')),
            aberto_em INTEGER NOT NULL,
            prazo_em INTEGER NOT NULL,
            resolvido_em INTEGER
        )
    """)
    return banco


def abrir_incidente(banco, titulo, prioridade, agora):
    titulo = titulo.strip()
    if not titulo or not titulo.isprintable():
        raise ValueError("Informe um título em uma única linha.")
    prazo = agora + PRAZOS[prioridade] * 60
    with banco:
        registro = banco.execute(
            "INSERT INTO incidente (titulo, prioridade, aberto_em, prazo_em) VALUES (?, ?, ?, ?)",
            (titulo, prioridade, agora, prazo),
        )
    return registro.lastrowid


def resolver(banco, identificador, agora):
    with banco:
        atualizacao = banco.execute(
            """UPDATE incidente SET resolvido_em = ?
               WHERE id = ? AND resolvido_em IS NULL AND aberto_em <= ?""",
            (agora, identificador, agora),
        )
        if atualizacao.rowcount == 0:
            raise ValueError("Incidente inexistente, já resolvido ou aberto no futuro.")


def status(registro, agora):
    resolvido = registro["resolvido_em"]
    prazo = registro["prazo_em"]
    if resolvido is not None:
        return "resolvido no prazo" if resolvido <= prazo else "resolvido com atraso"
    return "em atraso" if agora > prazo else "em aberto"


def listar(banco, incluir_resolvidos=False):
    return banco.execute(
        """SELECT * FROM incidente WHERE resolvido_em IS NULL OR ?
           ORDER BY resolvido_em IS NOT NULL, prazo_em, prioridade, id""",
        (incluir_resolvidos,),
    ).fetchall()


def main():
    parser = argparse.ArgumentParser(description="Fila local de incidentes com prazo de resolução.")
    parser.add_argument("--banco", default="plantao.sqlite3")
    comandos = parser.add_subparsers(dest="comando", required=True)
    abertura = comandos.add_parser("abrir")
    abertura.add_argument("prioridade", choices=PRAZOS)
    abertura.add_argument("titulo")
    fila = comandos.add_parser("fila")
    fila.add_argument("--todos", action="store_true")
    encerramento = comandos.add_parser("resolver")
    encerramento.add_argument("id", type=int)
    args = parser.parse_args()

    agora = int(datetime.now(timezone.utc).timestamp())
    try:
        with closing(abrir_banco(args.banco)) as banco:
            if args.comando == "abrir":
                print(f"Incidente #{abrir_incidente(banco, args.titulo, args.prioridade, agora)} aberto.")
            elif args.comando == "resolver":
                resolver(banco, args.id, agora)
                print(f"Incidente #{args.id} resolvido.")
            else:
                registros = listar(banco, args.todos)
                if not registros:
                    print("Nenhum incidente nesta fila.")
                for registro in registros:
                    prazo = datetime.fromtimestamp(registro["prazo_em"], timezone.utc)
                    print(f"#{registro['id']}  {registro['prioridade']}  {registro['titulo']}"
                          f" | {status(registro, agora)} | até {prazo:%d/%m %H:%M} UTC")
    except (ValueError, sqlite3.Error) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
