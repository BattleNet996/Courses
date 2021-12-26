# author：Charles Chen
# time: 2021.12.24
import RPi.GPIO as GPIO
import time
import threading

class car():
    def __init__(self):
        pass

    def set_up(self,name):
        """进行小车的初始化，包括各种GPIO接口的配置等"""
        print("进行小车的初始化ing！")
        self.name = name
        
        # 设置编码规范
        GPIO.setmode(GPIO.BCM)
    
        # 无视警告，开启引脚
        GPIO.setwarnings(False)

        # Wheel 接口
        # 设置引脚为输出
        self.LEFT_WHEEL_FRONT = 13
        self.LEFT_WHEEL_BACK = 12
        self.LEFT_CONTROL = 6

        self.RIGHT_WHEEL_FRONT = 21
        self.RIGHT_WHEEL_BACK = 20
        self.RIGHT_CONTROL = 26
        GPIO.setup((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.LEFT_CONTROL),GPIO.OUT)
        GPIO.setup((self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK,self.RIGHT_CONTROL),GPIO.OUT)
        
        # 对使能引脚开启pwm控制
        print("初始化使能引脚")
        self.left_speed = GPIO.PWM(self.LEFT_CONTROL, 1000)
        self.right_speed = GPIO.PWM(self.RIGHT_CONTROL, 1000)

        # IrSensor Front 接口
        self.IR_LEFT = 16
        self.IR_RIGHT = 19
        GPIO.setup(self.IR_LEFT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.IR_RIGHT, GPIO.IN, GPIO.PUD_UP)
        

    def stop(self):
        GPIO.output((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK),(0,0,0,0))

    def move_forward(self,speed):
        print("we are moving forward!")
        GPIO.output((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK),(1,0,1,0))
        while self.left_obstacl_distance != 0 and self.right_obstacl_distance != 0:        
            self.left_speed.start(speed)
            self.right_speed.start(speed)
            time.sleep(0.5)

        # 让小车每秒钟逐渐增加速度
        # self.left_speed.start(0)
        # self.right_speed.start(0)
        # for i in range(speed):
        #     self.left_speed.ChangeDutyCycle(10 * i)
        #     self.right_speed.ChangeDutyCycle(10 * i)
        #     time.sleep(1)
        #     print(i,"'s speed up!")

        # x = input("print q to stop:")
        # self.stop()
        return

    def move_backward(self,speed):
        print("we are moving backward!")
        GPIO.output((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK),(0,1,0,1))
        while self.left_obstacl_distance != 1 or self.right_obstacl_distance != 1:        
            self.left_speed.start(speed)
            self.right_speed.start(speed)
            time.sleep(0.5)

        # 让小车每秒钟逐渐增加速度
        # self.left_speed.start(0)
        # self.right_speed.start(0)
        # for i in range(speed):
        #     self.left_speed.ChangeDutyCycle(10 * i)
        #     self.right_speed.ChangeDutyCycle(10 * i)
        #     time.sleep(1)
        #     print(i,"'s speed up!")


        # x = input("print q to stop:")
        # self.stop()
        return
    
    def turn_right(self, speed):
        print("we are turing right!")
        GPIO.output((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK),(1,0,0,1))


        while self.left_obstacl_distance != 1 :  
            self.left_obstacl_distance = GPIO.input(self.IR_LEFT)
            print(f"此时left为: {self.left_obstacl_distance}")      
            self.left_speed.start(speed)
            self.right_speed.start(speed)
            time.sleep(1)


        # 让小车每秒钟逐渐增加速度
        # self.left_speed.start(0)
        # self.right_speed.start(0)
        # for i in range(speed):
        #     self.left_speed.ChangeDutyCycle(10 * i)
        #     self.right_speed.ChangeDutyCycle(10 * i)
        #     time.sleep(1)
        #     print(i,"'s speed up!")

        # x = input("print q to stop:")
        # self.stop()
        return

    def turn_left(self, speed):
        print("we are turing left!")
        GPIO.output((self.LEFT_WHEEL_FRONT,self.LEFT_WHEEL_BACK,self.RIGHT_WHEEL_FRONT,self.RIGHT_WHEEL_BACK),(0,1,1,0))
        
        while self.right_obstacl_distance != 1:      
            self.right_obstacl_distance = GPIO.input(self.IR_RIGHT)  
            self.left_speed.start(speed)
            self.right_speed.start(speed)
            time.sleep(0.5)

        # 让小车每秒钟逐渐增加速度
        # self.left_speed.start(0)
        # self.right_speed.start(0)
        # for i in range(speed):
        #     self.left_speed.ChangeDutyCycle(10 * i)
        #     self.right_speed.ChangeDutyCycle(10 * i)
        #     time.sleep(1)
        #     print(i,"'s speed up!")

        # x = input("print q to stop:")
        # self.stop()
        return

    def detect_obstacles(self):
        while True:
            self.left_obstacl_distance = GPIO.input(self.IR_LEFT)  # 注意，此处若前方有障碍物为0，无障碍物为1
            self.right_obstacl_distance = GPIO.input(self.IR_RIGHT)
            # self.right_obstacl_distance = 1 # 右边坏了...
            print(f"当前左右障碍物的距离为：左{self.left_obstacl_distance}, 右{self.left_obstacl_distance}")
            time.sleep(1)
        # return (left,right,)

    def drive(self,speed):
        """根据障碍探测进行总的调度"""
        while True:
            # mycar.move_forward(speed)
            left,right = self.left_obstacl_distance, self.right_obstacl_distance
            if left == 0 and right == 1:
                mycar.stop()
                # mycar.move_backward(speed)
                mycar.turn_right(speed)
                mycar.move_forward(speed)

            elif right == 0 and left == 1:
                mycar.stop()
                # mycar.move_backward(speed)
                mycar.turn_left(speed)
                mycar.move_forward(speed)
            
            elif right ==  0 and left == 0:
                mycar.stop()
                mycar.move_backward(speed)
                mycar.turn_right(speed)
            
            elif right == 1 and left == 1:
                mycar.move_forward(speed)

    
    def destroy():
        GPIO.cleanup()
    

