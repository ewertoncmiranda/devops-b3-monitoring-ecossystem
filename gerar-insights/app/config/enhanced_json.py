import json
from decimal import Decimal


class EnhancedJSONEncoder(json.JSONEncoder):
    """Permite serializar Decimal, sets, numpy, etc."""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        try:
            import numpy as np
            if isinstance(obj, (np.float32, np.float64, np.int32, np.int64)):
                return obj.item()
        except ImportError:
            pass

        return super().default(obj)
