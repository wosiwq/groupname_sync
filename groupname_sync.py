from hoshino import Service, priv
from .data_source import *
import aiohttp

name_old = None
default_groupname = None

sv = Service('群昵称同步', manage_priv=priv.SUPERUSER, enable_on_default=False)

try:
    config = hoshino.config.groupname_sync.config
except:
    hoshino.logger.error('not found config of clanbattlereport')

try:
    yobot_url = get_web_address()
except OSError:
    yobot_url = config.yobot_url

@sv.on_message()
async def groupname_sync(bot, ev):
    # 访问yobot api获取伤害等信息
    global name_old
    gid = ev.group_id

    if default_groupname == None:
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

    if data['challenges'][len(data['challenges'])-1]['health_ramain'] != 0:
        name_new = str(data['challenges'][len(data['challenges'])-1]['cycle']) + '-' + str(data['challenges'][len(data['challenges'])-1]['boss_num'])
    elif data['challenges'][len(data['challenges'])-1]['boss_num'] == 5 :
        name_new = str(data['challenges'][len(data['challenges']) - 1]['cycle']+1) + '-1'
    else:
        name_new = str(data['challenges'][len(data['challenges']) - 1]['cycle']) + '-' + str(data['challenges'][len(data['challenges']) - 1]['boss_num'] + 1)
    if name_old == name_new:
        return
    else:
        name_old = name_new
        try:
            await bot.set_group_name(
                group_id = gid,
                group_name = default_groupname+  name_old
            )
        except Exception as e:
            await bot.send(ev, '群名修改失败惹...\n错误代码：{e}')

@sv.on_prefix('初始化群名')
async def set_default_groupname(bot, ev):
    global default_groupname
    gid = ev.group_id
    try:
        group_info = await bot.get_group_info(
            group_id=gid
        )
        default_groupname = group_info['group_name']
        await bot.send(ev, '初始化成功')
    except Exception as e:
        await bot.send(ev, '获取群名失败...')
    pass

@sv.on_prefix(('修改群名','设置群名'))
async def set_group_name(bot, ev):
    global default_groupname
    default_groupname = None
    gid = ev.group_id
    name = ev.message.extract_plain_text()
    await bot.set_group_name(
        group_id = gid,
        group_name = name
    )