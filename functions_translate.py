# -*- coding:utf-8 -*-
from os import system
from time import sleep, time
from hashlib import md5
from json import loads
from requests import get
# from traceback import format_exc


# 功能：调用百度翻译API接口，翻译日语简介
# 参数：百度翻译api账户api_id, key，需要翻译的内容，目标语言
# 返回：中文简介str
# 辅助：os.system, hashlib.md5，time.time，requests.get，json.loads
def tran_plot(api_id, key, word, to_lang):
    for retry in range(10):
        # 把账户、翻译的内容、时间 混合md5加密，传给百度验证
        salt = str(time())[:10]
        final_sign = api_id + word + salt + key
        final_sign = md5(final_sign.encode("utf-8")).hexdigest()
        # 表单paramas
        paramas = {
            'q': word,
            'from': 'jp',
            'to': to_lang,
            'appid': '%s' % api_id,
            'salt': '%s' % salt,
            'sign': '%s' % final_sign
        }
        try:
            response = get('http://api.fanyi.baidu.com/api/trans/vip/translate', params=paramas, timeout=(6, 7))
        except:
            print('    >百度翻译拉闸了...重新翻译...')
            continue
        content = str(response.content, encoding="utf-8")
        # 百度返回为空
        if not content:
            print('    >百度翻译返回为空...重新翻译...')
            sleep(1)
            continue
        # 百度返回了dict json
        json_reads = loads(content)
        # print(json_reads)
        if 'error_code' in json_reads:    # 返回错误码
            error_code = json_reads['error_code']
            if error_code == '54003':
                print('    >请求百度翻译太快...技能冷却1秒...')
                sleep(1)
            elif error_code == '54005':
                print('    >发送了太多超长的简介给百度翻译...技能冷却3秒...')
                sleep(3)
            elif error_code == '52001':
                print('    >连接百度翻译超时...重新翻译...')
            elif error_code == '52002':
                print('    >百度翻译拉闸了...重新翻译...')
            elif error_code == '54003':
                print('    >使用过于频繁，百度翻译不想给你用了...')
                system('pause')
            elif error_code == '52003':
                print('    >请正确输入百度翻译API账号，请阅读【使用说明】！')
                print('>>javsdt已停止工作...')
                system('pause')
            elif error_code == '58003':
                print('    >你的百度翻译API账户被百度封禁了，请联系作者，告诉你解封办法！“')
                print('>>javsdt已停止工作...')
                system('pause')
            elif error_code == '90107':
                print('    >你的百度翻译API账户还未通过认证或者失效，请前往API控制台解决问题！“')
                print('>>javsdt已停止工作...')
                system('pause')
            else:
                print('    >百度翻译error_code！请截图联系作者！', error_code)
            continue
        else:  # 返回正确信息
            return json_reads['trans_result'][0]['dst']
    print('    >翻译简介失败...请截图联系作者...')
    return '【百度翻译出错】' + word


# 功能：去除xml文档不允许的特殊字符 &<>
# 参数：（文件名、简介、标题）str
# 返回：str
# 辅助：无
def replace_xml(name):
    # 替换xml中的不允许的特殊字符 .replace('\'', '&apos;').replace('\"', '&quot;')
    # .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')  nfo基于xml，xml中不允许这5个字符，但实际测试nfo只不允许左边3个
    return name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                .replace('\n', '').replace('\t', '').replace('\r', '').rstrip()

num_fail=0

def translate_process(plot):

    to_language = 'zh'          # 目标语言，百度翻译规定 zh是简体中文，cht是繁体中文
    tran_id = "20200611000492252"
    tran_sk = "VUkDD6PsemI38iPgsR9a"
    global num_fail 
    plot = tran_plot(tran_id, tran_sk, plot, to_language)
    if plot.startswith('【百度'):
        num_fail += 1
        print('    >第' + str(num_fail) + '个失败！翻译简介失败：' + '\n')
        plot = ''
    # 去除xml文档不允许的特殊字符 &<>  \/:*?"<>|
    plot = replace_xml(plot)
    # print(plot)]
    return plot



