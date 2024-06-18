# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render 
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout 


# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = []
    images=services_nasa_image_gallery.getAllImages() #lista de toda las imagenes de la API
    favourite_list = []
    favourite_list=services_nasa_image_gallery.getAllFavouritesByUser(request) #listado de los fav del usuario

    return images, favourite_list

# función principal de la galería.

def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    favourite_list = []
    images,favourite_list=getAllImagesAndFavouriteList(request) #retorno de las dos listas de la funcion anterior
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    
    images=[]
    favourite_list=[]
    search_msg = request.POST.get('query', '')
    if not search_msg: #Si no pone nada en el buscador
        images=services_nasa_image_gallery.getAllImages("space") #busca "space" por default
    else:
        images=services_nasa_image_gallery.getAllImages(search_msg) #busca lo que introdujo en search_msg
    
    
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    favourite_list=services_nasa_image_gallery.getAllFavouritesByUser(request) #lista de los favoritos del user
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    #Guarda el nuevo favorito en la lista
    services_nasa_image_gallery.saveFavourite(request)
    #Obtener la lista de favoritos actuales del usuario
    images,favourite_list=getAllImagesAndFavouriteList(request)
    #Renderiza la pagina home
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )
    


@login_required
def deleteFavourite(request):
    #Eliminar el favorito de la lista
    services_nasa_image_gallery.deleteFavourite(request)
    #Obtener la lista de favoritos actualizada del ususario
    favourite_list=services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})
    


@login_required
def exit(request):
    pass