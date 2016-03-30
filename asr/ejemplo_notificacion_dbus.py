#!/usr/bin/env python
 
import dbus
 
# Inicializando el bus de tipo session (se comunica entre aplicaciones)
bus = dbus.SessionBus()
 
# Se obtiene el objeto Notifications (es el encargado de las notificaciones)
notify_object = bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
 
# Se obtiene una interface del tipo Notificatios
notify_interface = dbus.Interface(notify_object,'org.freedesktop.Notifications')
 
# Finalmente lanzamos la notificacion
# Nota: el gtk-ok muestra un icono de ok en el mensaje, puede ser cualquier otro
# como gtk-cut (muestra una tijera), gtk-connect (una conexion), etc.
notify_id = notify_interface.Notify("DBus Test", 0, "gtk-ok", "Hola a todos",'Un ejemplo de mensaje o texto a mostrar', "",{},10000)

notify_id = notify_interface.Notify("DBus Test", 0, "gtk.STOCK_DIALOG_QUESTION", "Hola a todos",'mensaje o texto a mostrar ?', "",{},10000)
 
# Imprimimos el ID de esta notificacion
print "El ID de la notificacion es: ", notify_id
