import json
import collections
import copy

class OVSRuleTree():
    def __init__(self):
        self.ovs_rule = ''
        self.rule_tree = []
        self.record_rule = []

    def clear(self):
        self.ovs_rule = ''
        self.rule_tree = []
        self.record_rule = []

    def build_rule_tree(self,ovs_rule):
        self.ovs_rule = json.loads(ovs_rule)

        port_information = []
        dpid = None

        for i in range(0,len(self.ovs_rule)):
            #delete uneccessary informations
            if 'dpid' in self.ovs_rule[i].keys():
                if dpid is None:
                    dpid = self.ovs_rule[i]['dpid']
                del self.ovs_rule[i]['dpid']        
            if 'cookie' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['cookie']        
            if 'duration' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['duration']        
            if 'n_packets' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['n_packets']        
            if 'n_bytes' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['n_bytes']        
            if 'idle_age' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['idle_age']        
            if 'hard_age' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['hard_age']        
            if 'priority' in self.ovs_rule[i].keys():
                del self.ovs_rule[i]['priority']      

        self.build(self.ovs_rule)

        #use rule_tree to form list which content is dict
        #dict's key is (in_port & output) 
        in_port = None
        output = None    
        for rule_chain in self.rule_tree:
            for rule in rule_chain:
                if in_port is None:
                    if 'in_port' in rule.keys():
                        in_port = str(rule['in_port'])
                    else:
                        in_port = None
                if output is None:
                    if 'actions' in rule.keys():
                        if 'output' in rule['actions'].keys():
                            output = str(rule['actions']['output'])
                        elif 'LOCAL' in rule['actions'].keys():
                            output = 'LOCAL'
                        elif 'NORMAL' in rule['actions'].keys():
                            output = 'NORMAL'
                        elif 'FLOOD' in rule['actions'].keys():
                            output = 'FLOOD'
                        elif 'CONTROLLER' in rule['actions'].keys():
                            output = str('CONTROLLER('+rule['actions']['CONTROLLER']+')')
                        else:
                            output = None
            port_information.append({(in_port,output):rule_chain})
            in_port = None
            output = None
        
        tmp = {}
        for port in port_information:
            for each_rule in port[port.keys()[0]]:
                if 'table' in each_rule.keys():
                    del each_rule['table']
                if 'actions' in each_rule.keys():
                    if 'resubmit' in each_rule['actions'].keys():
                        del each_rule['actions']['resubmit']
                    if 'learn' in each_rule['actions'].keys():
                        del each_rule['actions']['learn']
                    if 'load' in each_rule['actions'].keys():
                        del each_rule['actions']['load']
                    if len(each_rule['actions']) == 0:
                        del each_rule['actions']
                tmp.update(each_rule)
            port[port.keys()[0]] = copy.deepcopy(tmp)
            tmp = {}
        
        for port in port_information:
            for key in port[port.keys()[0]].keys():
                if key == 'actions':
                    for k in port[port.keys()[0]]['actions'].keys():
                        port[port.keys()[0]]['actions'][str(k)] = str(port[port.keys()[0]]['actions'].pop(k))
                    port[port.keys()[0]][str(key)] = port[port.keys()[0]].pop(key)
                else:
                   port[port.keys()[0]][str(key)] = str(port[port.keys()[0]].pop(key))

        rtn = {}
        rtn[str(dpid)] = port_information

        return rtn
                        
        
    def table_member(self, ovs_rule,table_no):
        t_member = []
        for rule in ovs_rule:
            if 'table' in rule.keys():
                if rule['table'] == table_no:
                    t_member.append(rule)
        return t_member

    def build(self, rule_to_be_build):
        for rule in rule_to_be_build:
            if 'in_port' in rule.keys():
                self.parse_rule(rule)
            else:
                self.record_rule.append(rule)
                self.rule_tree.append(copy.deepcopy(self.record_rule))
                self.record_rule.pop()

    def parse_rule(self, rule_to_be_expand):
        if isinstance(rule_to_be_expand,list):#check one rule or multiple rule
            for rule in rule_to_be_expand:
                if 'actions' in rule.keys():
                    if 'resubmit' in rule['actions'].keys():
                        self.record_rule.append(rule)
                        self.parse_rule(self.table_member(self.ovs_rule,int(rule['actions']['resubmit'][2:-1])))
                        self.record_rule.pop()
                    else:
                        self.record_rule.append(rule)
                        self.rule_tree.append(copy.deepcopy(self.record_rule))
                        self.record_rule.pop()
            return 
        else:
            rule = rule_to_be_expand
            if 'actions' in rule.keys():
                if 'resubmit' in rule['actions'].keys():
                    self.record_rule.append(rule)
                    self.parse_rule(self.table_member(self.ovs_rule,int(rule['actions']['resubmit'][2:-1])))
                    self.record_rule.pop()
                else:
                    self.record_rule.append(rule)
                    self.rule_tree.append(copy.deepcopy(self.record_rule))
                    self.record_rule.pop()
                    return
