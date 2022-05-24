from environs import Env


env = Env()
env.read_env()

# 代理 API
IP3366 = env.str('IP3366')
QING_TING = env.str('QING_TING')
DAI_LI_CLOUD = env.str('DAI_LI_CLOUD')
SELF_PROXY_URL = env.str('SELF_PROXY_URL')
PA_DAI_LI_PROXY_URL = env.str('PADAILI_PROXY_URL')

# 对于获取到的代理是否需要测试
PROXY_TEST = True
PROXY_TEST_URL = 'https://www.baidu.com'

# cookie
JOB51_COOKIE = env.str('JOB51_COOKIE')