if __name__ == "__main__":
    mycar = car()
    mycar.set_up("wjj")
    try:
        mode = int(input("请选择运行的模式：1.手动 2.自动探测"))
        if mode == 1:
            direction = int(input("请控制运行的方向：1.前移 2.后移 3.左移 4.右移: "))
            speed = int(input("请输入速度:1-10挡: "))
            if direction==1:
                mycar.move_forward(speed)
            elif direction==2:
                mycar.move_backward(speed)
            elif direction==3:
                mycar.turn_left(speed)
            elif direction==4:
                mycar.turn_right(speed)
        
        elif mode == 2:
            speed = int(input("请输入速度:1-10挡: "))
            speed *= 10

            detect_thread = threading.Thread(target=mycar.detect_obstacles)
            detect_thread.start()
            
            drive_thread = threading.Thread(target=mycar.drive,args=(speed,))
            drive_thread.start()
                
            # while True:
            #     # 移动方向的切换应当设为一个监控线程！
            #     mycar.move_forward(speed)
            #     left,right = mycar.detect_obstacles()
            #     if left == 1 and right == 0:
            #         mycar.stop()
            #         mycar.move_backward(speed)
            #         mycar.turn_right(speed)
            #         mycar.move_forward(speed)

            #     elif right == 1 and left == 0:
            #         mycar.stop()
            #         mycar.move_backward(speed)
            #         mycar.turn_left(speed)
            #         mycar.move_forward(speed)
                
            #     elif right == 0 and left == 0:
            #         mycar.stop()
            #         mycar.move_backward(speed)
            
    except:
        mycar.destroy()
