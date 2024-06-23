#!/usr/bin/env python
# -*- coding=utf-8 -*-


class Message(object):
    INNER_FLAG = 0x10000000    # 服务器内部消息标识
    MSG_MASK = 0x0FFFFFFF

    ID_REQ = 0x01000000        # 请求
    ID_ACK = 0x02000000        # 应答
    ID_NTF = 0x04000000        # 通知
    ID_CMD = 0x08000000        # 命令

    # 框架内部消息
    ID_BASE_INNER_SYSTEM = 0x00001000
    MSG_INNER_BROKEN = (ID_BASE_INNER_SYSTEM + 0x03)               # 前端断线
    MSG_INNER_BI_REPORT = (ID_BASE_INNER_SYSTEM + 0x07)            # 数据统计上报
    MSG_INNER_SERVER_REGISTER = (ID_BASE_INNER_SYSTEM + 0x08)      # 服务器注册
    ID_BASE_INNER_SYSTEM_END = 0x00001FFF

    # 游戏内部消息
    ID_BASE_INNER_GAME = 0x00002000
    MSG_INNER_TIMER = (ID_BASE_INNER_GAME + 0x01)                  # 定时器
    ID_BASE_INNER_GAME_END = 0x00002FFF

    # 服务器与客户端框架消息
    ID_BASE_OUTER_SYSTEM = 0x00008000
    MSG_SYS_HOLD = (ID_BASE_OUTER_SYSTEM + 0x64)                   # 保持连接
    MSG_SYS_USER_INFO = (ID_BASE_OUTER_SYSTEM + 0x65)              # 玩家信息
    MSG_SYS_GAME_INFO = (ID_BASE_OUTER_SYSTEM + 0x66)              # 游戏数据
    MSG_SYS_QUICK_START = (ID_BASE_OUTER_SYSTEM + 0x67)            # 快速开始
    MSG_SYS_JOIN_TABLE = (ID_BASE_OUTER_SYSTEM + 0x68)             # 进入桌子
    MSG_SYS_SIT_DOWN = (ID_BASE_OUTER_SYSTEM + 0x69)               # 坐下
    MSG_SYS_READY = (ID_BASE_OUTER_SYSTEM + 0x6A)                  # 准备
    MSG_SYS_CANCEL_READY = (ID_BASE_OUTER_SYSTEM + 0x6B)           # 取消准备
    MSG_SYS_STAND_UP = (ID_BASE_OUTER_SYSTEM + 0x6C)               # 站起
    MSG_SYS_LEAVE_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6D)            # 离开桌子
    MSG_SYS_VIEWER_JOIN_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6E)      # 旁观者加入桌子
    MSG_SYS_VIEWER_LEAVE_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6F)     # 旁观者离开桌子
    MSG_SYS_FORCE_QUIT = (ID_BASE_OUTER_SYSTEM + 0x70)             # 强制退出,游戏中
    MSG_SYS_TABLE_EVENT = (ID_BASE_OUTER_SYSTEM + 0x71)            # table event
    MSG_SYS_BROADCAST = (ID_BASE_OUTER_SYSTEM + 0x72)              # 广播消息
    MSG_SYS_MULTIPLE_LOGIN = (ID_BASE_OUTER_SYSTEM + 0x73)         # 重复登陆
    MSG_SYS_FLUSH = (ID_BASE_OUTER_SYSTEM + 0x74)                  # 前端刷新
    MSG_SYS_TRUSTEE = (ID_BASE_OUTER_SYSTEM + 0x75)                # 托管
    MSG_SYS_ENTER_ROOM = (ID_BASE_OUTER_SYSTEM + 0x76)             # 进入房间
    MSG_SYS_LEAVE_ROOM = (ID_BASE_OUTER_SYSTEM + 0x77)             # 离开房间
    MSG_SYS_ROOM_EVENT = (ID_BASE_OUTER_SYSTEM + 0x78)             # 房间事件
    MSG_SYS_TIMEOUT = (ID_BASE_OUTER_SYSTEM + 0x79)                # 超时
    MSG_SYS_ROOM_LIST = (ID_BASE_OUTER_SYSTEM + 0x7A)              # 房间列表
    MSG_SYS_BENEFIT = (ID_BASE_OUTER_SYSTEM + 0x7B)                # 救济金
    MSG_SYS_RECONNECT = (ID_BASE_OUTER_SYSTEM + 0x7C)              # 断线重连
    MSG_SYS_BIND_REWARD = (ID_BASE_OUTER_SYSTEM + 0x7D)            # 绑定手机获取奖励
    MSG_SYS_BUY_WEAPON = (ID_BASE_OUTER_SYSTEM + 0x7E)             # 购买炮台
    MSG_SYS_USE_WEAPON = (ID_BASE_OUTER_SYSTEM + 0x7F)             # 使用炮台
    MSG_SYS_WBRANK_LIST = (ID_BASE_OUTER_SYSTEM + 0x80)            # 世界boss排行榜列表
    MSG_SYS_WBRANK_CAST = (ID_BASE_OUTER_SYSTEM + 0x81)            # 广播下发后，客户端向服务器请求排行榜列表

    MSG_SYS_SERVER_INFO = (ID_BASE_OUTER_SYSTEM + 0x83)            # 服务器信息
    MSG_SYS_LED = (ID_BASE_OUTER_SYSTEM + 0x84)                    # led信息
    #MSG_SYS_SERVER_TIME = (ID_BASE_OUTER_SYSTEM + 0x85)            # 服务器毫秒时间戳
    MSG_SYS_BIND_GAME = (ID_BASE_OUTER_SYSTEM + 0x86)              # 绑定游戏
    MSG_SYS_RANK_LIST = (ID_BASE_OUTER_SYSTEM + 0x87)              # 获取排行榜
    MSG_SYS_SIGN_IN = (ID_BASE_OUTER_SYSTEM + 0x88)                # 签到
    MSG_SYS_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x89)                 # 获取配置
    MSG_SYS_PROPS_LIST = (ID_BASE_OUTER_SYSTEM + 0x8A)             # 道具列表(背包)
    MSG_SYS_USE_PROPS = (ID_BASE_OUTER_SYSTEM + 0x8B)              # 使用道具
    MSG_SYS_RAFFLE = (ID_BASE_OUTER_SYSTEM + 0x8C)                 # 抽奖
    MSG_SYS_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0x8D)              # 每日任务
    MSG_SYS_CONSUME_TASK = (ID_BASE_OUTER_SYSTEM + 0x8E)           # 领取任务
    MSG_SYS_PRESENT = (ID_BASE_OUTER_SYSTEM + 0x8F)                # 赠送
    MSG_SYS_INNER_BUY = (ID_BASE_OUTER_SYSTEM + 0x90)              # 内部购买(二级货币的消耗)
    MSG_SYS_EXCHANGE = (ID_BASE_OUTER_SYSTEM + 0x91)               # 兑换(货币间兑换, 比如coupon兑换)
    MSG_SYS_CONSUME_CDKEY = (ID_BASE_OUTER_SYSTEM + 0x92)          # 兑换码(比如活动送兑换码)
    MSG_SYS_ACTIVITY_LIST = (ID_BASE_OUTER_SYSTEM + 0x93)          # 活动列表
    MSG_SYS_CONSUME_ACTIVITY = (ID_BASE_OUTER_SYSTEM + 0x94)       # 领取活动
    MSG_SYS_HISTORY = (ID_BASE_OUTER_SYSTEM + 0x95)                # 记录
    MSG_SYS_SHARE_INFO = (ID_BASE_OUTER_SYSTEM + 0x96)             # 获取分享模块信息
    MSG_SYS_SHARE = (ID_BASE_OUTER_SYSTEM + 0x97)                  # 分享
    MSG_SYS_BIND_INVITER = (ID_BASE_OUTER_SYSTEM + 0x98)           # 绑定邀请人
    MSG_SYS_INVITE_INFO = (ID_BASE_OUTER_SYSTEM + 0x99)            # 获取分享奖励信息(好友达成条件)
    MSG_SYS_INVITE_REWARD = (ID_BASE_OUTER_SYSTEM + 0x9A)          # 领取分享奖励（好友达成条件）

    # MSG_SYS_GROUP_BUY_INFO = (ID_BASE_OUTER_SYSTEM + 0x9B)         # 获取团购信息
    # MSG_SYS_GROUP_BUY_REWARD = (ID_BASE_OUTER_SYSTEM + 0x9C)       # 获取团购奖励
    # MSG_SYS_MARK_STATE = (ID_BASE_OUTER_SYSTEM + 0x9D)             # 红点标记信息

    MSG_SYS_UP_BARREL = (ID_BASE_OUTER_SYSTEM + 0x9E)              # 强化炮
    MSG_SYS_RESOLVE_STONE = (ID_BASE_OUTER_SYSTEM + 0x9F)          # 分解强化石
    MSG_SYS_POKE_MOLE = (ID_BASE_OUTER_SYSTEM + 0xA0)              # 打地鼠
    MSG_SYS_POKE_MOLE_CHANGE = (ID_BASE_OUTER_SYSTEM + 0xA1)       # 打地鼠换场景
    MSG_SYS_POKE_MOLE_INFO = (ID_BASE_OUTER_SYSTEM + 0xA2)         # 打地鼠信息
    MSG_SYS_POKE_MOLE_OL = (ID_BASE_OUTER_SYSTEM + 0xA3)           # 在线人数
    MSG_SYS_QUICK_TABLE_INFO = (ID_BASE_OUTER_SYSTEM + 0xA4)       # 获取桌子信息
    MSG_SYS_SWITCH_INFO = (ID_BASE_OUTER_SYSTEM + 0xA5)            # 获取开关信息
    MSG_SYS_AWARD_LIST = (ID_BASE_OUTER_SYSTEM + 0xA6)             # 获取奖励列表
    MSG_SYS_CONSUME_AWARD = (ID_BASE_OUTER_SYSTEM + 0xA7)          # 领取奖励
    MSG_SYS_HATCH_EGG = (ID_BASE_OUTER_SYSTEM + 0xA9)              # 宠物蛋孵化
    MSG_SYS_HATCH_QUICKEN = (ID_BASE_OUTER_SYSTEM + 0xAA)          # 宠物蛋孵化加速
    MSG_SYS_PET_INFO = (ID_BASE_OUTER_SYSTEM + 0xAB)               # 宠物信息
    MSG_SYS_PET_COMPOSE = (ID_BASE_OUTER_SYSTEM + 0xAC)            # 宠物合成
    MSG_SYS_PET_UP = (ID_BASE_OUTER_SYSTEM + 0xAD)                 # 宠物升级
    MSG_SYS_PET_CHOICE = (ID_BASE_OUTER_SYSTEM + 0xAE)             # 宠物选择
    MSG_SYS_IN_POKE_MOLE = (ID_BASE_OUTER_SYSTEM + 0xAF)           # 进入打地鼠之前 检查锁

    MSG_SYS_VILLAGE_CREATE = (ID_BASE_OUTER_SYSTEM + 0xB0)         # 公会创建
    MSG_SYS_VILLAGE_INFO = (ID_BASE_OUTER_SYSTEM + 0xB1)           # 公会信息
    MSG_SYS_VILLAGE_ADD = (ID_BASE_OUTER_SYSTEM + 0xB3)            # 公会加入
    MSG_SYS_VILLAGE_EXIT = (ID_BASE_OUTER_SYSTEM + 0xB9)           # 公会退出
    MSG_SYS_VILLAGE_LV_RANK = (ID_BASE_OUTER_SYSTEM + 0xB2)        # 公会等级排行
    MSG_SYS_VILLAGE_APPLYS = (ID_BASE_OUTER_SYSTEM + 0xB4)         # 公会申请列表
    MSG_SYS_VILLAGE_DEAL_APPLY = (ID_BASE_OUTER_SYSTEM + 0xB5)     # 公会处理申请
    MSG_SYS_VILLAGE_MEMBERS = (ID_BASE_OUTER_SYSTEM + 0xB7)        # 公会成员列表
    MSG_SYS_VILLAGE_SEARCH = (ID_BASE_OUTER_SYSTEM + 0xB6)         # 公会搜索
    MSG_SYS_VILLAGE_ADD_TYPE = (ID_BASE_OUTER_SYSTEM + 0xB8)       # 公会加入类型设置
    MSG_SYS_VILLAGE_SET_CALL = (ID_BASE_OUTER_SYSTEM + 0xBC)       # 公会宣言设置
    MSG_SYS_VILLAGE_KICK = (ID_BASE_OUTER_SYSTEM + 0xBB)           # 公会踢人
    MSG_SYS_VILLAGE_DEL = (ID_BASE_OUTER_SYSTEM + 0xBA)            # 公会解散
    MSG_SYS_QUICK_VILLAGE_TABLE = (ID_BASE_OUTER_SYSTEM + 0xBD)    # 公会房间信息

    MSG_SYS_MAIL_LIST = (ID_BASE_OUTER_SYSTEM + 0xD0)               # 邮件list
    MSG_SYS_MAIL_RECORD_LIST = (ID_BASE_OUTER_SYSTEM + 0xD1)        # 邮件记录list
    MSG_SYS_MAIL_RECEIVE = (ID_BASE_OUTER_SYSTEM + 0xD2)            # 邮件领取

    MSG_SYS_RANK = (ID_BASE_OUTER_SYSTEM + 0xD3)                    # 排行榜

    MSG_SYS_SHOP_BUY = (ID_BASE_OUTER_SYSTEM + 0xD4)                # 商城购买
    MSG_SYS_LIMIT_SHOP = (ID_BASE_OUTER_SYSTEM + 0xD5)              # 限时商城的入口
    MSG_SYS_SHOP_USER_INFO = (ID_BASE_OUTER_SYSTEM + 0xD6)          # 限时商城的入口
    MSG_SYS_SHOP_RECORD = (ID_BASE_OUTER_SYSTEM + 0xD7)             # 商城兑换记录

    MSG_SYS_DROP_COUPON = (ID_BASE_OUTER_SYSTEM + 0xD8)             #鸟券掉落

    MSG_SYS_VIP_RECEIVE_RECORD = (ID_BASE_OUTER_SYSTEM + 0xD9)      #VIP领取记录
    MSG_SYS_VIP_RECEIVE = (ID_BASE_OUTER_SYSTEM + 0xDA)             #VIP领取标记

    MSG_SYS_NEW_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0xDB)           # 任务列表
    MSG_SYS_TABLE_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0xDC)         # 房间任务
    MSG_SYS_RECEIVE_TASK_REWARD = (ID_BASE_OUTER_SYSTEM + 0xDD)     # 领取任务奖励
    MSG_SYS_TABLE_TASK_SINGLE = (ID_BASE_OUTER_SYSTEM + 0xDE)       # 任务完成推送单个任务下去
    MSG_SYS_ACTIVITY_RECEIVE = (ID_BASE_OUTER_SYSTEM + 0xDF)        # 任务活跃度领取
    MSG_SYS_ACTIVITY_TASK = (ID_BASE_OUTER_SYSTEM + 0xE0)           # 活动任务列表

    MSG_SYS_NEW_ACTIVITY_LIST = (ID_BASE_OUTER_SYSTEM + 0xE1)       # 活动列表
    MSG_SYS_NEW_ACTIVITY_CONFIG = (ID_BASE_OUTER_SYSTEM + 0xE2)     # 活动数据

    MSG_SYS_NEW_ACTIVITY_PAY_RAFFLE = (ID_BASE_OUTER_SYSTEM + 0xE3)       # 活动一点击抽奖
    MSG_SYS_NEW_ACTIVITY_PAY_SEND_RECORD = (ID_BASE_OUTER_SYSTEM + 0xE4)  # 活动一发送抽奖列表记录

    MSG_SYS_NEW_ACTIVITY_TASK_REWARD = (ID_BASE_OUTER_SYSTEM + 0xE5)       # 活动二接收任务奖励
    MSG_SYS_NEW_ACTIVITY_TASK_REWARD_TOTAL = (ID_BASE_OUTER_SYSTEM + 0xE6) # 活动二接收总奖励

    MSG_SYS_NEW_ACTIVITY_LOGIN_REWARD = (ID_BASE_OUTER_SYSTEM + 0xE7)      # 活动四接收登录奖励

    MSG_SYS_FFL_CONFIG = (ID_BASE_OUTER_SYSTEM + 0xE8)  # 配置
    MSG_SYS_FFL_START = (ID_BASE_OUTER_SYSTEM + 0xE9)  # 开始玩
    MSG_SYS_FFL_CHANGE = (ID_BASE_OUTER_SYSTEM + 0xEA)  # 换牌
    MSG_SYS_FFL_REWARD = (ID_BASE_OUTER_SYSTEM + 0xEB)  # 领取奖励
    MSG_SYS_FFL_OPEN = (ID_BASE_OUTER_SYSTEM + 0xEC)  # 领取奖励

    MSG_SYS_NEW_ACTIVITY_GIVE_REWARD = (ID_BASE_OUTER_SYSTEM + 0xED)  # 充值送炮领取奖励

    MSG_SYS_MODIFY_DROP_COUPON = (ID_BASE_OUTER_SYSTEM + 0xEE)    # 修改鸟券掉落标记

    MSG_SYS_PROPS_RECOVERY = (ID_BASE_OUTER_SYSTEM + 0x0101)       # 道具回收

    MSG_SYS_VIP_TABLE_CREATE = (ID_BASE_OUTER_SYSTEM + 0x0100)      # 创建并进入vip房
    MSG_SYS_VIP_TABLE_LIST = (ID_BASE_OUTER_SYSTEM + 0x0104)        # 获取vip房的列表
    MSG_SYS_VIP_TABLE_REFRESH = (ID_BASE_OUTER_SYSTEM + 0x0102)     # vip房的界面刷新
    MSG_SYS_VIP_TABLE_JOIN = (ID_BASE_OUTER_SYSTEM + 0x0103)        # 选择一个vip房进入F

    MSG_SYS_USER_DEAL = (ID_BASE_OUTER_SYSTEM + 0x0105)             # 用户的操作
    MSG_SYS_LIMIT_SHOP_OPEN = (ID_BASE_OUTER_SYSTEM + 0x0106)       # 后台修改限时商城的开启
    MSG_SYS_LIMIT_RAFFLE_OPEN = (ID_BASE_OUTER_SYSTEM + 0x0107)     # 后台修改奖金抽奖的开启
    MSG_SYS_SEND_RAFFLE_OPEN = (ID_BASE_OUTER_SYSTEM + 0x0108)      # 发送通知告诉前端奖金抽奖是否开启
    MSG_SYS_SET_RECHARGE_PRESENT = (ID_BASE_OUTER_SYSTEM + 0x0109)  # 后台对阿里微信充值赠送修改

    MSG_SYS_MATCH_READY = (ID_BASE_OUTER_SYSTEM + 0x010A)           # 竞技场匹配对手
    MSG_SYS_MATCH_START = (ID_BASE_OUTER_SYSTEM + 0x010B)           # 竞技场匹配完成进场
    MSG_SYS_MATCH_LEFT_TIME = (ID_BASE_OUTER_SYSTEM + 0x010C)       # 竞技场剩余时间下发
    MSG_SYS_MATCH_SEND_RANK = (ID_BASE_OUTER_SYSTEM + 0x010D)       # 竞技场下发积分排名
    MSG_SYS_MATCH_SEND_REWARD = (ID_BASE_OUTER_SYSTEM + 0x010F)     # 竞技场下发奖励排名
    MSG_SYS_MATCH_END = (ID_BASE_OUTER_SYSTEM + 0x0110)             # 竞技场结束
    MSG_SYS_MATCH_QUIT = (ID_BASE_OUTER_SYSTEM + 0x0111)            # 竞技场准备时取消
    MSG_SYS_MATCH_GET_STATUS = (ID_BASE_OUTER_SYSTEM + 0x0112)      # 竞技场获取竞技场状态

    MSG_SYS_UPDATE_ACTIVITY_CONF = (ID_BASE_OUTER_SYSTEM + 0x0113)  # 后台修改活动数据，通知前端请求活动数据

    MSG_SYS_NEW_ACTIVITY_VIP_RECEIVE = (ID_BASE_OUTER_SYSTEM + 0x0114)  # vip活动领取
    MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_DATA = (ID_BASE_OUTER_SYSTEM + 0x0115)  # 存钱窝数据
    MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_RECEIVE = (ID_BASE_OUTER_SYSTEM + 0x0116)  # 存钱窝领取

    MSG_SYS_SHOP_BROADCAST_RECORD_LIST = ID_BASE_OUTER_SYSTEM + 0x0117 # 商城公告推送列表
    MSG_SYS_SHOP_BROADCAST_RECORD_SINGLE = ID_BASE_OUTER_SYSTEM + 0x0118 # 商城公告推送单个

    MSG_SYS_DROP_COUPON_SLIDER = (ID_BASE_OUTER_SYSTEM + 0x0119)  # 掉券进度

    MSG_SYS_SHOP_TIPS_SEND = (ID_BASE_OUTER_SYSTEM + 0x0127)        # 商城tips获取（回应）
    MSG_SYS_SHOP_TIPS_NOTICE = (ID_BASE_OUTER_SYSTEM + 0x0128)      # 商城tips通知（下发通知修改）

    MSG_SYS_ACTIVITY_SHAKE_GET = (ID_BASE_OUTER_SYSTEM + 0x0129)  # 获取开心摇一摇的金币数
    MSG_SYS_ACTIVITY_SHAKE_RECV = (ID_BASE_OUTER_SYSTEM + 0x012A)  # 领取开心摇一摇的金币数

    MSG_SYS_UPDATE_PICTURE = (ID_BASE_OUTER_SYSTEM + 0x012B)       # 客服端请求图片
    MSG_SYS_UPDATE_MATCH_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x012C)   # 更新竞技场的配置
    MSG_SYS_GET_GAME_OPEN = (ID_BASE_OUTER_SYSTEM + 0x012D)         # 客户端获取小游戏开关数据

    MSG_SYS_RICH_MAN = (ID_BASE_OUTER_SYSTEM + 0x012E)         # 大富翁消息总id

    MSG_SYS_UPDATE_DAILY_INFO = (ID_BASE_OUTER_SYSTEM + 0x012F)    # 通知玩家拉取玩家信息
    MSG_SYS_ACTIVITY_GIFT_BOX_CAN = (ID_BASE_OUTER_SYSTEM + 0x0130)  # 玩家能不能购买活动礼包
    MSG_SYS_UPDATE_ACTIVITY_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x0131)  # 后台更新老活动配置
    MSG_SYS_UPDATE_POINT_SHOP_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x0132)  # 后台更新积分商城数据
    MSG_SYS_GET_POINT_SHOP_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x0133)  # 前端获取积分商城配置数据
    MSG_SYS_GET_POINT_SHOP_EXCHANGE = (ID_BASE_OUTER_SYSTEM + 0x0134)  # 前端获取积分商城兑换数据

    MSG_SYS_ACTIVITY_SMASH_EGG_START = (ID_BASE_OUTER_SYSTEM + 0x0135)  # 砸金蛋 开始
    MSG_SYS_ACTIVITY_SMASH_EGG_ACTION = (ID_BASE_OUTER_SYSTEM + 0x0136)  # 砸金蛋 砸蛋
    MSG_SYS_ACTIVITY_SMASH_EGG_REWARD = (ID_BASE_OUTER_SYSTEM + 0x0137)  # 砸金蛋 奖励

    MSG_SYS_SEND_AUTO_SHOT_TIME = (ID_BASE_OUTER_SYSTEM + 0x0138)  # 自动开炮剩余时间

    MSG_SYS_ACTIVE_USER_COUNT = (ID_BASE_OUTER_SYSTEM + 0x0139)    # 获取一小时内玩家的在线人数（只要在线过就算）
    MSG_SYS_BURYING_POINT = (ID_BASE_OUTER_SYSTEM + 0x013A)        # 前端埋点信息的提交

    MSG_SYS_DRAGON_BOAT_RECV = (ID_BASE_OUTER_SYSTEM + 0x013B)     # 龙舟领取奖励
    MSG_SYS_SMART_GAME_TOKEN = (ID_BASE_OUTER_SYSTEM + 0x013C)     # 获取小游戏的token
    MSG_SYS_SMART_GAME_LEAVE = (ID_BASE_OUTER_SYSTEM + 0x013D)     # 退出小游戏
    MSG_SYS_SHOP_GIFT_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x013E)     # 礼包商城获取配置
    MSG_SYS_SHOP_GIFT_BUY = (ID_BASE_OUTER_SYSTEM + 0x013F)        # 礼包商城购买

    MSG_SYS_MAIL_DELETE_RECORD = (ID_BASE_OUTER_SYSTEM + 0x0140)   # 邮件删除记录

    MSG_SYS_NEW_MONTH_CARD_BUY = (ID_BASE_OUTER_SYSTEM + 0x0141)  # 购买新月卡
    MSG_SYS_NEW_MONTH_CARD_RECV = (ID_BASE_OUTER_SYSTEM + 0x0142)  # 领取新月卡

    MSG_SYS_NOTICE_CLIENT_GIFT_SHOP = (ID_BASE_OUTER_SYSTEM + 0x0143)  # 通知客户端刷新礼包商城

    MSG_SYS_ACTIVITY_TOTAL_PAY_RECV = (ID_BASE_OUTER_SYSTEM + 0x0144)  # 领取累计充值奖励

    MSG_SYS_MATCH_ENTRY = (ID_BASE_OUTER_SYSTEM + 0x1F00)          # 比赛概览
    MSG_SYS_MATCH_RESULT = (ID_BASE_OUTER_SYSTEM + 0x1F01)         # 比赛结算
    MSG_SYS_MATCH_EVENT = (ID_BASE_OUTER_SYSTEM + 0x1F02)          # 比赛事件(比赛开始， 比赛结束)
    MSG_SYS_MATCH_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0x1F03)      # 比赛任务

    MSG_SYS_TARGET_RANGE = (ID_BASE_OUTER_SYSTEM + 0x1F05)         # 各个靶场

    MSG_SYS_SPECIAL_RED_ENVELOPE = (ID_BASE_OUTER_SYSTEM + 0x1F06)  # 特殊红包
    MSG_SYS_OPEN_SPECIAL_ENVELOPE = (ID_BASE_OUTER_SYSTEM + 0x1F07)  # 打开特殊红包
    MSG_SYS_SPECIAL_ENVELOPE_RECORD = (ID_BASE_OUTER_SYSTEM + 0x1F08)  # 特殊红包记录

    MSG_SYS_SHOP_REWARD_INFO = (ID_BASE_OUTER_SYSTEM + 0x1F09)     # 商城购买鸟蛋钻石道具下发数据结果

    MSG_SYS_MONTH_REWARD = (ID_BASE_OUTER_SYSTEM + 0x1F10)         # 商城购买鸟蛋钻石道具下发数据结果
    MSG_SYS_WEAPON_EXPIRE = (ID_BASE_OUTER_SYSTEM + 0x1F11)        # 限时炮台过期协议

    MSG_SYS_UPDATE_SHOP_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x1F13)    # 更新商城配置
    MSG_SYS_SWITCH_SHOP = (ID_BASE_OUTER_SYSTEM + 0x1F15)  # 限时商城开关

    MSG_SYS_FILL_POINT = (ID_BASE_OUTER_SYSTEM + 0x1F16)  # 填分修改

    MSG_SYS_SPECIA_RED_PACKET = (ID_BASE_OUTER_SYSTEM + 0x1F17)  # 后台发送全服红包

    MSG_SYS_RAFFLE_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x1F14)  # 抽奖配置

    MSG_SYS_POOL_LOOP_WAVE = (ID_BASE_OUTER_SYSTEM + 0x1F18)  # 池子循环波动处理
    MSG_SYS_PLAYER_PROTECTED = (ID_BASE_OUTER_SYSTEM + 0x1F19)  # 玩家游戏体验保护机制



    ID_BASE_MATCH_SYSTEM_END = 0x00008FFF

    # 服务器与客户端逻辑消息
    ID_BASE_OUTER_GAME = 0x00010000
    ID_BASE_OUTER_GAME_END = 0x0001FFFF

    # 小游戏消息区段
    ID_BASE_MINI_GAME = 0x00020000
    ID_BASE_MINI_GAME_END = 0x0002FFFF

    @classmethod
    def to_inner(cls, cmd):
        return cmd | cls.INNER_FLAG

    @classmethod
    def to_outer(cls, cmd):
        return cmd & cls.MSG_MASK

    @classmethod
    def is_inner(cls, cmd):
        return bool(cmd & cls.INNER_FLAG)

    @classmethod
    def is_game_server(cls, cmd):
        # 游戏逻辑
        cmd &= 0xF0FFFFFF
        if cls.ID_BASE_OUTER_GAME < cmd < cls.ID_BASE_OUTER_GAME_END:
            return True
        # 游戏框架
        if cls.MSG_SYS_JOIN_TABLE <= cmd <= cls.MSG_SYS_TIMEOUT:
            return True
        return False

    @classmethod
    def is_mini_game(cls, cmd):
        cmd &= 0xF0FFFFFF
        return cls.ID_BASE_MINI_GAME < cmd < cls.ID_BASE_MINI_GAME_END


