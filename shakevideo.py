import os
import random
import requests
import webview
from concurrent.futures import ThreadPoolExecutor
# from win32com.shell import shell, shellcon
# import win32con, win32event, win32process
from download import Download
import json
from home_girl import girl_home
import re
import time
import winreg
from urllib.parse import urlparse

# key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
#                      r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
# video_path = str(winreg.QueryValueEx(key, "Local AppData")[0]).replace('\\', '/') + '/Temp/'

play_url = []


def random_user():
    user1 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    user2 = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    user3 = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
    user4 = "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1"
    user5 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"
    user6 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
    user7 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    user8 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"
    user = [user1, user2, user3, user4, user5, user6, user7, user8]
    user = random.choice(user)
    header = {"user-agent": user,
              "x-requested-with": "XMLHttpRequest", }
    return header


class Douyin(object):
    """
    抖音用户类
    采集作品列表
    """

    def __init__(self, param: str, limit: int = 0):
        """
        初始化用户信息
        参数自动判断：ID/URL
        """
        self.limit = limit
        self.http = requests.Session()
        self.url = ''
        self.type = 'unknow'
        self.download_path = ''
        # ↑ 预定义属性，避免调用时未定义 ↑
        self.param = param.strip()
        self.sign = '5SNnmwAAhagN-UXmj.IaFOUjZ4'  # sign可以固定
        self.__get_type()  # 判断当前任务类型：链接/ID
        self.aria2 = Download()  # 初始化Aria2下载服务，先不指定目录了，在设置文件名的时候再加入目录
        self.has_more = True
        self.finish = False
        # 字典格式方便入库用id做key/取值/修改对应数据，但是表格都接收数组
        self.videosL = []  # 列表格式
        # self.videos = {}  #字典格式
        self.gids = {}  # gid和作品序号映射

    def __get_type(self):
        """
        判断当前任务类型
        链接/ID
        """
        print(self.param)
        if '://' in self.param:  # 链接
            if 'https://www.douyin.com/user/' in self.param:
                if '?relation=1' in self.param:
                    self.id = self.param.replace('https://www.douyin.com/user/', '').replace('?relation=1', '')
                else:
                    self.id = self.param.replace('https://www.douyin.com/user/', '')
                print(self.id)
            else:
                self.__url2redirect()
        else:  # ID
            self.id = self.param

    def __url2redirect(self):
        """
        取302跳转地址
        短连接转长链接
        """
        headers = {  # 以前作品需要解析去水印，要用到移动端UA，现在不用了
            'User-Agent':
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                'Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/89.0.4389.82 '
        }
        try:
            r = self.http.head(self.param, headers=headers, allow_redirects=False)
            self.url = r.headers['Location']
        except Exception as e:
            print(e)
            self.url = self.param

    def __url2id(self):
        try:
            self.id = urlparse(self.url).path.split('/')[3]
        except Exception as e:
            print(e)
            self.id = ''

    def __url2uid(self):
        try:
            headers = {
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
            }
            res = requests.get(self.url, headers=headers)
            print(res.url)
            s = re.findall(r'sec_uid=(.*?)&', res.url)
            if len(s) == 0:
                self.id = re.findall(r'did=(.*?)&', res.url)[0]
            else:
                self.id = s[0]
            print(self.id)
        except Exception as e:
            print(e)
            self.id = ''

    def get_sign(self):
        """
        网页sign算法，现在不需要了，直接固定
        """
        self.sign = 'TG2uvBAbGAHzG19a.rniF0xtrq'
        return self.sign

    def get_user_info(self):
        """
        取用户信息
        查询结果在 self.user_info
        """
        if self.url:
            self.__url2uid()
        url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=' + self.id
        try:
            headers = {
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
            }
            res = requests.get(url, headers=headers)
            if res.json()['status_code'] == 4:
                return
            info = res.json().get('user_info', dict())
        except Exception as e:
            print(e)
            info = dict()
        self.user_info = info
        # 下载路径
        username = '{}_{}_{}'.format(self.user_info.get('short_id', '0'),
                                     self.user_info.get('nickname', '无昵称'), self.type)
        self.download_path = Download.title2path(username)  # 需提前处理非法字符串

    def get_challenge_info(self):
        """
        取话题挑战信息
        查询结果在 self.challenge_info
        """
        if self.url:
            self.__url2id()
        url = 'https://www.iesdouyin.com/web/api/v2/challenge/info/?ch_id=' + self.id
        try:
            res = self.http.get(url).json()
            info = res.get('ch_info', dict())
        except Exception as e:
            print(e)
            info = dict()
        self.challenge_info = info
        # 话题挑战下载路径
        username = '{}_{}_{}'.format(self.challenge_info.get('cid', '0'),
                                     self.challenge_info.get('cha_name', '无标题'), self.type)
        self.download_path = Download.title2path(username)  # 需提前处理非法字符串

    def get_music_info(self):
        """
        取音乐原声信息
        查询结果在 self.music_info
        """
        if self.url:
            self.__url2id()
        url = 'https://www.iesdouyin.com/web/api/v2/music/info/?music_id=' + self.id
        try:
            headers = {
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
            }
            res = requests.get(url, headers=headers).json()
            info = res.get('music_info', dict())
        except Exception as e:
            print(e)
            info = dict()
        self.music_info = info
        # 音乐原声下载路径
        username = '{}_{}_{}'.format(self.music_info.get('mid', '0'), self.music_info.get('title', '无标题'),
                                     self.type)
        self.download_path = Download.title2path(username)  # 需提前处理非法字符串

    def crawling_users_post(self):
        """
        采集用户作品
        """
        self.type = 'post'
        self.__crawling_user()

    def crawling_users_like(self):
        """
        采集用户喜欢
        """
        self.type = 'like'
        self.__crawling_user()

    def crawling_challenge(self):
        """
        采集话题挑战
        """
        self.type = 'challenge'
        self.get_challenge_info()  # 取当前信息，用做下载目录

        # https://www.iesdouyin.com/web/api/v2/challenge/aweme/?ch_id=1570693184929793&count=9&cursor=9&aid=1128&screen_limit=3&download_click_limit=0&_signature=AXN-GQAAYUTpqVxkCT6GHQFzfg
        url = 'https://www.iesdouyin.com/web/api/v2/challenge/aweme/'

        cursor = '0'
        while self.has_more:
            params = {
                "ch_id": self.id,
                "count": "21",  # 可调大 初始值：9
                "cursor": cursor,
                "aid": "1128",
                "screen_limit": "3",
                "download_click_limit": "0",
                "_signature": self.sign
            }
            try:
                headers = {
                    'x-requested-with': 'XMLHttpRequest',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
                }
                res = requests.get(url, params=params, headers=headers)
                cursor = res.json()['cursor']
                self.has_more = res.json()['has_more']
                if res.json().get('aweme_list'):
                    for item in res.json()['aweme_list']:
                        info = dict()
                        info['desc'] = Download.title2path(item['desc'])  # 需提前处理非法字符串
                        info['uri'] = item['video']['play_addr']['uri']
                        info['play_addr'] = item['video']['play_addr']['url_list'][0]
                        info['dynamic_cover'] = item['video']['dynamic_cover']['url_list'][0]
                        info['status'] = 0  # 下载进度状态；等待下载：0，下载中：0.xx；下载完成：1
                        info['aweme_id'] = item['aweme_id']
                        info['share_count'] = item['duration']
                        if len(info['desc']) == 0:
                            info['desc'] = '该视频无描述'
                        # 列表格式
                        self.videosL.append(info)
                        # 字典格式
                        # self.videos[info['aweme_id']] = info

                        # 此处可以直接添加下载任务，不过考虑到下载占用网速,影响采集过程，所以采集完再下载
                    if self.limit:
                        more = len(self.videosL) - self.limit
                        if more >= 0:
                            # 如果给出了限制采集数目，超出的删除后直接返回
                            self.has_more = False
                            # 列表格式
                            self.videosL = self.videosL[:self.limit]
                            # 字典格式
                            # for i in range(more):
                            #     self.videos.popitem()
                            # return

                else:  # 还有作品的情况下没返回数据则进入这里
                    print('未采集完成，但返回作品列表为空')

            except Exception as e:
                print(e)
                print('话题挑战采集出错')
        print('话题挑战采集完成')

    def crawling_music(self):
        """
        采集音乐原声
        """
        self.type = 'music'
        global play_url
        self.get_user_info()  # 取当前信息，用做下载目录
        # https://www.iesdouyin.com/web/api/v2/music/list/aweme/?music_id=6928362875564067592&count=9&cursor=18&aid=1128&screen_limit=3&download_click_limit=0&_signature=5ULmIQAAhRYNmMRcpDm2COVC5j
        url = 'https://www.iesdouyin.com/web/api/v2/music/list/original/'
        cursor = '0'
        while self.has_more:
            params = {
                "user_id": '',
                'sec_uid': self.id,
                "count": "21",  # 可调大 初始值：9
                "cursor": cursor,
                "_signature": self.sign,
                'dytk': ''
            }
            try:
                headers = {
                    'x-requested-with': 'XMLHttpRequest',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
                }
                res = requests.get(url, params=params, headers=headers)
                cursor = res.json()['cursor']
                self.has_more = res.json()['has_more']
                # application_path = ''
                # if hasattr(sys, 'frozen'):
                #     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
                # if getattr(sys, 'frozen', None):
                #     application_path = sys._MEIPASS
                # elif __file__:
                #     application_path = os.path.dirname(__file__)
                # ruleFilePath = os.path.join(application_path, '')
                # os.chdir(ruleFilePath)
                if res.json().get('music_list'):
                    for item in res.json().get('music_list'):
                        info = dict()
                        info['share_count'] = item['use_count_desc']
                        info['desc'] = Download.title2path(item['title'])  # 需提前处理非法字符串
                        info['uri'] = item['play_url']['uri']
                        info['play_addr'] = item['play_url']['url_list'][0]
                        info['dynamic_cover'] = item['cover_hd']['url_list'][0]
                        info['status'] = 0  # 下载进度状态；等待下载：0，下载中：0.xx；下载完成：1
                        info['aweme_id'] = item['mid']
                        if len(info['desc']) == 0:
                            info['desc'] = '该视频无描述'
                        # 列表格式
                        info2 = {'play_addr': item['play_url']['url_list'][0]}
                        # 列表格式
                        play_url.append(item['play_url']['url_list'][0])
                        self.videosL.append(info2)
                        # 字典格式
                        # self.videos[info['aweme_id']] = info
                        # 此处可以直接添加下载任务，不过考虑到下载占用网速,影响采集过程，所以采集完再下载
                    if self.limit:
                        more = len(self.videosL) - self.limit
                        if more >= 0:
                            # 如果给出了限制采集数目，超出的删除后直接返回
                            self.has_more = False
                            # 列表格式
                            self.videosL = self.videosL[:self.limit]
                            # 字典格式
                            # for i in range(more):
                            #     self.videos.popitem()
                            # return
                else:  # 还有作品的情况下没返回数据则进入这里
                    print('未采集完成，但返回作品列表为空')
            except Exception as e:
                print(e)
                print('音乐原声采集出错')
        print('音乐原声采集完成')

    def __crawling_user(self):
        """
        采集用户作品/喜欢
        """
        self.get_user_info()  # 取当前用户信息，昵称用做下载目录

        max_cursor = 0
        # https://www.iesdouyin.com/web/api/v2/aweme/like/?sec_uid=MS4wLjABAAAAaJO9L9M0scJ_njvXncvoFQj3ilCKW1qQkNGyDc2_5CQ&count=21&max_cursor=0&aid=1128&_signature=2QoRnQAAuXcx0DPg2DVICdkKEY&dytk=
        # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAaJO9L9M0scJ_njvXncvoFQj3ilCKW1qQkNGyDc2_5CQ&count=21&max_cursor=0&aid=1128&_signature=DrXeeAAAbwPmb.wFM3e63w613m&dytk=
        url = 'https://www.iesdouyin.com/web/api/v2/aweme/{}/'.format(self.type)
        print(self.type)
        while self.has_more:
            params = {
                "sec_uid": self.id,
                "count": "21",
                "max_cursor": max_cursor,
                "aid": "1128",
                "_signature": self.sign,
                "dytk": ""
            }
            try:
                headers = {
                    'x-requested-with': 'XMLHttpRequest',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
                }
                res = requests.get(url, params=params, headers=headers)
                max_cursor = res.json()['max_cursor']
                self.has_more = res.json()['has_more']
                self.__append_videos(res.json())
            except Exception as e:
                print(e)
                print('作品采集出错')
                return
        print('作品采集完成')

    def __append_videos(self, res):
        """
        数据入库
        """
        # application_path = ''
        # if hasattr(sys, 'frozen'):
        #     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
        # if getattr(sys, 'frozen', None):
        #     application_path = sys._MEIPASS
        # elif __file__:
        #     application_path = os.path.dirname(__file__)
        # ruleFilePath = os.path.join(application_path, '')
        # os.chdir(ruleFilePath)
        # print(ruleFilePath)
        global play_url
        if res.get('aweme_list'):
            for item in res['aweme_list']:
                info = item['statistics']
                info.pop('forward_count')
                info.pop('play_count')
                # info['desc'] = Download.title2path(item['desc'])  # 需提前处理非法字符串
                # info['uri'] = item['video']['play_addr']['uri']
                info['play_addr'] = item['video']['play_addr']['url_list'][0]
                # info['dynamic_cover'] = item['video']['dynamic_cover']['url_list'][0]
                # info['status'] = 0  # 下载进度状态；等待下载：0，下载中：0.xx；下载完成：1
                # if len(info['desc']) == 0:
                #     info['desc'] = '该视频无描述'
                info2 = {'play_addr': item['video']['play_addr']['url_list'][0]}
                # 列表格式
                play_url.append(item['video']['play_addr']['url_list'][0])
                self.videosL.append(info2)
                # 字典格式
                # self.videos[info['aweme_id']] = info

                # 此处可以直接添加下载任务，不过考虑到下载占用网速,影响采集过程，所以采集完再下载
            if self.limit:
                more = len(self.videosL) - self.limit
                if more >= 0:
                    # 如果给出了限制采集数目，超出的删除后直接返回
                    self.has_more = False
                    # 列表格式
                    self.videosL = self.videosL[:self.limit]
                    # 字典格式
                    # for i in range(more):
                    #     self.videos.popitem()
                    # return

        else:  # 还有作品的情况下没返回数据则进入这里
            print('未采集完成，但返回作品列表为空')

    def download_all(self, type_):
        """
        作品抓取完成后，统一添加下载任务
        可选择在外部注册回调函数，监听下载任务状态
        """
        save_path = '{}/{}.mp4'
        if type_ == 'music':
            save_path = '{}/{}.mp3'

        for id, video in enumerate(self.videosL):
            # for id, video in self.videos.items():
            if len(video['desc']) == 0:
                video['desc'] = '该视频无描述'
            print(save_path.format(self.download_path, video['desc']))
            gid = self.aria2.download(url=video['play_addr'],
                                      filename=save_path.format(self.download_path, video['desc'])
                                      # ,options={'gid': id}  # 指定gid
                                      )
            self.gids[gid] = id  # 因为传入gid必须16位，所以就不指定gid了，另存一个字典映射
        print('下载任务投递完成')


