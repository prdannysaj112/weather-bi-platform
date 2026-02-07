from statistics import mean

def simple_sales_forecast(sales_rows):
    """
    Very simple baseline forecast: average of recent sales.
    (College-level + explainable. You can later upgrade to regression.)
    """
    if not sales_rows:
        return {"forecast": None, "method": "avg_recent", "note": "No sales data"}
    vals = [r[1] for r in sales_rows]  # (date, sales)
    return {"forecast": round(mean(vals), 2), "method": "avg_recent", "n": len(vals)}
