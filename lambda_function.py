import json
import redis
import logging
from multiprocessing import Process

#src = redis.cluster.RedisCluster(host='<ElastiCache Endpoint>',port=6379,decode_responses=True)

dst = redis.cluster.RedisCluster(host='<ElastiCache Endpoint>',port=6379,decode_responses=True)
idc=redis.Redis(host='172.16.0.60',port=6379,decode_responses=True,password='test1234')



def migration(keys):

    for key in keys:
        ttl = idc.ttl(str(key));
        if ttl < 0: # required as you can't create keys witn ttl -1, for no ttl , you can give 0 value.
            print("KEY {0} has no TTL".format(str(key)))
            ttl = 0
        else:
            ttl *= 1000
        #print('dump {0} and ttl is {1}'.format(str(key),ttl))
        value =idc.dump(str(key))
        
        #print('restore {0} and ttl is {1}'.format(str(key),ttl))
        dst.restore(str(key),ttl,value,replace=True)

def lambda_handler(event, context):
    #data migrations cluster to cluster
    cur = 0
    key_cnt=0
    flag=0;
    
    #using multiprocess
    #processes = []
    
    while True :
        
        #aws cluster scan
        #scans=src.scan(cursor=cur,count=1000)
        #keys=scans[-1]
        #cur=list(scans[0].values())[0]
        
        #idc redis scan
        scans=idc.scan(cursor=cur,count=1000)
        keys=scans[-1]
        cur=scans[0]
        migration(keys)
        
        
        #using multiprocess
        #process = Process(target=migration,args=([keys]));
        
        
        #data mig
        migration(keys)
        flag+=1;
        key_cnt+=len(keys)
        print("last cursor is {0}".format(cur))
        
        if cur == 0:
            break;
        elif flag >= 1:
            break;
    
    print("total key count is {0}".format(key_cnt))
    
    
    '''
    print(process)
    
    for process in processes:
        print("Start Migrations...")
        process.start();
    
    for process in processes:
        print("finished process")
        process.join();

    '''
    return {
        'LastCursor': cur
    }
