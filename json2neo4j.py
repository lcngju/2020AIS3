"""
# bash

docker run \
    --name testneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
    
pip install neo4j
python3 json2neo4j.py test.json
"""

import json
import sys
from neo4j import GraphDatabase

def cypherexecuter(driver, cypher):

    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run(cypher)
    session.close()


def CreateR(A, B, R, query):

    if B == set([]): 
        return ''
    A = A.replace('-','_')
    for b in B:
        cypher_R = "(%s)-[:%s]->(%s)"%(A,R,b.replace('-','_'))
        query.append(cypher_R)
        
    return cypher_R
    

def CreateNode(node_dict, name, query):
    name = name.replace('-','_')
    type_ = node_dict['type'].replace('-','_')
    mac = node_dict['mac'] 
    ip = node_dict['ip']
    ports = node_dict.get('ports', []) + node_dict.get('port', [])
    
    cypher_create = "(%s: %s { name: '%s', type: '%s', mac: '%s', ip: '%s', ports: %s})" %(name, type_, name, type_, mac, ip, ports)
    query.append(cypher_create)
    
    subnets = set(node_dict.keys()) - set(['ip', 'mac', 'ports', 'type', 'port'])
    for subnet in subnets:
        print(subnet)
        CreateNode(node_dict[subnet], subnet, query)
            
    CreateR(name, subnets, 'subnet', query)
    
    return query


if __name__ == '__main__':
    
    
    
    jfile = open(sys.argv[1])
    text = json.load(jfile)
     
    nid = 0
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test"))
    cypher_query = CreateNode(text, 'init', [])
    cypher_query = 'CREATE '+','.join(cypher_query)
    cypherexecuter(driver, cypher_query)
    

    jfile.close()






