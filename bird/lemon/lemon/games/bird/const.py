#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from framework.entity import const


class Message(const.Message):
    BIRD_MSG_BOARD_INFO = const.Message.ID_BASE_OUTER_GAME + 0x01            # 桌面信息, 游戏初始化数据
    BIRD_MSG_SHOT_BULLET = const.Message.ID_BASE_OUTER_GAME + 0x02           # 玩家射击
    BIRD_MSG_MOVE_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x03           # 玩家移动炮筒
    BIRD_MSG_HIT_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x04              # 玩家炮弹击中鸟
    BIRD_MSG_CATCH_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x05            # 玩家捕获鸟
    BIRD_MSG_NEXT_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x06            # 下一个场景
    BIRD_MSG_UNLOCK_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x07         # 解锁炮筒
    BIRD_MSG_SWITCH_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x08         # 改变炮筒
    BIRD_MSG_SKILL_LOCK = const.Message.ID_BASE_OUTER_GAME + 0x09            # 锁定攻击
    BIRD_MSG_SKILL_FREEZE = const.Message.ID_BASE_OUTER_GAME + 0x0A          # 冰冻
    BIRD_MSG_SKILL_VIOLENT = const.Message.ID_BASE_OUTER_GAME + 0x0B         # 狂暴
    BIRD_MSG_SKILL_SUPER_WEAPON = const.Message.ID_BASE_OUTER_GAME + 0x0C    # 超级武器
    BIRD_MSG_SKILL_PORTAL = const.Message.ID_BASE_OUTER_GAME + 0x0D          # 神秘传送门
    BIRD_MSG_LOCK_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x15             # 锁定攻击
    BIRD_MSG_EXP_UPGRADE = const.Message.ID_BASE_OUTER_GAME + 0x1F           # exp等级升级
    BIRD_MSG_DELTA_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x20           # 场景增量内容
    BIRD_MSG_BANKRUPT = const.Message.ID_BASE_OUTER_GAME + 0x21              # 破产
    BIRD_MSG_REPORT_BIRDS = const.Message.ID_BASE_OUTER_GAME + 0x22          # 上报辐射到的鸟
    BIRD_MSG_LED = const.Message.ID_BASE_OUTER_GAME + 0x23                   # 游戏内广播
    BIRD_MSG_CALL_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x24             # 召唤鸟
    BIRD_MSG_BIRD_ATTACK = const.Message.ID_BASE_OUTER_GAME + 0x25           # 小红龙攻击
    BIRD_MSG_RED_DRAGON_TASK_END = const.Message.ID_BASE_OUTER_GAME + 0x26   # 红龙任务结束
    BIRD_MSG_RANK_CHANGE = const.Message.ID_BASE_OUTER_GAME + 0x27           # 赏金任务信息变化
    BIRD_MSG_BOUNTY_END = const.Message.ID_BASE_OUTER_GAME + 0x28            # 赏金任务结束
    BIRD_MSG_COOK_TASK = const.Message.ID_BASE_OUTER_GAME + 0x29             # 厨师悬赏任务
    BIRD_MSG_COOK_TASK_CHANGE = const.Message.ID_BASE_OUTER_GAME + 0x2A      # 厨师悬赏任务变换
    BIRD_MSG_COOK_TASK_END = const.Message.ID_BASE_OUTER_GAME + 0x2B         # 厨师悬赏任务结束
    BIRD_MSG_TASK_FINISH = const.Message.ID_BASE_OUTER_GAME + 0x2C           # 任务完成: 首次达到2400积分
    BIRD_MSG_RED_DRAGON_COME = const.Message.ID_BASE_OUTER_GAME + 0x2D       # 红龙出现
    BIRD_MSG_NEW_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x2E              # 动态产生鸟
    MSG_SYS_ONLINE_REWARD_INFO = const.Message.ID_BASE_OUTER_GAME + 0x2F     # 在线奖励
    MSG_SYS_GET_ONLINE_REWARD = const.Message.ID_BASE_OUTER_GAME + 0x30      # 在线奖励
    BIRD_MSG_WORLD_BOSS_CALL = const.Message.ID_BASE_OUTER_GAME + 0x32       # world boss 入场退场
    BIRD_MSG_WORLD_BOSS_REWARD = const.Message.ID_BASE_OUTER_GAME + 0x33     # world boss 掉落物品
    BIRD_MSG_WORLD_BOSS_REFRESH = const.Message.ID_BASE_OUTER_GAME + 0x34     # world boss 倒计时
    BIRD_MSG_NOTIFY_BLOOD = const.Message.ID_BASE_OUTER_GAME + 0x35     # world boss 倒计时

    BIRD_MSG_RED_ENVELOPE = const.Message.ID_BASE_OUTER_GAME + 0x43          #红包信息
    BIRD_MSG_RANDOM_RED_ENVELOPE = const.Message.ID_BASE_OUTER_GAME + 0x44   # 打开普通红包
    BIRD_MSG_RED_ENVELOPE_RECORD = const.Message.ID_BASE_OUTER_GAME + 0x45   # 普通红包记录

    # 炮台特性处理
    BIRD_MSG_WEAPON_FREEZE = const.Message.ID_BASE_OUTER_GAME + 0x46            # 炮台冰冻特性
    BIRD_MSG_WEAPON_STOP = const.Message.ID_BASE_OUTER_GAME + 0x47              # 炮台定身特性
    BIRD_MSG_WEAPON_KILL = const.Message.ID_BASE_OUTER_GAME + 0x48              # 炮台必杀特性
    BIRD_MSG_WEAPON_HOLE = const.Message.ID_BASE_OUTER_GAME + 0x49              # 炮台黑洞特性
    BIRD_MSG_WEAPON_LIGHTNING = const.Message.ID_BASE_OUTER_GAME + 0x50         # 炮台闪电特性

    BIRD_MSG_WEAPON_REPORT_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x51       # 炮台辐射怪
    BIRD_MSG_WEAPON_LIGHT =  const.Message.ID_BASE_OUTER_GAME + 0x52            # 极光炮打中怪

    BIRD_MSG_TABLE_UP_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x53          # 房间内升级炮

    BIRD_MSG_SKILL_SUPER_WEAPON_READY = const.Message.ID_BASE_OUTER_GAME + 0x54          # 超级武器准备
    BIRD_MSG_SEND_EMOJI = const.Message.ID_BASE_OUTER_GAME + 0x55          # 表情的发送
    BIRD_MSG_SEND_SHAKE_START = const.Message.ID_BASE_OUTER_GAME + 0x56         # 开心摇一摇开始（服务器通知）
    BIRD_MSG_SEND_SHAKE_END = const.Message.ID_BASE_OUTER_GAME + 0x57           # 开心摇一摇结束（结果上发给服务器）
    BIRD_MSG_CLOSE_SHAKE = const.Message.ID_BASE_OUTER_GAME + 0x58              # 开心摇一摇关闭（通知房间玩家关闭特效）

    BIRD_MSG_DRILL_KILL = const.Message.ID_BASE_OUTER_GAME + 0x59               # 击杀天元突破
    BIRD_MSG_DRILL_SHOT = const.Message.ID_BASE_OUTER_GAME + 0x5A               # 天元突破发射子弹
    BIRD_MSG_DRILL_HIT_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x5B           # 天元突破钻头击中鸟
    BIRD_MSG_DRILL_BOOM = const.Message.ID_BASE_OUTER_GAME + 0x5C               # 天元突破钻头爆炸

    BIRD_MSG_DRAGON_BOAT_KILL = const.Message.ID_BASE_OUTER_GAME + 0x5D         # 击杀龙舟怪 获得粽子
    BIRD_MSG_AUTO_SHOT_STATUS = const.Message.ID_BASE_OUTER_GAME + 0x5E         # 自动开炮的状态

