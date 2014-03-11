from pysnmp.entity.rfc3413.oneliner import cmdgen

snmpCmdGen = cmdgen.CommandGenerator()
snmpTransportData = cmdgen.UdpTransportTarget(('localhost', 161))

error, errorStatus, errorIndex, binds = snmpCmdGen.getCmd(cmdgen.CommunityData("public"), snmpTransportData, "1.3.6.1.2.1.1.1.0", "1.3.6.1.2.1.1.3.0", "1.3.6.1.2.1.2.1.0")
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