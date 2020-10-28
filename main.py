from jsconf import Config



conf_Server = Config('Server', './Config/', dict(ip='localhost'))
conf_Server.loading_config()