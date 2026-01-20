DOMAIN = "precio_combustible_ar"

ID_RECURSO = "80ac25de-a44a-4445-9215-090cf55cfda5"
URL_API_BUSQUEDA = f"https://datos.energia.gob.ar/api/3/action/resource_show?id={ID_RECURSO}"

URL_ARCHIVO = "https://datos.energia.gob.ar/dataset/c846e793-24d1-4db9-957c-8909e14cfef2/resource/80ac2599-eeed-4990-ba7e-39918cf30948/download/precios-en-surtidor-resolucin-3142016.csv"

URL_OFICIAL = URL_ARCHIVO

PRODUCTOS = {
    "2": "Nafta Súper",
    "3": "Nafta Premium",
    "19": "Gasoil Grado 2",
    "21": "Gasoil Grado 3",
    "28": "GNC"
}
