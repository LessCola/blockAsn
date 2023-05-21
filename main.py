import requests
import os
import re
# os.system(cmd)


class BlockAsn():
    def __init__(self):
        self.asn_list = []
        self.asnList_url = 'https://raw.githubusercontent.com/VirgilClyne/GetSomeFries/main/ruleset/ASN.China.list'
        self.ipset_url   = 'https://asn.ipinfo.app/api/download/ipset/AS'


    def del_all_asn(self):
        ip4shell = 'iptables -F asn_block'
        ip6shell = 'ip6tables -F asn_block'
        os.system(ip4shell)
        os.system(ip6shell)


    def get_asn_list(self):
        r = requests.get(self.asnList_url)
        r = r.text
        for x in r.splitlines():
            if x.startswith('IP-ASN'):
                asn = re.findall(r'\b\d+\b',x)[0]
                self.asn_list.append(asn)
    
    def block_asn(self):
        for x in self.asn_list:
            sh = requests.get(str(self.ipset_url) + str(x))
            sh = sh.text
            shell = ''
            for i in sh.splitlines():
                if i .startswith('iptables') or i .startswith('ip6tables'):
                    pass
                else:
                    shell += (i + '\n')
            shell = shell + ('iptables -A asn_block -m set --match-set %s-4 src -p tcp --dport 52525 -j DROP')  % x + '\n'
            shell = shell + ('iptables -A asn_block -m set --match-set %s-4 src -p udp --dport 52525 -j DROP')  % x + '\n'
            shell = shell + ('ip6tables -A asn_block -m set --match-set %s-6 src -p tcp --dport 52525 -j DROP') % x + '\n'
            shell = shell + ('ip6tables -A asn_block -m set --match-set %s-6 src -p udp --dport 52525 -j DROP') % x
            os.system(shell)



    def main(self):
        self.del_all_asn()
        self.get_asn_list()
        self.block_asn()


if __name__ == '__main__':
    BlockAsn = BlockAsn()
    BlockAsn.main()

