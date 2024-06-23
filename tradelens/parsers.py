from abc import ABC, abstractmethod
from enum import StrEnum

import polars as pl

from tradelens.models import TradeLog


class TradeLogParserType(StrEnum):
    KIWOOM_HTS_CLIPBOARD = "kiwoom_hts_clipboard"


class TradeLogParser(ABC):
    @abstractmethod
    def parse(self) -> list[TradeLog]:
        pass


class KiwoomHtsClipboardTradeLogParser(TradeLogParser):
    def parse(self) -> list[TradeLog]:
        """클립보드에서 키움 HTS 거래내역 데이터를 읽어 TradeLog 객체로 변환합니다.
        화면번호 1691의 일별 매매내역 데이터 화면에서 복사한 데이터를 붙여넣어 사용합니다.

        Returns:
            list[TradeLog]: _description_
        """

        def _preprocess(column: pl.Expr) -> pl.Expr:
            return pl.when(column != "").then(column.str.replace_all(r"'|,|%", "")).otherwise(None)

        try:
            # 클립보드에서 데이터 읽기
            df = pl.read_clipboard(separator="\t", skip_rows=1)

            # 명시적으로 컬럼 이름 지정
            df.columns = [
                "내역",
                "거래일",
                "종목코드",
                "종목명",
                "매수평균가",
                "매수수량",
                "매수금액",
                "매수메모",
                "매도평균가",
                "매도수량",
                "매도금액",
                "매도메모",
                "수수료+제세금",
                "손익금액",
                "수익률",
                "정산금액",
            ]

            df = df.select([
                pl.col("거래일").str.to_datetime("%Y/%m/%d"),
                _preprocess(pl.col("종목코드")).cast(pl.Utf8),
                pl.col("종목명"),
                _preprocess(pl.col("매수평균가")).cast(pl.Float64),
                _preprocess(pl.col("매수수량")).cast(pl.Int64),
                _preprocess(pl.col("매수금액")).cast(pl.Float64),
                _preprocess(pl.col("매도평균가")).cast(pl.Float64),
                _preprocess(pl.col("매도수량")).cast(pl.Int64),
                _preprocess(pl.col("매도금액")).cast(pl.Float64),
                _preprocess(pl.col("수수료+제세금")).cast(pl.Float64),
                _preprocess(pl.col("손익금액")).cast(pl.Float64),
                _preprocess(pl.col("수익률")).cast(pl.Float64).alias("수익률(%)"),
            ])

            trade_logs = []
            for row in df.iter_rows(named=True):
                if row["매수평균가"]:  # 매수 데이터가 있을 경우
                    trade_log = TradeLog(
                        date=row["거래일"],
                        symbol=row["종목코드"],
                        label=row["종목명"],
                        side="매수",
                        quantity=row["매수수량"],
                        price=row["매수평균가"],
                        amount=row["매수금액"],
                        transaction_costs=row["수수료+제세금"],
                        pnl=row["손익금액"],
                        return_pct=row["수익률(%)"],
                    )
                    trade_logs.append(trade_log)

                if row["매도평균가"]:  # 매도 데이터가 있을 경우
                    trade_log = TradeLog(
                        date=row["거래일"],
                        symbol=row["종목코드"],
                        label=row["종목명"],
                        side="매도",
                        quantity=row["매도수량"],
                        price=row["매도평균가"],
                        amount=row["매도금액"],
                        transaction_costs=row["수수료+제세금"],
                        pnl=row["손익금액"],
                        return_pct=row["수익률(%)"],
                    )
                    trade_logs.append(trade_log)

            return trade_logs
        except Exception as e:
            raise RuntimeError(f"Error parsing trade log data: {e}") from e


class TradeLogParserFactory:
    @staticmethod
    def create_parser(parser_type: str) -> TradeLogParser:
        if parser_type == TradeLogParserType.KIWOOM_HTS_CLIPBOARD:
            return KiwoomHtsClipboardTradeLogParser()
        else:
            raise ValueError(f"Unknown parser type: {parser_type}")
