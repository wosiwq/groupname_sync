from hoshino import Service, priv
from .data_source import *
import aiohttp

sv = Service('群昵称同步', manage_priv=priv.SUPERUSER, enable_on_default=False)

name_old = None
group_list = {}
FILE_PATH = os.path.dirname(__file__)

try:
    config = hoshino.config.groupname_sync.config
except:
    hoshino.logger.error('not found config of clanbattlereport')

try:
    yobot_url = get_web_address()
except OSError:
    yobot_url = config.yobot_url


def save_group_list():
    with open(os.path.join(FILE_PATH, 'group_list.json'), 'w', encoding='UTF-8') as f:
        json.dump(group_list, f, ensure_ascii=False)


if not os.path.exists(os.path.join(FILE_PATH, 'group_list.json')):
    save_group_list()
    hoshino.logger.error('未找到group_list.json，已创建')

with open(os.path.join(FILE_PATH, 'group_list.json'), 'r', encoding='UTF-8') as f:
    group_list = json.load(f)

@sv.on_message()
async def groupname_sync(bot, ev):
    # 访问yobot api获取伤害等信息
    global name_old
    gid = ev.group_id

    if not group_list.get(str(gid)):
        return

    if len(yobot_url) == 0:
        await bot.finish(ev, '获取api地址失败，请检查配置')
    if not get_db_path():
        await bot.finish(ev, '获取数据库路径失败，请检查配置')
    try:
        apikey = get_apikey(gid)
    except:
        await bot.finish(ev, '本群未创建公会，或已禁止API获取数据，请检查设置后再试')

    api_url = f'{yobot_url}clan/{gid}/statistics/api/?apikey={apikey}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
    except Exception as e:
        # sv.logger.error(f'Error: {e}')
        # result['msg'] = '无法访问API，请检查yobot服务器状态'
        print('无法访问API，请检查yobot服务器状态')
        return

    if data['challenges'][len(data['challenges']) - 1]['health_ramain'] != 0:
        name_new = str(data['challenges'][len(data['challenges']) - 1]['cycle']) + '-' + str(
            data['challenges'][len(data['challenges']) - 1]['boss_num'])
    elif data['challenges'][len(data['challenges']) - 1]['boss_num'] == 5:
        name_new = str(data['challenges'][len(data['challenges']) - 1]['cycle'] + 1) + '-1'
    else:
        name_new = str(data['challenges'][len(data['challenges']) - 1]['cycle']) + '-' + str(
            data['challenges'][len(data['challenges']) - 1]['boss_num'] + 1)
    if name_old == name_new:
        return
    else:
        name_old = name_new
        try:
            await bot.set_group_name(
                group_id=gid,
                group_name=group_list[str(gid)] + name_old
            )
        except Exception as e:
            await bot.send(ev, f'群名修改失败惹...\n错误代码：{str(e)}')


@sv.on_prefix('启用群昵称同步')
async def enable_groupname_sync(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '抱歉，您非管理员，无此指令使用权限')
    global name_old
    name_old = None
    gid = ev.group_id
    while group_list.get(str(gid)):
        group_list.pop(str(gid))
    s = ev.message.extract_plain_text()
    if s:
        group_list.update({str(gid) : s})
        save_group_list()
        await bot.send(ev, '初始化成功，默认群名设置为'+s)
    else:
        try:
            group_info = await bot.get_group_info(
                group_id=gid
            )
            group_list.update({str(gid) : group_info['group_name']})
            save_group_list()
            await bot.send(ev, '初始化成功，默认群名设置为'+group_info['group_name'])
        except Exception as e:
            await bot.send(ev, '获取群名失败...')

@sv.on_fullmatch('禁用群昵称同步')
async def disable_groupname_sync(bot, ev):
    global name_old
    gid = ev.group_id
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '抱歉，您非管理员，无此指令使用权限')
    await bot.set_group_name(
        group_id=gid,
        group_name=group_list[str(gid)]
    )
    name_old = None
    group_list.pop(str(gid))
    save_group_list()
    await bot.send(ev, '已禁用')

@sv.on_prefix(('修改群名', '设置群名'))
async def set_group_name(bot, ev):
    gid = ev.group_id
    group_list.pop(str(gid))
    name = ev.message.extract_plain_text()
    await bot.set_group_name(
        group_id=gid,
        group_name=name
    )
    group_list.update({str(gid) : name})
    save_group_list()
