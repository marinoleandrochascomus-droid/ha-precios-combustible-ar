import logging
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if not coordinator.data:
        return

    entities = [
        CombustibleArgentinoSensor(coordinator, key, entry.entry_id)
        for key in coordinator.data
    ]
    async_add_entities(entities)

class CombustibleArgentinoSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, entry_id):
        super().__init__(coordinator)
        self._key = key
        self._entry_id = entry_id

    @property
    def name(self):
        data = self.coordinator.data[self._key]
        return f"{data['empresa']} - {data['direccion']}"

    @property
    def unique_id(self):
        return f"{self._entry_id}_{self._key}"

    @property
    def native_unit_of_measurement(self):
        return "ARS"

    @property
    def device_class(self):
        return "monetary"

    @property
    def state_class(self):
        return SensorStateClass.TOTAL

    @property
    def entity_picture(self):
        empresa = self.coordinator.data[self._key]["empresa"].upper()
        if "YPF" in empresa: return "https://upload.wikimedia.org/wikipedia/commons/c/cd/YPF.svg"
        if "SHELL" in empresa: return "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Shell_logo_1948.png/512px-Shell_logo_1948.png"
        if "AXION" in empresa: return "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Logo_AXION_energy.jpg/512px-Logo_AXION_energy.jpg"
        if "PUMA" in empresa: return "https://upload.wikimedia.org/wikipedia/commons/b/ba/Puma_Energy_logo.svg"
        if "GULF" in empresa: return "https://upload.wikimedia.org/wikipedia/commons/7/72/Gulf_Oil_logo.svg"
        return None

    @property
    def icon(self):
        return None if self.entity_picture else "mdi:gas-station"

    @property
    def native_value(self):
        data = self.coordinator.data[self._key]
        if data.get("es_viejo"):
            return None
        return data["precio"]

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data[self._key]
        estado = data["estado_del_dato"]
        estado_visual = "✅ AL DÍA" if estado == "AL DÍA" else "⚠️ DESACTUALIZADO"
        return {
            "empresa": data["empresa"],
            "direccion": data["direccion"],
            "localidad": data["localidad"],
            "provincia": data.get("provincia"),
            "producto": data["producto"],
            "ultima_modificacion_oficial": data["ultima_modificacion"],
            "estado_del_dato": estado_visual
        }
