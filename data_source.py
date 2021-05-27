import hoshino, sqlite3, os ,json

try:
    config = hoshino.config.groupname_sync.config
except:
    hoshino.logger.error('not found config of groupname_sync')


def get_db_path():
    if not (os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                        "yobot/yobot/src/client/yobot_data/yobotdata.db"))) or os.access(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                                                                                                                      "yobot/yobot/src/client/yobot_data/yobotdata.db")), os.R_OK)):
        raise OSError
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                           "yobot/yobot/src/client/yobot_data/yobotdata.db"))
    return db_path

def get_web_address():
    if not os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                       "yobot/yobot/src/client/yobot_data/yobot_config.json"))):
        raise OSError
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                               "yobot/yobot/src/client/yobot_data/yobot_config.json"))
    with open(f'{config_path}', 'r', encoding='utf8')as fp:
        yobot_config = json.load(fp)
    website_suffix = str(yobot_config["public_basepath"])
    web_address = "http://127.0.0.1" + ":" + str(hoshino.config.PORT) + website_suffix
    return web_address

try:
    db_path = get_db_path()
except OSError:
    db_path = config.db_path

def get_apikey(gid: int) -> str:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'select apikey from clan_group where group_id={gid}')
    apikey = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return apikey
