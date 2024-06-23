# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user # type: ignore

def getAllImages(input=None):
    # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
    # el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.
    json_collection = []

    #Obtiene un listado de imagenes desde transport.py
    json_collection=transport.getAllImages(input)

    # recorre el listado de objetos JSON, lo transforma en una NASACard y lo agrega en el listado de images.
    images = []
    
    for objetos in json_collection: #Recorro la lista json_collection.
        nasa_card=mapper.fromRequestIntoNASACard(objetos)
        images.append(nasa_card) #Agrega los objetos (pasados a nasacard) a la lista imagenes.
    return images

def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = mapper.fromTemplateIntoNASACard(request) # transformamos un request del template en una NASACard.
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated: #si no loguea
        return [] #no devuelve favoritos (debido a que no tiene cuenta)
    else:
        
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositorio TODOS los favoritos del usuario (variable 'user').
        favourite_list=repositories.getAllFavouritesByUser(user)
        mapped_favourites = []

        for favourite in favourite_list:
            nasa_card = mapper.fromRepositoryIntoNASACard(favourite) # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.