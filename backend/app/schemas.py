from pydantic import BaseModel


class PipelineResult(BaseModel):
    message: str
    rows_loaded: int


class Summary(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    average_order_value: float
