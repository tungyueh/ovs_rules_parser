from OVSRuleCommand import OVSRuleCommand
from OVSRuleYacc import OVSRuleYacc
from OVSRuleTree import OVSRuleTree

def main():

    ovs_cmd = OVSRuleCommand()
    ovs_parser = OVSRuleYacc()
    ovs_rule_tree = OVSRuleTree()

    bridge_list = ovs_cmd.get_bridge_list()

    print '-----Bridge List-----\n',bridge_list

    print '***** Start Parse Each Bridge Rule *****\n'
    
    for bridge in bridge_list:
    
        print '-----Parse [',bridge,'] Rule-----\n'

        dpid = ovs_cmd.get_dpid(bridge)

        print '-----Dpid-----\n',dpid

        ovs_rule = ovs_cmd.get_OVSRule(bridge) #put the bridge name

        print '-----OVS Rule-----\n',ovs_rule

        #--------------------------------------------

        ovs_parser.build(ovs_rule,dpid)

        ovs_rule_json = ovs_parser.msg

        ovs_parser.clear()

        print '-----OVS Rule(json)-----\n',ovs_rule_json

        #--------------------------------------------

        port_relation_information = ovs_rule_tree.build_rule_tree(ovs_rule_json)

        ovs_rule_tree.clear()

        print '-----OVS Rule Expand by (input,ouput)-----\n',port_relation_information
        
if __name__ == "__main__":
    main()
