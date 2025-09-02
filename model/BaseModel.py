from dataclasses import dataclass
@dataclass
class BaseModel(object):
    table_name: str = None
    def __init__(self, data):
        
        for col in self.columns():
            setattr(self, col, data.get(col))
    
    def columns(self):
        raise NotImplementedError
    
    def values(self):
        return tuple(getattr(self, col) for col in self.columns())
