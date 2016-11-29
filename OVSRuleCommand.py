import subprocess

class OVSRuleCommand():
    def get_bridge_list(self):
        cmd = "ovs-vsctl list-br"
        cmd_out = subprocess.check_output(cmd, shell=True)
        bridge_list = []

        for bridge in cmd_out.split():
            bridge_list.append(bridge)

        return bridge_list


    def get_dpid(self,bridge_name):
        cmd = "ovs-ofctl show " + bridge_name
        cmd_out = subprocess.check_output(cmd, shell=True)
        #search dpid
        for word in cmd_out.split():
            if word[:4] == "dpid":
                dpid = word[5:]
                break

        return dpid

    def get_OVSRule(self,bridge_name):
        cmd = "ovs-ofctl dump-flows " + bridge_name
        ovs_rule_origin = subprocess.check_output(cmd, shell=True)
        
        return ovs_rule_origin
