-- KEYS: [uid, gid, vid, deal_type, args]
-- ARGV: []
-- ACK:  []
-- deal_type 1 add 人数上限 2 deal_apply (1 同意 最大人数 -1拒绝) 3 add_apply 4 exit
-- tonumber(KEYS[5])

function table.getn(x)
    local ret = 0
    for i in pairs(x) do
        ret=ret+1
    end
    return ret
end

local function add(key, uid, num_max)
    local members = redis.call('hget', key, 'members')
    members = cjson.decode(members)

    local len = table.getn(members)
    if len >= num_max then
        return {0, 1}
    end
    members[uid] = 5
    members = cjson.encode(members)
    redis.call('hset', key, 'members', members)
    return {1}
end

local function deal_apply(key, uid, arg1)
    local res = redis.call('hmget', key, 'members', 'applys')
    local members = res[1]
    local applys = res[2]
    applys = cjson.decode(applys)
    members = cjson.decode(members)

    if arg1 >= 0 then
        local len = table.getn(members)
        if len >= arg1 then
            return {0, 1}
        end
    end

    local is_in = false
    for k, v in pairs(applys) do
        if v == uid then
            table.remove(applys, k)
            is_in = true
            break
       end
    end
    if not is_in then
        return {0, 1}
    end

    applys = cjson.encode(applys)
    if arg1 == -1 then
        redis.call('hmset', key, 'applys', applys)
        return {1}
    end

    members[uid] = 5
    members = cjson.encode(members)
    redis.call('hmset', key, 'members', members, 'applys', applys)
    return {1}
end

local function add_apply(key, uid)
    local data = redis.call('hget', key, 'applys')
    local data = cjson.decode(data)
    for k, v in pairs(data) do
        if v == uid then
            return {1}
       end
    end
    local len = table.getn(data)
    if len >= 20 then
        table.remove(data, 1)
    end
    table.insert(data, uid)
    data = cjson.encode(data)
    redis.call('hset', key, 'applys', data)
    return {1}
end

local function v_exit(key, uid)
    local data = redis.call('hget', key, 'members')
    local data = cjson.decode(data)
    for k, v in pairs(data) do
        if k == uid then
            data[k] = nil
            break
       end
    end

    data = cjson.encode(data)
    redis.call('hset', key, 'members', data)
    return {1}
end

local function village(uid, gid, vid, deal_type, args)
    local key = 'village:' .. gid .. ':' .. vid
    if deal_type == 'deal_apply' then
        return deal_apply(key, uid, args)
    elseif deal_type == 'add' then
        return add(key, uid, args)
    elseif deal_type == 'add_apply' then
        return add_apply(key, uid)
    elseif deal_type == 'exit' then
        return v_exit(key, uid)
    else
        return
    end
end

return village(KEYS[1], KEYS[2], KEYS[3], KEYS[4], tonumber(KEYS[5]))
