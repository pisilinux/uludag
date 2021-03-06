site_config = {}

site_config['title'] = 'Pardus İyileştirme Listesi'
site_config['path'] = '/mnt/hdb8/uludag/depo/uludag/trunk/pardil/'
site_config['url'] = 'http://pardil/'
site_config['mail'] = 'pardil@uludag.org.tr'

site_config['db_host'] = 'localhost'
site_config['db_name'] = 'pardil_py'
site_config['db_user'] = 'pardil_py'
site_config['db_pass'] = ''

site_config['session_timeout'] = 1800
site_config['passcode_timeout'] = 1800
site_config['activation_timeout'] = 86400

site_config['pag_perpage'] = 25

site_config['safe_tags'] = {
                            'a': ['href'],
                            'strong': [],
                            'em': [],
                            'abbr': ['title']
                            }
