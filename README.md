# OpenStack-Ironic-and-Server-List
On OpenStack TripleO, user can see IPMI IP by running openstack baremetal node show on certain ironic/baremetal UUID.
However in many case to identify the server, we usually use server hostname not ironic UUID
So it will be very convenient if we can get the IPMI information, zoning, provisioning IP in one output.

This serverlist.py will print out the list of IPMI IP from ironic, provisioning IP, server hostname and server zone in one output.
Run this script from Undercloud VM. It need to source stackrc and overcloudrc.

I assumes that the compute host use "compute" string in its hostname, e.g. overcloud-compute-0
If the compute hostname use different naming convention e.g. overcloud-worker-0, change line cmp_key = "compute" to cmp_key = "worker" or to whatever keyword can used to filter the compute hostname.
Otherwise remove the codes to check compute zone.

Command:
$ python serverlist.py

or you can pipe to a file

$ python serverlist.py > serverlist.txt
