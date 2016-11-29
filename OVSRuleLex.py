import ply.lex as lex

class OVSRuleLex():
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = (
    'OFPST_FLOW','NXST_FLOW','REPLY','OF','XID','COOKIE','DURATION','TABLE','N_PACKETS','N_BYTES','PRIORITY','IN_PORT','DL_VLAN','DL_SRC','DL_DST','DL_TYPE','NW_SRC','NW_DST','NW_PROTO','NW_TTL','TP_SRC','TP_DST','ICMP_TYPE','ICMP_CODE','S_IP','S_ICMP','S_TCP','S_UDP','S_ARP','S_RARP','VLAN_TCI','TUN_ID','TUN_SRC','TUN_DST','REG','S_IPV6','S_TCP6','S_UDP6','S_ICMP6','ACTIONS','IDLE_TIMEOUT','HARD_TIMEOUT','HARD_AGE','IDLE_AGE','OUTPUT','LOCAL','NORMAL','FLOOD','ALL','CONTROLLER_INFO','DROP','MOD_VLAN_VID','MOD_VLAN_PCP','STRIP_VLAN','PUSH_VLAN','PUSH_MPLS','POP_MPLS','MOD_DL_SRC','MOD_DL_DST','MOD_NW_SRC','MOD_NW_DST','MOD_TP_SRC','MOD_TP_DST','RESUBMIT','SET_FIELD','SET_TUNNEL','SET_TUNNEL64','DEC_TTL','LEARN','FIN_IDLE_TIMEOUT','FIN_HARD_TIMEOUT','LOAD','MOVE','APPLY_ACTIONS','CLEAR_ACTIONS','WRITE_METADATA','METADATA','HEX','SECOND','NUMBER','MAC','IP','POINTER','GOTO_TABLE','NXM_EXTENSION'
        )

    literals = ['(',')',',',':','=','/','-','>','[',']','.']

    t_ignore = ' \t'
    t_OFPST_FLOW = r'OFPST_FLOW'
    t_NXST_FLOW = r'NXST_FLOW'
    t_REPLY = r'reply'

    def t_OF(self,t):
        r'OF\d+\.\d+'
        t.value = float(t.value[2:])
        return t

    t_XID = r'xid'

    def t_NEWLINE(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    t_POINTER = r'->'
    t_GOTO_TABLE = r'go_table'

    t_COOKIE = r'cookie'
    t_DURATION = r'duration'
    t_TABLE = r'table'
    t_N_PACKETS = r'n_packets'
    t_N_BYTES = r'n_bytes'
    t_PRIORITY = r'priority'

    t_IN_PORT = r'in_port'
    t_DL_VLAN = r'dl_vlan'
    t_DL_SRC = r'dl_src'
    t_DL_DST = r'dl_dst'
    t_DL_TYPE = r'dl_type'
    t_NW_SRC = r'nw_src'
    t_NW_DST = r'nw_dst'
    t_NW_PROTO = r'nw_proto'
    t_NW_TTL = r'nw_ttl'
    t_TP_SRC =  r'tp_src'
    t_TP_DST = r'tp_dst'
    t_ICMP_TYPE = r'icmp_type'
    icmp6t_ICMP_CODE = r'icmp_code'
    t_S_IP = r'ip'
    t_S_ICMP = r'icmp'
    t_S_TCP = r'tcp'
    t_S_UDP = r'udp'
    t_S_ARP = r'arp'
    t_S_RARP = r'rarp'
    t_VLAN_TCI = r'vlan_tci'
    t_TUN_ID = r'tun_id'
    t_TUN_SRC = r'tun_src'
    t_TUN_DST = r'tun_dst'
    t_REG = r'reg'
    t_S_IPV6 = r'ipv6'
    t_S_TCP6 = r'tcp6'
    t_S_UDP6 = r'udp6'
    t_S_ICMP6 = r'icmp6'

    t_ACTIONS = r'actions'

    t_IDLE_TIMEOUT = r'idle_timeout'
    t_HARD_TIMEOUT = r'hard_timeout'
    t_HARD_AGE = r'hard_age'
    t_IDLE_AGE = r'idle_age'

    t_OUTPUT = r'output'

    t_LOCAL = r'LOCAL'
    t_NORMAL = r'NORMAL'
    t_FLOOD = r'FLOOD'
    t_ALL = r'ALL'
    t_DROP = r'drop'

    t_MOD_VLAN_VID = r'mod_vlan_vid'
    t_MOD_VLAN_PCP = r'mod_vlan_pcp'
    t_STRIP_VLAN = r'strip_vlan'
    t_PUSH_MPLS = r'push_mpls'
    t_POP_MPLS = r'pop_mpls'
    t_MOD_DL_SRC = r'mod_dl_src'
    t_MOD_DL_DST = r'mod_dl_dst'
    t_MOD_NW_SRC = r'mod_nw_src'
    t_MOD_NW_DST = r'mod_nw_dst'
    t_MOD_TP_SRC = r'mod_tp_src'
    t_MOD_TP_DST = r'mod_tp_dst'
    t_RESUBMIT = r'resubmit'
    t_SET_TUNNEL = r'set_tunnel'
    t_SET_TUNNEL64 = r'set_tunnel64'
    t_DEC_TTL = r'dec_ttl'
    t_SET_FIELD = r'set_field'
    t_LEARN = r'learn'
    t_FIN_IDLE_TIMEOUT = r'fin_idle_timeout'
    t_FIN_HARD_TIMEOUT = r'fin_hard_timeout'
    t_LOAD = r'load'
    t_MOVE = r'move'
    t_APPLY_ACTIONS = r'apply_actions'
    t_CLEAR_ACTIONS = r'clear_actions'
    t_WRITE_METADATA = r'write_metadata'

    def t_HEX(self,t):
        r'0x[0-9A-Za-z]+'
        return t

    def t_MAC(self,t):
        r'([0-9A-Za-z]{2}[:-]){5}([0-9A-Za-z]{2})'
        return t

    def t_IP(self,t):
        r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])'
        return t

    def t_SECOND(self,t):
        r'\d*\.\d+s|\d+s'
        t.value = float(t.value[0:len(t.value)-1])#discard "s"
        return t

    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CONTROLLER_INFO(self,t):
        r'CONTROLLER:\d+'
        return t

    def t_NXM_EXTENSION(self,t):
        r'NXM_[A-Za-z_]+'
        return t

    def t_error(self,t):
        f.write("[LEX] Illegal character '%s' '%d'" % (t.value[0],t.lineno))
        t.lexer.skip(1)

