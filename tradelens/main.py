import os

import typer
from jinja2 import Template

from tradelens.models import TradeLog
from tradelens.parsers import TradeLogParserFactory, TradeLogParserType
from tradelens.utils import load_template

app = typer.Typer()


def write_journal(trade_log: TradeLog, template: Template, output_dir: str) -> None:
    try:
        note_content = template.render(
            date=trade_log.date,
            label=trade_log.label,
            symbol=trade_log.symbol,
            side=trade_log.side,
            quantity=trade_log.quantity,
            price=trade_log.price,
            amount=trade_log.amount,
            transaction_costs=trade_log.transaction_costs,
            pnl=trade_log.pnl,
            return_pct=trade_log.return_pct,
        )

        filename = os.path.join(
            output_dir, f"{trade_log.date.strftime("%Y-%m-%d")}_{trade_log.label}.md"
        )
        with open(filename, "w", encoding="utf-8") as file:
            file.write(note_content)
    except Exception as e:
        typer.secho(
            f"Error creating note for {trade_log.symbol} on {trade_log.date}: {e}",
            fg=typer.colors.RED,
        )


@app.command()
def generate_notes(
    output_dir: str = "notes", template_path: str = "tradelens/templates/journal_template.md"
) -> None:
    """
    Generate Obsidian notes from clipboard data.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 템플릿 로드
        template = load_template(template_path)

        # 파서 인스턴스 생성
        parser = TradeLogParserFactory.create_parser(TradeLogParserType.KIWOOM_HTS_CLIPBOARD)
        trade_logs = parser.parse()

        # 각 row에 대해 노트를 생성
        for trade_log in trade_logs:
            write_journal(trade_log, template, output_dir)

        typer.secho("Notes generated successfully!", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f"Error reading clipboard data or generating notes:\n{e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
