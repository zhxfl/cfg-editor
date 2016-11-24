#coding: utf-8
g_dState = {
    0:u"start",
    1:u"BornState(出生状态)",
    2:u"NormalState(非战斗状态)",
    3:u"IdleState(Idle状态)",
    4:u"ReturnState（返回状态)",
    5:u"FightState(战斗状态)",
    6:u"ControlState(受控状态)",
    7:u"DeadState(死亡状态)",
    8:u"end"
}

g_dCondition = {
    0 : u"",
    1 : u"new",
    2 : u"eGMSG_CreateCompleted,創建完成",
    3 : u"close_idle, 关闭了IDLE开关时",
    4 : u"open_idle, 开启了IDLE开关时",
    5 : u"eGMSG_DestroyMySelf,无法被玩家看到",
    6 : u"eGMSG_InitMySelf,被玩家看到",
    7 : u"eGMSG_GetControl, 被强控",
    8 : u"eGMSG_OnDamage, 受到损害",
    9 : u"eGMSG_FoundTarget, 发现可攻击目标",
    10: u"eGMSG_MoveEnded, 到达返回点",
    11: u"eGMSG_OnDead, 死亡",
    12: u"eGMSG_OnTargetLost, 所有可攻击目标丢失",
    13: u"eGMSG_OnDead, 死亡",
    14: u"eGMSG_DisControl, 强制结束"
}