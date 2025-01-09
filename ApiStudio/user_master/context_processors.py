from .models import UserProfile, AppPermission, AppPermissionGroup, StudioMenus


def studio_menus_processor(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # studio_menus = user_profile.studio_menus.all()
            studio_menus = user_profile.studio_menus.filter(active=True).order_by('menu_order')
        except UserProfile.DoesNotExist:
            studio_menus = StudioMenus.objects.filter(active=True).order_by('menu_order')
    else:
        studio_menus = []
    # print(studio_menus)
    return {'studio_menus': studio_menus}
