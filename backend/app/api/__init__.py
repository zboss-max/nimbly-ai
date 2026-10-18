"""
版本控制
"""
def get_registry():
    from app.api.v1 import register_routes as register_v1
    return {
        "v1": register_v1,
    }