class Task(object):
    def __init__(self, type_search='user', limit=10):
        """
        抖音采集命令行版本
        可指定下载类别：user; like; challenge; music，默认为user
        可指定下载数量：limit，默认为0，即全部下载
        """
        self.__type = type_search
        self.__limit = limit
        self.douyin = None
        # key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        #                      r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        # self.dir_path = str(winreg.QueryValueEx(key, "Desktop")[0]).replace('\\', '/') + '/'

    def download(self, target, number, user_type="0"):
        """
        单个下载
        """
        if user_type == "0":
            self.__type = 'user'
        elif user_type == "1":
            self.__type = 'like'
        elif user_type == "2":
            self.__type = 'music'
        self.douyin = Douyin(target, number)
        print('开始采集')
        print(self.__type)
        if self.__type == 'user':
            # 用户作品
            print("用户作品")
            self.douyin.crawling_users_post()
        elif self.__type == 'like':
            # 用户喜欢[不可用]
            self.douyin.crawling_users_like()
        elif self.__type == 'challenge':
            # 话题挑战
            self.douyin.crawling_challenge()
        elif self.__type == 'music':
            # 音乐原声
            self.douyin.crawling_music()
        else:
            print('输入格式错误')
            return

    def task_pause(self):
        return self.douyin.aria2.task_pause()

    def continue_task(self):
        return self.douyin.aria2.continue_task()

    def start_download(self):
        print('开始下载')
        print(len(self.douyin.videosL))
        self.douyin.download_all(self.__type)
        # 外部添加回调函数，监听下载任务状态
        # 结束监听：self.douyin.aria2.stop_listening()
        # on_finish监听到任务全部完成时会自动结束监听
        # （如果出现暂停的任务会无法自动结束，需要外部结束监听）
        # 不结束监听会阻塞进程，导致程序无法关闭
        self.douyin.aria2.start_listening(on_start=self._on_finish,
                                          on_stop=self._on_finish,
                                          on_complete=self._on_finish,
                                          on_error=self._on_finish,
                                          on_pause=self._on_pause)
        # 有需要（界面）再循环监听下载状态，可在外部添加回调函数
        self.douyin.aria2.start_loop(on_loop=self._on_loop)
        print('当前任务流程结束，等待下载完成')
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        dir_path = str(winreg.QueryValueEx(key, "Desktop")[0]).replace('\\', '/') + '/下载'
        with open(dir_path + '/{}.json'.format(self.douyin.download_path), 'w', encoding='utf-8') as f:
            json.dump(self.douyin.videosL, f, ensure_ascii=False)  # 中文不用Unicode编码
            # json.dump(self.douyin.videos, f, ensure_ascii=False)  # 中文不用Unicode编码

    def download_batch(self, target, number):
        """
        批量下载
        文件格式：一行一个链接/id
        """
        print(target)
        with open(target, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                print(line.strip())
                self.download(line.strip(), number)
                while not self.douyin.finish:
                    time.sleep(1)

    def _on_finish(self, gid):
        """
        任务完成/停止/失败时的回调函数
        任务完成时结束监听
        """
        print(self.douyin.aria2.get_files(gid)[0]['path'], '任务完成（成功/停止/失败）')
        stat = self.douyin.aria2.get_stat()
        print('当前下载信息：', stat.__dict__['_struct'])
        if stat.num_active + stat.num_waiting == 0:  # 正在进行任务数=0，任务全部完成
            # 当前任务由此结束
            self.douyin.aria2.stop_listening()
            self.douyin.aria2.stop_loop()
            self.douyin.finish = True
            print('当前任务队列下载完成，3秒后结束当前任务')
            time.sleep(3)
            print('任务已完成')

    def _on_loop(self, info: list):
        """
        循环监听回调函数
        参数info为进行中的下载任务状态
        每秒一次
            'gid': str,
            '文件名称': /下载/文件名.mp4,
            '下载速度': 1.25MB/s,
            '下载进度': 12.25%
        """
        # 固定位置输出，暂时未找到命令行固定多行内容输出方法
        # print(info)
        pass

    def _on_pause(self, gid):
        """
        任务暂停时的回调函数
        """
        print(gid, '任务暂停')


class API(Task):
    """
    前后端交互接口
    """

    def __init__(self):
        """
        初始化
        """
        super().__init__()
        # print(sys.path[0])
        # print(sys.argv[0])
        # print(os.path.dirname(os.path.realpath(sys.executable)))
        # print(os.path.dirname(os.path.realpath(sys.argv[0])))
        # application_path = ''
        # if hasattr(sys, 'frozen'):
        #     print("frozen检测到")
        #     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
        # if getattr(sys, 'frozen', None):
        #     application_path = sys._MEIPASS
        # elif __file__:
        #     application_path = os.path.dirname(__file__)
        # print(application_path)
        # self.ruleFilePath = os.path.join(application_path, '')
        # print(self.ruleFilePath)
        # os.chdir(self.ruleFilePath)
        # print(self.ruleFilePath)
        global play_url
        self.url_list = play_url
        print(len(self.url_list))
        self.over_list = []

    def init(self, type_search='user', limit=0):
        """
        在UI中，类的初始化无法传参，所以需要重新定义初始化
        """
        super().__init__(type_search=type_search, limit=limit)

    def load_video(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        save_path_global = str(winreg.QueryValueEx(key1, "Desktop")[0]).replace('\\', '/') + '/beau_girl.txt'
        urls = []
        user_type = []
        if os.path.exists(save_path_global):
            file_name = save_path_global
            print("发现桌面文件")
            with open(file_name, 'r') as file:
                print(file_name)
                temp_info = file.readlines()
                print(temp_info)
                for i in temp_info:
                    if i != '\n':
                        x = i.split(' ')
                        urls.append(x[0])
                        print(x[1])
                        try:
                            user_type.append(x[1].replace('\n', ''))
                        except:
                            user_type.append(0)

        else:
            for girl_info in girl_home:
                urls.append(girl_info[0])
                user_type.append(girl_info[1])
        global play_url
        play_url.clear()
        temp_url = 'http://h.guomis.cn/video?type=%E6%94%92%E5%8A%B2%E8%8A%82%E7%9B%AE'
        try:
            hesi = requests.get(temp_url, headers=random_user()).json()
            for hesi_i in hesi['list']:
                play_url.append(hesi_i['urllink'])
        except:
            pass
        for data in self.executor.map(super().download, urls, [False] * len(urls), user_type):
            print("in main: get page {}s success".format(data))
        file.close()

    def next_one(self):
        global play_url
        if len(self.url_list) <= 10:
            self.url_list = play_url
            print("没有更多了")
            print(len(self.url_list))

        self.url_list = play_url
        number = random.randint(0, len(self.url_list) - 1)
        print('刷新')
        print(number)
        if self.url_list[number] not in self.over_list:
            self.over_list.append(self.url_list[number])
            return self.url_list[number]
        else:
            return ""

    def savedir(self):
        result = window.create_file_dialog(webview.FOLDER_DIALOG, directory='/', )
        self.save_dir = result

    # def on_press(self, key):
    #     '按下按键时执行。'
    #     try:
    #         if key == keyboard.KeyCode.from_char('enter'):
    #             pass
    #         elif key == keyboard.Key.down:
    #             temp = ''
    #     except AttributeError:
    #         print('special key {0} pressed'.format(key))
    #
    # # 通过属性判断按键类型。
    #
    # def on_release(self, key):
    #     '松开按键时执行。'
    #     print('{0} released'.format(key))
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return False


if __name__ == "__main__":
    api = API()
    chinese = {
        'global.quitConfirmation': u'确定要关闭吗?',
    }
    window = webview.create_window(
        title='抖音精选-为你筛选最想看的内容',  # 标题
        url='static/index.html',  # 本地文件或网络URL
        js_api=api,  # 暴露api对象，或使用flask等服务创建的对象
        width=400,  # 窗口宽；好像和网页中大小不一样，网页中大小为620*470px
        height=729,  # 窗口高
        resizable=True,  # 是否可以缩放窗口
        frameless=False,  # 窗口是否无边框
        confirm_close=True,  # 退出确认
    )
    webview.start(debug=True, localization=chinese)
