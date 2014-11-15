#! /bin/bash
echo BB-BONE-PRU-01 > /sys/devices/bone_capemgr.*/slots                                                       
systemctl start ledscape.service
