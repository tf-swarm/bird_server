-- KEYS: [userId, gameId, total, [tableId]]
-- ARGV: []
--  ACK: [seatid, before_cnt, after_cnt]

local function to_number(val, dft)
    local v = tonumber(val)
    if v == nil then
        v = dft
    end
    return v
end

local function get_attrs(total)
    local attrs = {}
    for i = 1, total do
        table.insert(attrs, 'seat'..tostring(i-1))
    end
    return attrs
end

local function get_player_count(key, total)
    local attrs = get_attrs(total)

    local res = redis.call('HMGET', key, unpack(attrs))
    local cnt = 0
    for i = 1, total do
        if res[i] and tonumber(res[i]) > 0 then
            cnt = cnt + 1
        end
    end
    return cnt
end

local function leave_table(uid, key, total)
    local attrs = get_attrs(total)
    local res = redis.call('HMGET', key, unpack(attrs))
    local sid = -1
    for i = 1, total do
        if res[i] == uid then
            sid = i - 1
            local field = 'seat' .. tostring(sid)
            redis.call('HSET', key, field, 0)
        end
    end
    return sid
end

local function get_user_location(uid, gid)
    local key = 'location:' .. gid .. ':' .. uid
    local res = redis.call('HMGET', key, 'room_type', 'table_id', 'play_mode', 'pwd', 'multi')
    redis.call('DEL', key)
    if not res[1] or not res[2] then
        return -1, -1, res[3]
    end
    return tonumber(res[1]), tonumber(res[2]), tonumber(res[3])
end

local function kick_off(uid, gid, total, tid)
    local rid, _tid, mode = get_user_location(uid, gid)

    if rid < 0 or _tid < 0 then
        repeat
            _tid = tid
            if _tid > 0 then
                local rid_mode = redis.call('HMGET', 'relax_table:' .. gid .. ':' .. tostring(_tid), 'room_type', 'play_mode')
                rid, mode = rid_mode[1], rid_mode[2]
                if rid then
                    rid = tonumber(rid)
                    break
                end
            end
            return { -1, -1, -1 }
        until true
    end

    local key = 'relax_table:' .. gid .. ':' .. tostring(_tid)
    local sid = leave_table(uid, key, total)

    redis.call('HDEL', key, 'pwd')

    return { 0, 0, 0 }
end

local total = tonumber(KEYS[3])
local tid = to_number(KEYS[4], 0)
return kick_off(KEYS[1], KEYS[2], total, tid)