class FlagType(object):
    flag_type_client = 0
    flag_type_game = 1
    flag_type_connect = 2
    flag_type_ai = 3
    flag_type_account = 4
    flag_type_quick = 5
    flag_type_entity = 6
    flag_type_match = 7
    flag_type_stat = 8
    flag_type_sdk = 9
    flag_type_http = 10
    flag_type_shell = 11
    flag_type_proxy = 12

    __cache_map = {}

    @classmethod
    def trans_server_type(cls, server_type):
        if not cls.__cache_map:
            cls.__make_cache()
        return cls.__cache_map.get(server_type, None)

    @classmethod
    def __make_cache(cls):
        for attr, v in cls.__dict__.iteritems():
            if attr.startswith('flag_type_'):
                cls.__cache_map[attr[len('flag_type_'):]] = v
                cls.__cache_map[v] = attr[len('flag_type_'):]


class Const(object):
    chip_operate_noop = 0
    chip_operate_zero = 1

    run_mode_online = 1
    run_mode_simulation = 2
    run_mode_test = 3
    run_mode_audit = 4

    data_type_str = 0
    data_type_json = 1
    data_type_int = 2
    data_type_float = 3


class Enum(object):
    # 登陆
    login_success = 0                    # 成功
    login_failed_unknown = -1            # 未知错误
    login_failed_low_version = -2        # client版本过低, 必须升级
    login_failed_forbidden = -3          # 账号封停
    login_failed_freeze = -4             # 账号冻结
    login_failed_id = -5                 # 错误的user id
    login_failed_key = -6                # 错误的session key
    login_failed_multi = -7              # 多点登陆

    # 加入桌子
    join_table_success = 0               # 成功
    join_table_reconnect = -1            # 断线重连
    join_table_failed_unknown = -2       # 未知错误
    join_table_failed_id = -3            # 错误的table id
    join_table_failed_multi = -4         # 在其他桌子未离开
    join_table_failed_getout = -5        # 上局逃跑，游戏未结束

    # 旁观者加入桌子
    viewer_join_table_success = 0            # 成功
    viewer_join_table_failed_unknown = -1    # 未知错误
    viewer_join_table_failed_id = -2         # 错误的table id
    viewer_join_table_failed_multi = -3      # 在其他桌子未离开

    # 离开桌子
    leave_table_success = 0                  # 成功
    leave_table_failed_unknown = -1          # 未知错误
    leave_table_failed_id = -2               # 错误的table id
    leave_table_failed_playing = -3          # 游戏中

    # 强制退出
    force_quit_success = 0                   # 成功
    force_quit_failed_unknown = -1           # 未知错误
    force_quit_failed_id = -2                # 错误的table id

    # 旁观者退出
    viewer_leave_table_success = 0           # 成功
    viewer_leave_table_failed_unknown = -1   # 未知错误
    viewer_leave_table_failed_id = -2        # 错误的table id

    # 广播
    broadcast_success = 0                    # 成功
    broadcast_failed_unknown = -1            # 未知错误
    broadcast_failed_id = -2                 # 错误的table id

    # 刷新
    flush_success = 0                        # 成功
    flush_failed_unknown = -1                # 未知错误
    flush_failed_id = -2                     # 错误的table id

    # 托管
    trustee_success = 0                      # 成功
    trustee_failed_unknown = -1              # 未知错误
    trustee_failed_id = -2                   # 错误的table id

    # 超时
    timeout_success = 0                      # 成功
    timeout_failed_unknown = -1              # 未知错误
    timeout_failed_id = -2                   # 错误的table id

    # 坐下
    sit_down_success = 0                     # 成功
    sit_down_failed_unknown = -1             # 未知错误
    sit_down_failed_id = -2                  # 错误的table id

    # 准备
    ready_success = 0                        # 成功
    ready_failed_unknown = -1                # 未知错误
    ready_failed_id = -2                     # 错误的table id

    # 快速开始
    quick_start_success = 0
    quick_start_failed_unknown = -1
    quick_start_failed_chip_small = -2
    quick_start_failed_chip_big = -3
    quick_start_failed_multi = -4

    # 重连
    reconnect_success = 0
    reconnect_failed_unknown = -1
    reconnect_failed_id = -2
    reconnect_failed_state = -3

    # 桌子事件
    table_event_login = 0                        # 玩家登陆
    table_event_join_table = 1                   # 玩家加入桌子
    table_event_sit_down = 2                     # 玩家坐下
    table_event_stand_up = 3                     # 玩家站起
    table_event_ready = 4                        # 玩家ready
    table_event_cancel_ready = 5                 # 玩家取消ready
    table_event_leave_table = 6                  # 玩家离开桌子
    table_event_force_quit = 7                   # 玩家强退
    table_event_viewer_join_table = 8            # 旁观者进入
    table_event_viewer_leave_table = 9           # 旁观者退出
    table_event_kick_off = 10                    # 玩家被踢出
    table_event_offline = 11                     # 玩家断线
    table_event_reconnect = 12                   # 断线重连
    table_event_game_start = 13                  # 游戏开始
    table_event_game_end = 14                    # 游戏结束
    table_event_game_info = 15                   # 玩家gameinfo改变
    table_event_user_info = 16                   # 玩家userinfo改变
    table_event_table_info = 17                  # tableinfo改变
    table_event_broadcast = 18                   # 广播
    table_event_trustee = 19                     # 托管
    table_event_cancel_trustee = 20              # 取消托管
    table_event_join_all = 21                    # 桌子满
    table_event_close = 22                       # 房间关闭

    # 玩家状态
    user_state_unknown = 0            # 未知
    user_state_getout = 1             # 离开了
    user_state_free = 2               # 在房间站立
    user_state_sit = 3                # 坐在椅子上
    user_state_ready = 4              # 同意游戏开始
    user_state_playing = 5            # 正在玩
    user_state_offline = 6            # 断线等待续玩
    user_state_lookon = 7             # 旁观
    user_state_trustee = 8            # 托管
    user_state_wait = 9               # 等待
    user_state_lose = 10              # 已经输了

    # redis中玩家状态
    location_status_unknown = -1
    location_status_dispatch = 0       # 已分配
    location_status_join = 1           # game已确认
    location_status_playing = 2        # 游戏中

    # redis中桌子状态
    table_status_unknown = -1
    table_status_free = 0              # 分配玩家
    table_status_robot = 1             # 准许投放机器人
    table_status_playing = 2           # 游戏中, 禁止投放机器人

    # 玩家身份
    identity_type_unknown = 0
    identity_type_player = 1
    identity_type_viewer = 2
    identity_type_robot = 3

    # 比赛事件
    match_event_start_apply = 1         # 开始报名
    match_event_start = 2               # 比赛开始
    match_event_end_apply = 3           # 结束报名
    match_event_end = 4                 # 比赛结束

    match_status_ready = 1              # 竞技场报名
    match_status_enter = 2              # 竞技场人员到齐，等待创建房间
    match_status_start = 3              # 竞技场创建房间，进入房间
    match_status_end = 4                # 竞技场结束

    match_table_start = 1               # 房间里面已经有人了
    match_table_end = 2                 # 房间的人全部离开了