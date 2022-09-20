
from dataclasses import dataclass
from app.broker_abc import Broker
from app.mod_api_keys.entity import XYZEntity

@dataclass
class XYZService():
    broker: Broker
    entity: XYZEntity = None

    def get_single_entity_by_id(self, id: Any) -> XYZEntity:
        self.entity = self.broker.get_single_entity_by_id(id)
        return self.entity


    def set_single_entity(self, **kwargs) -> XYZEntity:
        self.entity = self.broker.set_single_entity(kwargs)
        return self.entity


    def delete_single_entity_by_key(self, key: str, value: Any) -> None:
        self.broker.delete_single_entity_by_key(key, value)


    def update_single_entity_by_key(self, key: str, value: Any, **kwargs) -> XYZEntity:
        self.entity = self.broker.update_single_entity_by_key(key, value, **kwargs)
        return self.entity