import subprocess
import json

cmp_key = "compute"

if __name__ == '__main__':

# Baremetal node list
    bm_node_json = "bm_node_list.json"
    bm_node = open(bm_node_json, 'w')
    bm_line = "source /home/stack/stackrc; openstack baremetal node list --long -c \"Driver Info\" -c \"Instance UUID\" -c Name -f json"
    subprocess.call(bm_line, shell=True, stdout=bm_node)
    bm_node.close()

# Ironic server list
    server_lst_json = "server_lst.json"
    server_lst = open(server_lst_json, 'w')
    server_line = "source /home/stack/stackrc; openstack server list -c ID -c Name -c Networks -f json"
    subprocess.call(server_line, shell=True, stdout=server_lst)
    server_lst.close()

# Compute service list
    cmp_service_json = "cmp_service.json"
    cmp_service = open(cmp_service_json, 'w')
    cmp_line = "source /home/stack/overcloudrc; openstack compute service list -c Host -c Zone -f json"
    subprocess.call(cmp_line, shell=True, stdout=cmp_service)
    cmp_service.close()

#  Load json file
    with open(bm_node_json, 'r') as jbm_stream:
        jbm_data = json.load(jbm_stream)
    with open(server_lst_json, 'r') as svr_stream:
        jsvr_data = json.load(svr_stream)
    with open(cmp_service_json, 'r') as cmp_stream:
        cmp_data = json.load(cmp_stream)

    if len(jsvr_data) != len(jbm_data):
        print "There are missing server, the number of servers in openstack baremetal node list and openstack server list are NOT same."
        exit(1)

    index_min = 0
    index_max = len(jsvr_data)

    index_cmp_min = 0
    index_cmp_max = len(cmp_data)

# Read the server details from json files
    print "ServerUUID , IPMIuser , IPMIaddress , ServerName , HostName , ZoneName , ProvisioningIP"
    for x in range (index_min, index_max):
        new_list_tmp = []
        uuid_svr = jbm_data[x]["Instance UUID"]
        new_list_tmp.append(str(jbm_data[x]["Instance UUID"]))
        new_list_tmp.append(str(jbm_data[x]["Driver Info"]["ipmi_username"]))
        new_list_tmp.append(str(jbm_data[x]["Driver Info"]["ipmi_address"]))
        new_list_tmp.append(str(jbm_data[x]["Name"]))

        for y in range (index_min, index_max):
                if jsvr_data[y]["ID"] == uuid_svr:
                        new_list_tmp.append(str(jsvr_data[y]["Name"]))

                        if cmp_key in jsvr_data[y]["Name"]:
                                for z in range(index_cmp_min, index_cmp_max):
                                        cmp_hostname = jsvr_data[y]["Name"] + ".localdomain"
                                        if cmp_hostname == cmp_data[z]["Host"]:
                                                new_list_tmp.append(str(cmp_data[z]["Zone"]))
                        else:
                                new_list_tmp.append("N/A")
                                
                        new_list_tmp.append(str(jsvr_data[y]["Networks"]))

        
# Print the server details
        ServerUUID = new_list_tmp[0]
        IPMIuser = new_list_tmp[1]
        IPMIaddress = new_list_tmp[2]
        ServerName = new_list_tmp[3]
        HostName = new_list_tmp[4]
        ZoneName = new_list_tmp[5]
        ProvisioningIP = new_list_tmp[6]
        space = ","

#        print ServerUUID ,space, IPMIuser, space, IPMIaddress, space, ServerName, space, HostName, space, ZoneName, space, ProvisioningIP
        print HostName, space, IPMIaddress, space, ServerName, space, ZoneName, space, ProvisioningIP
