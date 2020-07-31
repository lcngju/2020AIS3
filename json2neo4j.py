"""
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
"""

import json
from neo4j import GraphDatabase

def cypherexecuter(driver, cypher):

    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run(cypher)
    session.close()


def CreateR(A, B, Relation):
    cypher_R = ["(%s)-[:%s]->(%s)"%(A,Relation,b) for b in B]
    cypher_R = "CREATE " + ','.join(cypher_R)
    
    return cypher_R
    

def CreatNode(node_dict, name):
    type_ = node_dict['type'] 
    mac = node_dict['mac'] 
    ip = node_dict['ip'] 
    ports = node_dict['ports']
    
    
    cypher_create = "CREATE (%s: %s { type: '%s', mac: '%s', ip: '%s', port: %s})" %(name, type_, type_, mac, ip, ports)
    
    subnets = []
    for subnet in node_dict.keys():
        subnets.append(subnet)

    cypher_R = CreateR(name, subnets, node_dict[subnet]['ip'])
    
    return cypher_create, cypher_R


if __name__ == '__main__':
    jfile = open('test.json')
    text = json.load(jfile)
     
    
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test"))
    

"""
def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])
        
        

with driver.session() as session:
    session.write_transaction(add_friend, "Arthur", "Guinevere")
    session.write_transaction(add_friend, "Arthur", "Lancelot")
    session.write_transaction(add_friend, "Arthur", "Merlin")
    session.read_transaction(print_friends, "Arthur")
    
"""  
    
    
    
    



jfile.close()






