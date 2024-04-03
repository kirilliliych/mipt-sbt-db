import redis
import time
import json

with open('large-file.json') as file:
    data = json.load(file)

db = redis.Redis(
    host='localhost',
    port=6380
)

MEASURE_TIMES = 12

# ADD
print("ADD")
# string
result_avg = 0
for i in range(MEASURE_TIMES):
    start = time.time()
    db.set('json_string' + str(i), json.dumps(data))
    end = time.time()
    result_avg += end - start
print("add json as string to redis: ", result_avg / MEASURE_TIMES)

# hset
result_avg = 0
for i in range(MEASURE_TIMES):
    start = time.time()
    db.hset('json_hset' + str(i), 'elem' + str(i), json.dumps(data))
    end = time.time()
    result_avg += end - start
print("add json as hset to redis: ", result_avg / MEASURE_TIMES)

# zset
result_avg = 0
zset_count = []
for i in range(MEASURE_TIMES):
    zset_data = {}
    for num, elem in enumerate(data):
        zset_data[json.dumps(elem)] = num
    start = time.time()
    zset_count_elem = db.zadd('json_zset' + str(i), zset_data)
    end = time.time()
    zset_count.append(zset_count_elem)
    result_avg += end - start
print("add json as zset to redis: ", result_avg / MEASURE_TIMES)

# list
result_avg = 0
list_count = []
for i in range(MEASURE_TIMES):
    list_data = []
    for elem in data:
        list_data.append(json.dumps(elem))
    start = time.time()
    list_count_elem = (db.lpush('json_list' + str(i), *list_data))
    end = time.time()
    list_count.append(list_count_elem)
    result_avg += end - start
print("add json as list to redis: ", result_avg / MEASURE_TIMES)


# READ
print("READ")
# string
result_avg = 0
for i in range (MEASURE_TIMES):
    start = time.time()
    read_json_string = db.get('json_string' + str(i))
    end = time.time()
    result_avg += end - start
print("get string from redis: ", result_avg / MEASURE_TIMES)

# hset
result_avg = 0
for i in range (MEASURE_TIMES):
    start = time.time()
    read_json_hset = db.hget('json_hset' + str(i), 'elem' + str(i))
    end = time.time()
    result_avg += end - start
print("get hset from redis: ", result_avg / MEASURE_TIMES)

# zset
result_avg = 0
for i in range (MEASURE_TIMES):
    start = time.time()
    read_json_zset = db.zrange('json_zset' + str(i), 0, zset_count[i])
    end = time.time()
    result_avg += end - start
print("get zset from redis: ", result_avg / MEASURE_TIMES)

# list
result_avg = 0
for i in range (MEASURE_TIMES):
    start = time.time()
    read_json_list = db.lrange('json_list' + str(i), 0, list_count[i])
    end = time.time()
    result_avg += end - start
print("get list from redis: ", result_avg / MEASURE_TIMES)

db.flushall()
