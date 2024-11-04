#!/usr/bin/env python3
import rospy
from nmea_msgs.msg import Sentence
from sensor_msgs.msg import NavSatFix, NavSatStatus
from std_msgs.msg import Header


gnss_data = NavSatFix()

def parse_nmea_sentence(nmea_sentence):
    try:
        parts = nmea_sentence.split(',')
        if parts[0] == "$GPGGA":
            latitude = float(parts[2])
            latitude_direction = parts[3]
            longitude = float(parts[4])
            longitude_direction = parts[5]
            altitude = float(parts[9])

            latitude = (latitude // 100) + ((latitude % 100) / 60)
            longitude = (longitude // 100) + ((longitude % 100) / 60)
            if latitude_direction == 'S':
                latitude = -latitude
            if longitude_direction == 'W':
                longitude = -longitude

            return latitude, longitude, altitude
    except (ValueError, IndexError) as e:
        rospy.logwarn("NMEA sentence parsing error: %s", e)
    return None, None, None

def nmea_callback(data):
    latitude, longitude, altitude = parse_nmea_sentence(data.sentence)
    
    if latitude is not None and longitude is not None:
        nmea2navsatfix_msg = NavSatFix()
        nmea2navsatfix_msg.header = gnss_data.header
        nmea2navsatfix_msg.status = gnss_data.status
        nmea2navsatfix_msg.position_covariance = gnss_data.position_covariance
        nmea2navsatfix_msg.position_covariance_type = gnss_data.position_covariance_type
        
        nmea2navsatfix_msg.latitude = latitude
        nmea2navsatfix_msg.longitude = longitude
        nmea2navsatfix_msg.altitude = altitude

        pub.publish(nmea2navsatfix_msg)
#         rospy.loginfo(
#     "\n---\nheader:\n  seq: {seq}\n  stamp:\n    secs: {secs}\n    nsecs: {nsecs}\n  frame_id: {frame_id}\n"
#     "status:\n  status: {status}\n  service: {service}\n"
#     "latitude: {latitude}\nlongitude: {longitude}\naltitude: {altitude}\n"
#     "position_covariance: {covariance}\nposition_covariance_type: {covariance_type}\n---".format(
#         seq=nmea2navsatfix_msg.header.seq,
#         secs=nmea2navsatfix_msg.header.stamp.secs,
#         nsecs=nmea2navsatfix_msg.header.stamp.nsecs,
#         frame_id=nmea2navsatfix_msg.header.frame_id,
#         status=nmea2navsatfix_msg.status.status,
#         service=nmea2navsatfix_msg.status.service,
#         latitude=nmea2navsatfix_msg.latitude,
#         longitude=nmea2navsatfix_msg.longitude,
#         altitude=nmea2navsatfix_msg.altitude,
#         covariance=nmea2navsatfix_msg.position_covariance,
#         covariance_type=nmea2navsatfix_msg.position_covariance_type,
#     )
# )

def gnss_callback(data):
    global gnss_data
    gnss_data = data

def main():
    rospy.init_node('gnss_nmea_converter', anonymous=True)
    global pub
    pub = rospy.Publisher('/nmea2gnss', NavSatFix, queue_size=10)

    rospy.Subscriber('/nmea', Sentence, nmea_callback)
    rospy.Subscriber('/gnss', NavSatFix, gnss_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
