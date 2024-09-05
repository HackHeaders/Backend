from django.contrib import admin
from core.authUser.models import Address, User, Client, ClientPhysicalPerson, ClientLegalPerson, Driver, Employe, DataEmploye, Offices

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Client)
admin.site.register(ClientPhysicalPerson)
admin.site.register(ClientLegalPerson)
admin.site.register(Driver)
admin.site.register(Employe)
admin.site.register(DataEmploye)
admin.site.register(Offices)