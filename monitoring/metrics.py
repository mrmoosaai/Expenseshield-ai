"""Simple metrics tracking for the expense agent."""

from datetime import datetime
from typing import Dict, Any


class MetricsTracker:
    """Tracks request and decision metrics for the agent workflow."""

    def __init__(self):
        self.total_requests = 0
        self.auto_approvals = 0
        self.llm_reviews = 0
        self.human_reviews = 0
        self.security_blocks = 0
        self.errors = 0
        self.start_time = datetime.now()

    def increment(self, metric_name: str):
        """Increment a named metric if it exists."""
        if hasattr(self, metric_name):
            current_value = getattr(self, metric_name)
            setattr(self, metric_name, current_value + 1)

    def record_request(self):
        """Record a newly processed request."""
        self.total_requests += 1

    def record_auto_approval(self):
        """Record an auto-approval decision."""
        self.auto_approvals += 1

    def record_llm_review(self):
        """Record a decision that required LLM review."""
        self.llm_reviews += 1

    def record_human_review(self):
        """Record a decision that required human review."""
        self.human_reviews += 1

    def record_security_block(self):
        """Record a blocked event due to security concerns."""
        self.security_blocks += 1

    def record_error(self):
        """Record an error encountered during processing."""
        self.errors += 1

    def get_stats(self) -> Dict[str, Any]:
        """Return current system metrics and rates."""
        uptime = datetime.now() - self.start_time

        return {
            "total_requests": self.total_requests,
            "auto_approvals": self.auto_approvals,
            "llm_reviews": self.llm_reviews,
            "human_reviews": self.human_reviews,
            "security_blocks": self.security_blocks,
            "errors": self.errors,
            "uptime_seconds": uptime.total_seconds(),
            "auto_approval_rate": (
                self.auto_approvals / self.total_requests
                if self.total_requests > 0 else 0
            ),
            "error_rate": (
                self.errors / self.total_requests
                if self.total_requests > 0 else 0
            ),
        }

    def print_stats(self):
        """Print the current metrics to the console."""
        stats = self.get_stats()

        print("\n" + "=" * 50)
        print("📊 AGENT METRICS")
        print("=" * 50)
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Auto-Approvals: {stats['auto_approvals']}")
        print(f"LLM Reviews: {stats['llm_reviews']}")
        print(f"Human Reviews: {stats['human_reviews']}")
        print(f"Security Blocks: {stats['security_blocks']}")
        print(f"Errors: {stats['errors']}")
        print(f"Uptime: {stats['uptime_seconds']:.2f} seconds")
        print(f"Auto-Approval Rate: {stats['auto_approval_rate']:.2%}")
        print(f"Error Rate: {stats['error_rate']:.2%}")
        print("=" * 50 + "\n")


metrics = MetricsTracker()
