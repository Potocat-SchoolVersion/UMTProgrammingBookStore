# model/discount.py

class Discount:
    """Voucher-based discount calculation"""

    VOUCHERS = {
        "FIRSTTIMEBUY": 0.05,
        "RAYA": 0.07,
        "CNY": 0.07,
        "DEPAVALI": 0.07
    }

    @staticmethod
    def get_discount_rate(voucher: str | None) -> float:
        """
        Return discount rate for a voucher code.
        Unknown or empty vouchers return 0.0
        """
        if not voucher:
            return 0.0

        return Discount.VOUCHERS.get(voucher.upper(), 0.0)

    @staticmethod
    def get_discount_text(voucher: str | None) -> str:
        """
        Return human-readable voucher description.
        """
        if not voucher:
            return "No voucher applied"

        rate = Discount.VOUCHERS.get(voucher.upper())

        if rate is None:
            return "Invalid voucher"

        return f"{voucher} ({int(rate * 100)}% OFF)"
