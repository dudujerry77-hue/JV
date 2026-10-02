"""Cost tracking + ceiling enforcement -- see .jarvis/decisions.md D-0008,
D-0016 and .jarvis/ai_provider_spec.md "Cost Transparency Requirement".

Cost-per-token figures live in config (D-0016), not here, and are an
estimate the owner configures -- this module does not claim to reproduce
a provider's exact billing, only to give the router something concrete to
enforce a ceiling against and the owner something to see in /status.
"""

import sqlite3
from datetime import UTC, datetime


class CostTracker:
    def __init__(self, conn: sqlite3.Connection, monthly_ceiling_usd: float):
        """`conn` must already have the `ai_usage` table (see
        jarvis_core/storage/db.py's SCHEMA) -- this class does not create
        its own tables, consistent with storage/db.py owning all schema.
        """
        self._conn = conn
        self.monthly_ceiling_usd = monthly_ceiling_usd

    def spent_this_month(self) -> float:
        month_prefix = datetime.now(UTC).strftime("%Y-%m")
        row = self._conn.execute(
            "SELECT COALESCE(SUM(estimated_cost_usd), 0) AS total FROM ai_usage "
            "WHERE timestamp LIKE ?",
            (f"{month_prefix}%",),
        ).fetchone()
        return float(row["total"])

    def would_exceed_ceiling(self, additional_estimated_cost_usd: float) -> bool:
        return self.spent_this_month() + additional_estimated_cost_usd > self.monthly_ceiling_usd

    def record_usage(
        self,
        *,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        estimated_cost_usd: float,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO ai_usage
                (timestamp, provider, model, input_tokens, output_tokens, estimated_cost_usd)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(UTC).isoformat(),
                provider,
                model,
                input_tokens,
                output_tokens,
                estimated_cost_usd,
            ),
        )
        self._conn.commit()
