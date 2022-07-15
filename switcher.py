import os

admin_enabled_status = ['ENABLED', 'enabled', 'Enabled', u'已启用']
admin_disabled_status = ['DISABLED', 'disabled', 'Disabled', u'已禁用']

connected_status = ['CONNECTED', 'connected', 'Connected', u'已连接']
disconnected_status = ['DISCONNECTED', 'disconnected', 'Disconnected', u'已断开连接']

class Switcher():
    def __init__(self) -> None:
        self.net_info = {}
        self.get_net()
        self.interfaces = list(self.net_info.keys())
        self.pairs = self.interfaces[:2]

    def get_net(self):
        cmd = 'netsh interface show interface'  # 查看本地存在的网卡
        tmp = os.popen(cmd)
        net = tmp.read().strip().split('\n')
        
        for n in net[2:]:
            info = n.split()
            self.net_info[info[-1]] = {
                'isEnabled': info[0],
                'isConnected': info[1],
            }

    # 切换网络状态，pairs为需要对调的网卡
    # TODO: 设定自动连接的目标wifi
    def switch(self):  
        self.get_net()
        history = []
        for i in range(2):
            interface_name = self.pairs[i]
            status = self.net_info[interface_name]['isEnabled']
            history.append(status)
            # 若该接口当前状态为启用，则将其禁用，否则禁用
            status = 'DISABLED' if status in admin_enabled_status else 'ENABLED'
            cmd = f'netsh interface set interface name="{interface_name}" admin={status}'
            os.system(cmd)
        
        # 检查是否切换
        self.get_net()
        error = []
        for i in range(2):    
            status = self.net_info[self.pairs[i]]['isEnabled']
            if history[i] == status:
                error.append(self.pairs[i])
        
        if len(error) > 0:
            print(' '.join(error), 'switch failed with unknown error.')
            return 1
        else:
            return 0

    def update_pairs(self, pairs):
        assert len(self.pairs) == len(pairs)
        self.pairs = pairs

    def display_password(self,):
        #TODO 显示wifi密码 # https://www.cnblogs.com/hiwangzi/p/7475121.html
        # :: 查看特定
        # netsh wlan show profile 配置名称 key=clear

        # :: 查看所有
        # for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do  @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
        pass