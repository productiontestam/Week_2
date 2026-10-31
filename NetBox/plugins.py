# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

# PLUGINS = ["netbox_bgp"]

# PLUGINS_CONFIG = {
#   "netbox_bgp": {
#     ADD YOUR SETTINGS HERE
#   }
# }
PLUGINS = [
    "netbox_topology_views",
    "netbox_reorder_rack",
    "netbox_diode_plugin",
]

PLUGINS_CONFIG = {
    "netbox_diode_plugin": {
        "diode_target": "grpc://192.168.1.102:8080/diode",
        "diode_target_override": "grpc://192.168.1.102:8080/diode",
        "diode_username": "diode",
    },
}
