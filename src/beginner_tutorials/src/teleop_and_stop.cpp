# include "ros/ros.h"
# include "std_msgs/String.h"
# include "geometry_msgs/Twist.h"
# include "geometry_msgs/TwistStamped.h"
# include "sensor_msgs/LaserScan.h"
# include "message_filters/time_synchronizer.h"
# include "message_filters/subscriber.h"
# include "std_msgs/Header.h"

using namespace std_msgs;
using namespace sensor_msgs;
using namespace geometry_msgs;
using namespace message_filters;

//Need to figure out how to avoid the scoping problem, where I'm currently passing in the publishers and subscribers as parameters

/*

void teleop_callback(ros::Publisher altered_input_pub, Twist input) {
  //if you like it you should put a stamp on it
  TwistStamped output = TwistStamped();
  output.twist = input;
  output.header = Header();
  output.header.stamp = ros::Time::now();
  altered_input_pub.publish(output);

}

void scan_and_teleop_callback(ros::Publisher move_pub, TwistStamped input, LaserScan scan)
{
  bool near_wall = false;
  geometry_msgs::Twist stahp = Twist();
  for (int i = 0; i < scan.ranges.size(); i++)
  {
      if (i <= 0.5 && input.twist.linear.x >= 0) {
        move_pub.publish(stahp);
        near_wall = true;
      } else if (not near_wall) {
        move_pub.publish(input.twist);
      }
  }

}
*/

class Teleop_and_Stop
{
  public:
    ros::Publisher move_pub;
    ros::Publisher altered_input_pub;

    Teleop_and_Stop(ros::NodeHandle& n);
    //void teleop_callback(const Twist& input);
    //void scan_and_teleop_callback(const TwistStamped& input, const LaserScan& scan);
    void scan_callback(const LaserScan& scan);

  private:
    ros::NodeHandle n_;
};

Teleop_and_Stop::Teleop_and_Stop(ros::NodeHandle& n) : n_(n)
{
  ROS_INFO_STREAM("got to 62");
  ros::Publisher move_pub = n.advertise<Twist>("cmd_vel_mux/input/navi", 1000);
  //ros::Publisher altered_input_pub = n.advertise<TwistStamped>("/my_altered_input", 1000);
  //ros::Subscriber teleop_sub = n.subscribe("/my_teleop", 1, &Teleop_and_Stop::teleop_callback, this);
  ros::Subscriber scan_sub = n.subscribe("/scan", 1, &Teleop_and_Stop::scan_callback, this);

  // message_filters::Subscriber <LaserScan> scan_sub(n, "/scan", 1000);
  // message_filters::Subscriber <TwistStamped> altered_input_sub(n, "/my_altered_input", 1000);
  // TimeSynchronizer<TwistStamped, LaserScan> ats(altered_input_sub, scan_sub, 10);
  // ats.registerCallback(&Teleop_and_Stop::scan_and_teleop_callback);
}
//
// void Teleop_and_Stop::teleop_callback(const Twist& input)
// {
//   //if you like it you should put a stamp on it
//   TwistStamped output = TwistStamped();
//   output.twist = input;
//   output.header = Header();
//   output.header.stamp = ros::Time::now();
//   altered_input_pub.publish(output);
// }

void Teleop_and_Stop::scan_callback(const LaserScan& scan)
{
  Twist forward = Twist();
  forward.linear.x = 1.0;
  bool is_near_wall = false;
  for (int i = 0; i < scan.ranges.size(); i++)
  {
    if (i <= 0.5)
    {
      move_pub.publish(Twist());
      is_near_wall = true;
    } else if (!is_near_wall) {
      move_pub.publish(forward);
    }
  }
}

// void Teleop_and_Stop::scan_and_teleop_callback(const TwistStamped& input, const LaserScan& scan)
// {
//   bool near_wall = false;
//   geometry_msgs::Twist stahp = Twist();
//   for (int i = 0; i < scan.ranges.size(); i++)
//   {
//       if (i <= 0.5 && input.twist.linear.x >= 0) {
//         move_pub.publish(stahp);
//         near_wall = true;
//       } else if (not near_wall) {
//         move_pub.publish(input.twist);
//       }
//   }
// }


int main(int argc, char **argv)
{
  /*
  ros::init(argc, argv, "cp_teleop_and_stop");
  ros::NodeHandle n;

  ros::Publisher move_pub = n.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/teleop", 1000);
  ros::Publisher altered_input_pub = n.advertise<TwistStamped>("/my_altered_input", 1000);

  message_filters::Subscriber <LaserScan> scan_sub(n, "/scan", 1000);
  ros::Subscriber teleop_sub = n.subscribe("/my_teleop", 1000, teleop_callback(altered_input_pub));
  message_filters::Subscriber <TwistStamped> altered_input_sub(n, "/my_altered_input", 1000);

  message_filters.TimeSynchronizer<TwistStamped, LaserScan> ats(altered_input_sub, scan_sub);
  ats.registerCallback(scan_and_teleop_callback(move_pub));
  */
  ros::init(argc, argv, "cp_teleop_and_stop");
  ROS_INFO_STREAM("here");
  ros::NodeHandle n;
  Teleop_and_Stop ts(n);
  ros::spin();
  return 0;
}
