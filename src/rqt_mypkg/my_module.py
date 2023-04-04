#!/usr/bin/env python3
import os
import rospy
import rospkg
from geometry_msgs.msg import PoseStamped, PointStamped, PoseWithCovarianceStamped
import psycopg2

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget,QPushButton,QVBoxLayout,QCheckBox,QLCDNumber,QLineEdit

 
class MyPlugin(Plugin):

    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.points = [] # Add this line to define the "points" attribute
        self.issendpoint = None
        self.count= 0

        self.setObjectName('MyPlugin')
        # self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        self.pub = rospy.Publisher("clicked_point", PointStamped, queue_size=100)

  

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print('arguments: ', args)
            print ('unknowns: ', unknowns)

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('MyPluginUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        self.insert_table = 'pose_a'

        self.update_table = 'pose_a_init'

        self.id_update = "1"

        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface

        context.add_widget(self._widget)

        # Create a button and add it to the layout
  
        button = self._widget.findChild(QPushButton, 'add_point_one_cilck')

        button.clicked.connect(self.add_point_on_button_click2)
        
     
        button2 = self._widget.findChild(QPushButton, 'save')

        button2.clicked.connect(self.save_point_on_button_click2)

        button3 = self._widget.findChild(QPushButton, 'delete_value_teble')

        button3.clicked.connect(self.delete_data)


        button4 = self._widget.findChild(QPushButton, 'remove_point')

        button4.clicked.connect(self.remove_point)

        button5 = self._widget.findChild(QPushButton, 'add_point_continue')

        button5.clicked.connect(self.add_point_on_button_click2_continue)

        button6 = self._widget.findChild(QPushButton, 'create_db')

        button6.clicked.connect(self.create_db)
        

        button7 = self._widget.findChild(QPushButton, 'run_navigation_agv')
        button7.clicked.connect(self.run_navigation_agv)

        button8 = self._widget.findChild(QPushButton, 'run_navigation_agv')
        button8.clicked.connect(self.run_visualize)

        button9 = self._widget.findChild(QPushButton, 'run_navigation_agv')
        button9.clicked.connect(self.run_navigation_agv)

        button10 = self._widget.findChild(QPushButton, 'add_point_init_2')
        button10.clicked.connect(self.add_point_init_2)

        button11 = self._widget.findChild(QPushButton, 'save_init')

        button11.clicked.connect(self.save_point_init_on_button_click2)


        self.checkbox = self._widget.findChild(QCheckBox, 'pose_a')
        self.checkbox.stateChanged.connect(self.insert_table_name_a)
        
        self.checkbox = self._widget.findChild(QCheckBox, 'pose_b')
        self.checkbox.stateChanged.connect(self.insert_table_name_b)
        
        self.checkbox = self._widget.findChild(QCheckBox, 'pose_c')
        self.checkbox.stateChanged.connect(self.insert_table_name_c)


        self.checkbox = self._widget.findChild(QCheckBox, 'pose_a_init')
        self.checkbox.stateChanged.connect(self.update_table_name_a)
        
        self.checkbox = self._widget.findChild(QCheckBox, 'pose_b_init')
        self.checkbox.stateChanged.connect(self.update_table_name_b)
        
        self.checkbox = self._widget.findChild(QCheckBox, 'pose_c_init')
        self.checkbox.stateChanged.connect(self.update_table_name_c)



        self.numberlcd = self._widget.findChild(QLCDNumber, 'arrypoint')

        # self.lineedit = 
        self.line_edit =self._widget.findChild(QLineEdit,'intervel_point')
        self.line_edit.setPlaceholderText('Enter text here')

        # self.conn = psycopg2.connect(
        #     dbname="dbagv8",
        #     user="postgres",
        #     password="pass1234",
        #     host="192.168.54.165",
        #     port="5432",
        # )

        self.conn = psycopg2.connect(
            dbname="dbagv8",
            user="postgres",
            password="pass1234",
            host="localhost",
            port="5432",
        )

        # self.conn = psycopg2.connect(
        #     dbname="dbagv8",
        #     user="postgres",
        #     password="pass1234",
        #     host="192.168.54.165",
        #     port="5432",
        # )
    def insert_data(self, points):
        # print(self.points)

        print("Delete")

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""DROP TABLE {self.insert_table}""")
        self.conn.commit()

        rospy.sleep(0.5)
        print("CREATE")

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.insert_table} (
                        id SERIAL PRIMARY KEY,
                        position_x DOUBLE PRECISION,
                        position_y DOUBLE PRECISION,
                        position_z DOUBLE PRECISION
                    )
                """)
        self.conn.commit()

        rospy.sleep(0.5)
        print("insert")

        with self.conn.cursor() as cur:
            for point in points:
                cur.execute(f"""
                    INSERT INTO {self.insert_table} (position_x, position_y, position_z)
                    VALUES (%s, %s, %s)
                """, (point.point.x, point.point.y, point.point.z))
        self.conn.commit()

    def create_db(self):  

        rospy.sleep(0.5)
        print("CREATE")

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.insert_table} (
                        id SERIAL PRIMARY KEY,
                        position_x DOUBLE PRECISION,
                        position_y DOUBLE PRECISION,
                        position_z DOUBLE PRECISION
                    )
                """)
        self.conn.commit()


    def update_data(self,points):
        rospy.sleep(0.5)
        print(self.id_update)

        with self.conn.cursor() as cur:
            for point in points:
                print(self.id_update)

                cur.execute(f"""
                    UPDATE {self.update_table}
                    SET position_x = %s, position_y = %s, position_z = %s
                    WHERE id = %s::integer
                """, (point.point.x, point.point.y, point.point.z, int(self.id_update)))
        self.conn.commit()


    def run_navigation_agv(self):  
        print("run_navigation_agv")

        os.system('roslaunch nctc_guideless_navigation nctc_navigation.launch')

    def run_visualize(self):  
        print("run_visualize")

        os.system('~/nctc_guideless/src/nctc_guideless_navigation/rviz/  rviz -d agv_navigation.rviz')



    def delete_data(self, points):
        print("delete")

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""DROP TABLE {self.insert_table}""")
        self.conn.commit()

        rospy.sleep(0.5)
    
    def shutdown_plugin(self):
        self.conn.close()
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
    def add_point_on_button_click2(self):
        # do something here when the button is clicked
        # os.system('rosrun nctc_guideless_oper save_amcl_to_click_point.py ')
        print("add_point_on_button_click2")

        self.issendpoint = True

        self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)

        rospy.sleep(0.5)
        self.sub5.unregister()


    def add_point_on_button_click2_continue(self):

        # self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        # print("add_point_on_button_click2_continue")
        # rospy.sleep(0.5)
        self.issendpoint = True
        print("issendpoint == true")
        self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        print("add_point_on_button_click2_continue")
        rospy.sleep(0.2)
        self.issendpoint = False

        print("issendpoint == False")

    def save_point_on_button_click2(self):
        # do something here when the button is clicked
        # os.system('rosrun nctc_guideless_oper save_amcl_to_click_point.py ')
        # self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        print("save_point")

        # list_len = len(self.points)
        # print(list_len)

        # print(self.points)

        self.insert_data(self.points)

    def save_point_init_on_button_click2(self):
        # do something here when the button is clicked
        # os.system('rosrun nctc_guideless_oper save_amcl_to_click_point.py ')
        # self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        print("save_point_init")

        # list_len = len(self.points)
        # print(list_len)

        # print(self.points)

        self.update_data(self.points)



    def remove_point(self):
        # do something here when the button is clicked
        # os.system('rosrun nctc_guideless_oper save_amcl_to_click_point.py ')
        # self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)
        self.numberlcd.display(0)

        print("remove_point")
        self.points.clear()

        # list_len = len(self.points)
        # print(list_len)

        # print(self.points)

    def cancel_click_point(self):
        print("cancel_click_point")
        self.sub5.unregister()
        # text = self.lineedit.text()
        # print(text)

    def add_point_init_2(self):
        print("add_point_init_2")
        self.issendpoint = True

        self.sub5 = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.sub5_callback)

        rospy.sleep(0.5)
        self.sub5.unregister()


        

    def insert_table_name_a(self, state):
        print("insert_table_name_a")
        if state:
            self.insert_table = 'pose_a'
    
    def insert_table_name_b(self, state):
        print("insert_table_name_b")
        if state:
            self.insert_table = 'pose_b'

    def insert_table_name_c(self, state):
        print("insert_table_name_c")
        if state:
            self.insert_table = 'pose_c'



    def update_table_name_a(self, state):
        print("update_table_name_a")
        if state:
            self.update_table = 'pose_init'
            self.id_update = "1"
    
    def update_table_name_b(self, state):
        print("update_table_name_b")
        if state:
            self.update_table = 'pose_init'
            self.id_update = "2"

    def update_table_name_c(self, state):
        print("update_table_name_c")
        if state:
            self.update_table = 'pose_init'
            self.id_update= "3"

    def sub5_callback(self, msg):
        if(self.issendpoint == True):
            self.msg_raw_odom = msg.pose.pose.orientation.z
            point_stamped = PointStamped()
            # point_stamped.header.seq = row[0]

            point_stamped.header.stamp = rospy.Time.now()
            point_stamped.header.frame_id = "map"
            point_stamped.point.x = msg.pose.pose.position.x
            point_stamped.point.y =  msg.pose.pose.position.y
            point_stamped.point.z =  msg.pose.pose.orientation.z
            rospy.sleep(0.5)
        
            self.points.append(point_stamped)  # append the new PointStamped message to the list
            #self.points.push(point_stamped)
            list_len = len(self.points)
            self.numberlcd.display(list_len)

            self.pub.publish(point_stamped)

            print(point_stamped)
        else:
            self.count =  self.count +  1
       
            text = self.line_edit.text()
            my_int = int(text)
            print(my_int)
            print(self.count)
            if  self.count == my_int:

                self.msg_raw_odom = msg.pose.pose.orientation.z
                point_stamped = PointStamped()
                # point_stamped.header.seq = row[0]

                point_stamped.header.stamp = rospy.Time.now()
                point_stamped.header.frame_id = "map"
                point_stamped.point.x = msg.pose.pose.position.x
                point_stamped.point.y =  msg.pose.pose.position.y
                point_stamped.point.z =  msg.pose.pose.orientation.z
                rospy.sleep(0.5)
            
                self.points.append(point_stamped)  # append the new PointStamped message to the list
                #self.points.push(point_stamped)
                list_len = len(self.points)
                self.numberlcd.display(list_len)

                self.pub.publish(point_stamped)

                print(point_stamped)
                self.count = 0

      