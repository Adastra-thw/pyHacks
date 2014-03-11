from pysnmp.entity.rfc3413.oneliner import cmdgen

snmpCmdGen = cmdgen.CommandGenerator()
snmpTransportData = cmdgen.UdpTransportTarget(('localhost', 161))
mib = cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0)
error, errorStatus, errorIndex, binds = snmpCmdGen.getCmd(cmdgen.CommunityData("public"), snmpTransportData, mib)
if error:
    print "Error "+error
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and binds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in binds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))