import io
import csv
import os
import logging
from datetime import datetime, timedelta
import aiohttp
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, URL_API_BUSQUEDA, PRODUCTOS

_LOGGER = logging.getLogger(__name__)

class PrecioCombustibleCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )
        self.entry = entry
        self.provincia_config = str(entry.data.get("provincia", "")).strip().upper()
        self.localidad_config = str(entry.data.get("localidad", "")).strip().upper()
        self.producto_config = str(entry.data.get("idproducto", "")).strip()

    def _save_and_process(self, content):
        path_local = self.hass.config.path(f"custom_components/{DOMAIN}/precios.csv")
        try:
            with open(path_local, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            _LOGGER.error(f"Error guardando backup CSV: {e}")

        result = {}
        reader = csv.DictReader(io.StringIO(content))
        ahora = datetime.now()

        for row in reader:
            if str(row.get("idtipohorario")) != "2":
                continue
            prov_csv = str(row.get("provincia", "")).strip().upper()
            loc_csv = str(row.get("localidad", "")).strip().upper()
            if prov_csv != self.provincia_config or loc_csv != self.localidad_config:
                continue
            prod_id = str(row.get("idproducto", "")).strip()
            if prod_id != self.producto_config:
                continue

            fecha_str = row.get("fecha_vigencia", "")
            es_viejo = False
            estado_texto = "AL DÍA"
            try:
                fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                if (ahora - fecha_dt).days > 30:
                    es_viejo = True
                    estado_texto = "DESACTUALIZADO"
            except Exception:
                estado_texto = "SIN DATOS"

            id_estacion = row.get("idempresa", "unknown")
            key = f"st_{id_estacion}_{prod_id}"

            result[key] = {
                "empresa": row.get("empresabandera", "OTRAS").strip().upper(),
                "producto": PRODUCTOS.get(prod_id, "Desconocido"),
                "precio": float(row.get("precio", 0)),
                "direccion": row.get("direccion", "").strip().upper(),
                "localidad": loc_csv,
                "provincia": prov_csv,
                "estado_del_dato": estado_texto,
                "ultima_modificacion": fecha_str,
                "es_viejo": es_viejo
            }
        return result

    async def _async_update_data(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with async_timeout.timeout(120):
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(URL_API_BUSQUEDA, ssl=False) as resp:
                        api_data = await resp.json()
                        url_csv = api_data["result"]["url"]
                    async with session.get(url_csv, ssl=False) as response:
                        content = await response.text()
                        return await self.hass.async_add_executor_job(self._save_and_process, content)
        except Exception as err:
            raise UpdateFailed(f"Error: {err}")
