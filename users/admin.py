from django.contrib import admin
from .models import participants,reservation
# Register your models here.
class Reservation_Tag(admin.TabularInline):
    model=reservation
    extra=4
    can_delete=True
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cin', 'email', 'first_name', 'last_name', 'username','created_at','update_at')

    list_filter = ('cin','username','last_name',)
    search_fields = ('cin', 'first_name','last_name','username')
    autocomplete_fields = ('reservations',)
    list_per_page = 2
    readonly_fields = ('created_at', 'update_at')
    exclude = ('created_at', 'update_at',) 
    fieldsets = (
        ('Login_Information', {
            'fields': ('username', 'email'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'cin'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'update_at'),
        }),
    )
    inlines = [Reservation_Tag]
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        print(queryset)
        return queryset.order_by('-is_superuser', 'username')
    

class ReservationAdmin(admin.ModelAdmin):
    list_display=['conference','participant','confirmed','reservation_date']
    actions=['confirmede','unconfirmed']
    def confirmede(self,request,queryset):
        queryset.update(confirmed=True)
        self.message_user(request,"les reservations sont confirmé")
    
    confirmede.short_description = 'Reservation a confirmer'
    def unconfirmed(self,request,queryset):
        queryset.update(confirmed=False)
        self.message_user(request,"les reservations sont non confirmé")
    
    unconfirmed.short_description = 'Reservation a non confirmer'


admin.site.register(participants,ParticipantAdmin)
admin.site.register(reservation,ReservationAdmin) # type: ignore