import ply.yacc as yacc
import OVSRuleLex

class OVSRuleYacc():
    def __init__(self):
        self.lexer = OVSRuleLex.OVSRuleLex()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self,write_tables=1,debug=True)
        self.msg = ''
        self.dpid = 0

    def clear(self):
        self.msg = ''
        self.dpid = 0

    def build(self,ovs_rule_origin,dpid):
        self.dpid = dpid
        if ovs_rule_origin:
            return self.parser.parse(ovs_rule_origin,self.lexer.lexer,0,0,None)
        else:
            return []

    def p_openvswitch(self,p):
        '''openvswitch : openflow_protocol_information openflow_rule_list'''
        self.msg += ']'

    def p_openflow_protocol_information(self,p):
        '''openflow_protocol_information : OFPST_FLOW REPLY '(' OF ')' '(' XID '=' HEX ')' ':'
                                        | NXST_FLOW REPLY '(' XID '=' HEX ')' ':' '''
        self.msg += '['

    def p_openflow_rule_list(self,p):
        '''openflow_rule_list : start_rule openflow_rule another_rule openflow_rule_list
                         | start_rule openflow_rule'''

    def p_another_rule(self,p):
        "another_rule : "
        self.msg += ','

    def p_start_rule(self,p):
        "start_rule :"
        self.msg = self.msg+'{"dpid":"'+str(self.dpid)+'",'

    def p_openflow_rule(self,p):
        '''openflow_rule : openflow_rule_element ',' openflow_rule_element_list
                         | openflow_rule_element'''
        self.msg += '}\n'

    def p_openflow_rule_element_list(self,p):
        '''openflow_rule_element_list : openflow_rule_element ',' openflow_rule_element_list
                                      | openflow_rule_element openflow_rule_element_list
                                      | openflow_rule_element_end'''


    def p_openflow_rule_element_end(self,p):
        '''openflow_rule_element_end : ACTIONS seen_actions '=' action_list'''

    def p_seen_actions(self,p):
        "seen_actions :"
        self.msg += '"actions":{'

    def p_openflow_rule_element(self,p):
        '''openflow_rule_element : COOKIE '=' HEX
                                 | DURATION '=' SECOND
                                 | TABLE '=' NUMBER
                                 | N_PACKETS '=' NUMBER
                                 | N_BYTES '=' NUMBER
                                 | PRIORITY '=' NUMBER
                                 | IDLE_TIMEOUT '=' NUMBER
                                 | HARD_TIMEOUT '=' NUMBER
                                 | HARD_AGE '=' NUMBER
                                 | IDLE_AGE '=' NUMBER
                                 | IN_PORT seen_in_port '=' port 
                                 | DL_VLAN '=' NUMBER
                                 | DL_VLAN '=' HEX
                                 | DL_SRC '=' MAC
                                 | DL_DST '=' MAC
                                 | DL_SRC '=' MAC '/' MAC
                                 | DL_DST '=' MAC '/' MAC
                                 | DL_TYPE '=' HEX 
                                 | NW_SRC '=' IP
                                 | NW_DST '=' IP
                                 | NW_SRC '=' IP '/' IP 
                                 | NW_DST '=' IP '/' IP
                                 | NW_SRC '=' IP '/' NUMBER 
                                 | NW_DST '=' IP '/' NUMBER
                                 | NW_PROTO '=' NUMBER
                                 | NW_TTL '=' NUMBER
                                 | TP_SRC '=' NUMBER
                                 | TP_DST '=' NUMBER 
                                 | TP_SRC '=' NUMBER '/' NUMBER
                                 | TP_DST '=' NUMBER '/' NUMBER
                                 | TP_SRC '=' HEX '/' HEX
                                 | TP_DST '=' HEX '/' HEX
                                 | ICMP_TYPE '=' NUMBER
                                 | ICMP_CODE '=' NUMBER
                                 | METADATA '=' NUMBER
                                 | METADATA '=' NUMBER '/' NUMBER
                                 | METADATA '=' HEX '/' HEX
                                 | S_IP
                                 | S_ICMP
                                 | S_TCP    
                                 | S_UDP
                                 | S_ARP 
                                 | S_RARP
                                 | VLAN_TCI '=' NUMBER
                                 | VLAN_TCI '=' HEX
                                 | VLAN_TCI '=' HEX '/' HEX
                                 | VLAN_TCI '=' NUMBER '/' HEX
                                 | TUN_ID '=' HEX
                                 | TUN_ID '=' HEX '/' HEX
                                 | TUN_SRC '=' IP
                                 | TUN_SRC '=' IP '/' IP
                                 | TUN_SRC '=' IP   '/' NUMBER
                                 | TUN_DST '=' IP
                                 | TUN_DST '=' IP '/' IP
                                 | TUN_DST '=' IP   '/' NUMBER
                                 | REG NUMBER '=' NUMBER
                                 | REG NUMBER '=' HEX
                                 | REG NUMBER '=' NUMBER '/' NUMBER
                                 | REG NUMBER '=' NUMBER '/' HEX
                                 | REG NUMBER '=' HEX '/' NUMBER
                                 | REG NUMBER '=' HEX '/' HEX
                                 | S_IPV6
                                 | S_TCP6
                                 | S_UDP6
                                 | S_ICMP6
                                '''
        if len(p) == 4:
            if isinstance(p[3],(int,float)):    
                self.msg = self.msg+'"'+p[1]+'":'+str(p[3])+','
            else:
                self.msg = self.msg+'"'+p[1]+'":"'+str(p[3])+'",'
        elif len(p) == 6:
            self.msg = self.msg+'"'+p[1]+'":"'+str(p[3])+'/'+str(p[5])+'",'
        elif len(p) == 2:
            self.msg = self.msg+'"'+p[1]+'":"",'
        else:
            self.msg += ','

    def p_seen_in_port(self,p):
        "seen_in_port :"
        self.msg += '"in_port":'

    def p_port(self,p):
        '''port : NUMBER
                | LOCAL 
                | NORMAL 
                | FLOOD 
                | ALL'''
        self.msg += '"'+str(p[1])+'"'

    def p_action_list(self,p):
        '''action_list : action seen_action ',' action_list
                       | action'''
        if len(p) == 2:
            self.msg += '}'

    def p_seen_action(self,p):
        "seen_action :"
        self.msg += ','

    def p_action(self,p):
        '''action : OUTPUT seen_output ':' port
                  | CONTROLLER_INFO
                  | NORMAL
                  | FLOOD
                  | ALL
                  | LOCAL
                  | IN_PORT
                  | DROP
                  | MOD_VLAN_VID ':' NUMBER
                  | MOD_VLAN_PCP ':' NUMBER
                  | STRIP_VLAN
                  | PUSH_VLAN ':' HEX
                  | PUSH_MPLS ':' HEX
                  | POP_MPLS ':' HEX
                  | MOD_DL_SRC ':' MAC
                  | MOD_DL_DST ':' MAC
                  | MOD_NW_SRC ':' IP
                  | MOD_NW_DST ':' IP
                  | MOD_TP_SRC seen_mod_tp_src ':' port
                  | MOD_TP_DST seen_mod_tp_dst ':' port
                  | RESUBMIT seen_resubmit ':' port
                  | RESUBMIT '(' ',' ')'
                  | RESUBMIT seen_resubmit_lp '(' port ',' ')'
                  | RESUBMIT '(' ',' NUMBER ')'
                  | RESUBMIT seen_resubmit_lp '(' port ',' NUMBER ')'
                  | SET_FIELD seen_set_field ':' NUMBER POINTER IN_PORT
                  | SET_FIELD seen_set_field ':' LOCAL POINTER IN_PORT
                  | SET_FIELD seen_set_field ':' ALL POINTER IN_PORT
                  | SET_FIELD seen_set_field ':' FLOOD POINTER IN_PORT
                  | SET_FIELD seen_set_field ':' HEX POINTER DL_VLAN
                  | SET_FIELD seen_set_field ':' MAC POINTER DL_SRC
                  | SET_FIELD seen_set_field ':' MAC POINTER DL_DST
                  | SET_FIELD seen_set_field ':' HEX POINTER DL_TYPE
                  | SET_FIELD seen_set_field ':' IP POINTER NW_SRC
                  | SET_FIELD seen_set_field ':' IP POINTER NW_DST
                  | SET_FIELD seen_set_field ':' NUMBER POINTER NW_PROTO
                  | SET_FIELD seen_set_field ':' NUMBER POINTER NW_TTL
                  | SET_FIELD seen_set_field ':' NUMBER POINTER TP_SRC
                  | SET_FIELD seen_set_field ':' NUMBER POINTER TP_DST
                  | SET_FIELD seen_set_field ':' NUMBER POINTER ICMP_TYPE
                  | SET_FIELD seen_set_field ':' NUMBER POINTER ICMP_CODE
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_IP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_ICMP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_TCP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_UDP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_ARP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_RARP
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_IPV6
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_TCP6
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_UDP6
                  | SET_FIELD seen_set_field ':' NUMBER POINTER S_ICMP6
                  | SET_TUNNEL ':' NUMBER
                  | SET_TUNNEL ':' HEX
                  | SET_TUNNEL64 ':' NUMBER
                  | SET_TUNNEL64 ':' HEX
                  | DEC_TTL 
                  | DEC_TTL '[' '(' NUMBER NUMBER ')' ']'
                  | GOTO_TABLE ':' NUMBER
                  | LEARN seen_start_learn '(' learn_list ')'
                  | MOVE ':' NUMBER POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | MOVE ':' NUMBER POINTER  NXM_EXTENSION '[' ']'
                  | MOVE ':' HEX POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | MOVE ':' HEX POINTER  NXM_EXTENSION '[' ']'
                  | MOVE ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | MOVE ':' NXM_EXTENSION '[' ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | MOVE ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER  NXM_EXTENSION '[' ']'
                  | MOVE ':' NXM_EXTENSION '[' ']' POINTER  NXM_EXTENSION '[' ']'
                  | LOAD ':' NUMBER POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | LOAD ':' NUMBER POINTER  NXM_EXTENSION '[' ']'
                  | LOAD ':' HEX POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | LOAD ':' HEX POINTER  NXM_EXTENSION '[' ']'
                  | LOAD ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | LOAD ':' NXM_EXTENSION '[' ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                  | LOAD ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER  NXM_EXTENSION '[' ']'
                  | LOAD ':' NXM_EXTENSION '[' ']' POINTER  NXM_EXTENSION '[' ']'
                  '''

        if len(p) == 2:
            if p[1][:10] == 'CONTROLLER':
                self.msg = self.msg+'"'+p[1][:10]+'":"'+p[1][11:]+'"'
            else:
                self.msg = self.msg+'"'+p[1]+'":""'
        elif len(p) == 4:
            if isinstance(p[3],(int,float)):    
                self.msg = self.msg+'"'+p[1]+'":'+str(p[3])
            else:
                self.msg = self.msg+'"'+p[1]+'":"'+str(p[3])+'"'
        elif len(p) == 'set_field':
            self.msg = self.msg+str(p[4])+p[5]+p[6]
        elif p[1] == 'resubmit':
            if p[2] == '(':
                if p[4] == ')':
                    self.msg += '"resubmit":"(,)"'
                else:
                    self.msg = self.msg+'"resubmit":"(,'+str(p[4])+')"'
            else:
                if p[6] == ')':
                    self.msg += ',)"'
                else:
                    self.msg = self.msg+','+str(p[5])+')"'
        elif p[1] == 'load':
            if len(p) == 8:
                self.msg = self.msg+'"load":"'+str(p[3])+'->'+str(p[5])+'[]"'
            elif len(p) == 12:
                self.msg = self.msg+'"load":"'+str(p[3])+'->'+str(p[5])+'['+str(p[7])+'..'+str(p[10])+']"'
            elif len(p) == 10:
                self.msg = self.msg+'"load":"'+str(p[3])+'[]->'+str(p[7])+'[]"'
            elif len(p) == 14:
                if p[5] == ']':
                    self.msg = self.msg+'"load":"'+str(p[3])+'[]->'+str(p[7])+'['+str(p[9])+'..'+str(p[12])+']"'
                else:
                    self.msg = self.msg+'"load":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'[]"'
            else:
                    self.msg = self.msg+'"load":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'['+str(p[13])+'..'+str(p[16])+']"'
        elif p[1] == 'move':
            if len(p) == 8:
                self.msg = self.msg+'"move":"'+str(p[3])+'->'+str(p[5])+'[]"'
            elif len(p) == 12:
                self.msg = self.msg+'"move":"'+str(p[3])+'->'+str(p[5])+'['+str(p[7])+'..'+str(p[10])+']"'
            elif len(p) == 10:
                self.msg = self.msg+'"move":"'+str(p[3])+'[]->'+str(p[7])+'[]"'
            elif len(p) == 14:
                if p[5] == ']':
                    self.msg = self.msg+'"move":"'+str(p[3])+'[]->'+str(p[7])+'['+str(p[9])+'..'+str(p[12])+']"'
                else:
                    self.msg = self.msg+'"move":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'[]"'
            else:
                    self.msg = self.msg+'"move":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'['+str(p[13])+'..'+str(p[16])+']"'
        elif len(p) == 8:
            self.msg = self.msg+'"'+p[1]+'":'+'"[('+p[4]+','+p[6]+')]"'

    def p_seen_output(self,p):
        "seen_output :"
        self.msg += '"output":'

    def p_seen_mod_tp_src(self,p):
        "seen_mod_tp_src :"
        self.msg += '"mod_tp_src":'

    def p_seen_mod_tp_dst(self,p):
        "seen_mod_tp_dst :"
        self.msg += '"mod_tp_dst":'

    def p_seen_set_field(self,p):
        "seen_set_field :"
        self.msg += '"set_field":'

    def p_seen_resubmit(self,p):
        "seen_resubmit :"
        self.msg += '"resubmit":'

    def p_seen_resubmit_lp(self,p):
        "seen_resubmit_lp :"
        self.msg += '"resubmit":"('

    def p_seen_learn_start(self,p):
        "seen_start_learn :"
        self.msg += '"learn":{'

    def p_learn_list(self,p):
        '''learn_list : learn seen_learn ',' learn_list
                       | learn'''
        if len(p) == 2:
            self.msg += '}'

    def p_seen_learn(self,p):
        "seen_learn :"
        self.msg += ','

    def p_learn_(self,p):
        '''learn : IDLE_TIMEOUT '=' NUMBER
                      | HARD_TIMEOUT '=' NUMBER
                      | PRIORITY '=' NUMBER
                      | FIN_IDLE_TIMEOUT '=' NUMBER
                      | FIN_HARD_TIMEOUT '=' NUMBER
                      | TABLE '=' NUMBER
                      | NXM_EXTENSION '[' ']'
                      | NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' '=' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | NXM_EXTENSION '[' ']' '=' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' '=' NXM_EXTENSION '[' ']'
                      | NXM_EXTENSION '[' ']' '=' NXM_EXTENSION '[' ']'
                      | LOAD ':' NUMBER POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | LOAD ':' NUMBER POINTER  NXM_EXTENSION '[' ']'
                      | LOAD ':' HEX POINTER  NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | LOAD ':' HEX POINTER  NXM_EXTENSION '[' ']'
                      | LOAD ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | LOAD ':' NXM_EXTENSION '[' ']' POINTER NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | LOAD ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']' POINTER  NXM_EXTENSION '[' ']'
                      | LOAD ':' NXM_EXTENSION '[' ']' POINTER  NXM_EXTENSION '[' ']'
                      | OUTPUT ':' NXM_EXTENSION '[' ']'
                      | OUTPUT ':' NXM_EXTENSION '[' NUMBER '.' '.' NUMBER ']'
                      | APPLY_ACTIONS '(' action_list ')'
                      | CLEAR_ACTIONS 
                      | WRITE_METADATA ':' NUMBER 
                      | WRITE_METADATA ':' NUMBER '/' NUMBER 
                      | WRITE_METADATA ':' HEX 
                      | WRITE_METADATA ':' HEX '/' HEX
                      | GOTO_TABLE ':' NUMBER'''
        if p[1] == 'load':
            if len(p) == 8:
                self.msg = self.msg+'"load":"'+str(p[3])+'->'+str(p[5])+'[]"'
            elif len(p) == 12:
                self.msg = self.msg+'"load":"'+str(p[3])+'->'+str(p[5])+'['+str(p[7])+'..'+str(p[10])+']"'
            elif len(p) == 10:
                self.msg = self.msg+'"load":"'+str(p[3])+'[]->'+str(p[7])+'[]"'
            elif len(p) == 14:
                if p[5] == ']':
                    self.msg = self.msg+'"load":"'+str(p[3])+'[]->'+str(p[7])+'['+str(p[9])+'..'+str(p[12])+']"'
                else:
                    self.msg = self.msg+'"load":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'[]"'
            else:
                    self.msg = self.msg+'"load":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']->'+str(p[11])+'['+str(p[13])+'..'+str(p[16])+']"'
        elif p[1][:3] == 'NXM':
            if p[3] == ']':
                if len(p) == 4:
                    self.msg = self.msg+'"'+str(p[1])+'":""'
                elif p[7] == ']':
                    self.msg = self.msg+'"'+str(p[1])+'[]":"'+str(p[5])+'[]"'
                else:
                    self.msg = self.msg+'"'+str(p[1])+'[]":"'+str(p[5])+'['+str(p[7])+'..'+str(p[10])+']"'
            else:
                if len(p) == 8:
                    self.msg = self.msg+'"'+str(p[1])+'['+str(p[3])+'..'+str(p[6])+']":""'
                elif p[11] == ']':
                    self.msg = self.msg+'"'+str(p[1])+'['+str(p[3])+'..'+str(p[6])+']":"'+str(p[9])+'[]"'
                else:
                    self.msg = self.msg+'"'+str(p[1])+'['+str(p[3])+'..'+str(p[6])+']":"'+str(p[9])+'['+str(p[11])+'..'+str(p[14])+']"'
        elif p[1] == 'output':
            if len(p) == 6:
                self.msg = self.msg+'"output":"'+str(p[3])+'[]"'
            else:
                self.msg = self.msg+'"output":"'+str(p[3])+'['+str(p[5])+'..'+str(p[8])+']"'
        elif p[1] == 'clear_action':
            self.msg = self.msg+'"'+str(p[1])+'":""'
        elif p[1] == 'write_metadata':
            if len(p) == 4:
                self.msg = self.msg+'"write_metadata":'+str(p[3])
            else:
                self.msg = self.msg+'"write_metadata":'+str(p[3])+'/'+str(p[5])
        elif len(p) == 4:
            if isinstance(p[3],(int,float)):
                self.msg = self.msg+'"'+p[1]+'":'+str(p[3])
            else:
                self.msg = self.msg+'"'+p[1]+'":"'+str(p[3])+'"'

    def p_error(self,p):
        self.msg = "ERROR"