class Enum(const.Enum):
    join_table_failed_error_state = 1                # 错误的状态
    join_table_failed_already_full = 2               # 人数已满
    join_table_failed_already_join = 3               # 该用户已经加入table
    join_table_failed_limit_min = 4                  # 低于最低限制
    join_table_failed_limit_max = 5                  # 高于最高限制

    sit_down_failed_error_state = 1                  # 错误的状态
    sit_down_failed_error_seat_id = 2                # 错误的seat id
    sit_down_failed_error_not_join = 3               # 用户不在桌子中
    sit_down_failed_error_identity = 4               # 用户身份错误
    sit_down_failed_not_free = 5                     # 不是free状态
    sit_down_failed_other_here = 6                   # 座位已经有人

    ready_failed_error_state = 1                     # 错误的状态
    ready_failed_error_not_join = 2                  # 用户不在桌子中
    ready_failed_error_identity = 3                  # 用户身份错误
    ready_failed_not_sit_down = 6                    # 该用户没有坐下

    leave_table_failed_not_join = 1                  # 没有加入
    leave_table_failed_error_identity = 2            # 错误的身份

    kick_reason_unknown = 0                          # 未知
    kick_reason_no_ready = 2                         # 指定时间内不ready
    kick_reason_limit_min = 3                        # 低于最低限制
    kick_reason_limit_max = 4                        # 高于最高限制

    quick_start_failed_barrel_small = 1
    quick_start_failed_barrel_big = 2
    quick_start_failed_diamond_lack = 3
    quick_start_failed_match_free = 4
    quick_start_failed_match_end = 5
    quick_start_failed_match_limit = 6
    quick_start_failed_vip_limit = 7

    game_state_free = 0                              # 未开始

    task_state_free = 0
    task_state_pre = 1
    task_state_ing = 2
    task_state_clear = 3

    play_mode_common = 1                             # 不带红龙和悬赏任务
    play_mode_task = 2                               # 带红龙和悬赏任务
    play_mode_match = 3                              # 比赛
    play_mode_vip = 4                                # VIP房间
    play_mode_village = 5                            # 公会房间

    match_state_free = 0                             # 未开始
    match_state_ing = 1                              # 进行中，需要报名
    match_state_goon = 2                             # 续完, 已经报名
    match_state_end = 3                              # 已结束

    award_level_day = 1
    award_level_week = 2
    award_level_month = 3

    award_type_direct = 1
    award_type_contact = 2

    award_state_open = 1                             # 等待领取状态
    award_state_process = 2                          # 不能直接领取的奖励, 用户提交信息后的状态
    award_state_finish = 3                           # 已发放
