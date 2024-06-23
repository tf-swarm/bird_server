1. 引入event替换一些接口回调
2. 整理小游戏框架
3. 引入协程(done)
4. paramiko远程操作

## cluster:

### game.2.20001  hash
>hash

* recharge_buff
>json [[奖励组编号，{id: count}],[]]

* re_buff
>json [[奖励组编号，{id: count}],[]]

* chip_pool
>int

* shit_pool
>int


## 后台
1. 金币消耗，红龙小鸟吃钱
2. 宝盒掉落部分
3. 金币排行榜


## 遗留问题

2 脚本处理 清理chip_pool

3 脚本处理 recharge_buff 转换格式

player   def issue_rewards(self, rewards, event, **kwargs):

chip

红龙时间
