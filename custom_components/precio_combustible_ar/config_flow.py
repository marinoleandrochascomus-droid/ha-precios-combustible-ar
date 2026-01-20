import voluptuous as vol
import csv
import os
import logging
import aiohttp
import asyncio
from datetime import datetime
from homeassistant import config_entries
from .const import DOMAIN, URL_API_BUSQUEDA, PRODUCTOS

_LOGGER = logging.getLogger(__name__)

PROVINCIAS_MAP = {
    "CAPITAL FEDERAL": "CABA",
    "BUENOS AIRES": "BUENOS AIRES",
    "CATAMARCA": "CATAMARCA",
    "CHACO": "CHACO",
    "CHUBUT": "CHUBUT",
    "CORDOBA": "CORDOBA",
    "CORRIENTES": "CORRIENTES",
    "ENTRE RIOS": "ENTRE RIOS",
    "FORMOSA": "FORMOSA",
    "JUJUY": "JUJUY",
    "LA PAMPA": "LA PAMPA",
    "LA RIOJA": "LA RIOJA",
    "MENDOZA": "MENDOZA",
    "MISIONES": "MISIONES",
    "NEUQUEN": "NEUQUEN",
    "RIO NEGRO": "RIO NEGRO",
    "SALTA": "SALTA",
    "SAN JUAN": "SAN JUAN",
    "SAN LUIS": "SAN LUIS",
    "SANTA CRUZ": "SANTA CRUZ",
    "SANTA FE": "SANTA FE",
    "SANTIAGO DEL ESTERO": "SANTIAGO DEL ESTERO",
    "TIERRA DEL FUEGO": "TIERRA DEL FUEGO",
    "TUCUMAN": "TUCUMAN"
}

class PrecioCombustibleFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración con saltos lógicos."""
    VERSION = 1

    def __init__(self):
        self.data = {}
        self.archivo_path = None

    async def _obtener_y_descargar_csv(self):
        """Descarga el CSV si no existe o es viejo."""
        self.archivo_path = self.hass.config.path(f"custom_components/{DOMAIN}/precios.csv")
        if os.path.exists(self.archivo_path):
            mtime = os.path.getmtime(self.archivo_path)
            if (datetime.now().timestamp() - mtime) < 86400:
                return True
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL_API_BUSQUEDA, timeout=10) as response:
                    res = await response.json()
                    url_csv = res.get("result", {}).get("url")
                if url_csv:
                    async with session.get(url_csv, timeout=15) as csv_res:
                        content = await csv_res.read()
                        with open(self.archivo_path, "wb") as f:
                            f.write(content)
                        return True
        except Exception as e:
            _LOGGER.error("Error descarga: %s", e)
        return os.path.exists(self.archivo_path)

    def _get_localidades(self, provincia_seleccionada):
        """Busca localidades únicas."""
        localidades = set()
        try:
            with open(self.archivo_path, mode='r', encoding='utf-8', errors='ignore') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('provincia', '').strip().upper() == provincia_seleccionada:
                        loc = row.get('localidad', '').strip().upper()
                        if loc:
                            localidades.add(loc)
        except Exception as e:
            _LOGGER.error("Error al procesar localidades: %s", e)
        return sorted(list(localidades))

    async def async_step_user(self, user_input=None):
        """Paso 1: Provincia y Producto."""
        await self._obtener_y_descargar_csv()

        if user_input is not None:
            self.data.update(user_input)
            if self.data["provincia"] == "CAPITAL FEDERAL":
                self.data["localidad"] = "CAPITAL FEDERAL"
                return self._crear_entrada()
            lista = await self.hass.async_add_executor_job(
                self._get_localidades, self.data["provincia"]
            )
            if not lista:
                self.data["localidad"] = self.data["provincia"] # Fallback
                return self._crear_entrada()
            return await self.async_step_localidad()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("provincia"): vol.In(PROVINCIAS_MAP),
                vol.Required("idproducto"): vol.In(PRODUCTOS),
            })
        )

    async def async_step_localidad(self, user_input=None):
        """Paso 2: Selección de Localidad."""
        lista_localidades = await self.hass.async_add_executor_job(
            self._get_localidades, self.data["provincia"]
        )

        if user_input is not None:
            self.data.update(user_input)
            return self._crear_entrada()

        return self.async_show_form(
            step_id="localidad",
            data_schema=vol.Schema({
                vol.Required("localidad"): vol.In(lista_localidades)
            })
        )

    def _crear_entrada(self):
        """Finaliza la configuración."""
        nombre_prod = PRODUCTOS.get(self.data["idproducto"], "Combustible")
        return self.async_create_entry(
            title=f"{nombre_prod}: {self.data['localidad']}",
            data=self.data
        )
