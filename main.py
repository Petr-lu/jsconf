from jsconf import Config


conf_server = Config('Server', './Config/', dict(ip='localhost', port=4040))
conf_server.save_config_hash()
print(conf_server.loading_config_hash())