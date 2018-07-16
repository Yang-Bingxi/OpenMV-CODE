# Untitled - By: weycen - 周四 七月 27 2017
# Blob Detection Example
#
# This example shows off how to use the find_blobs function to find color
# blobs in the image. This example in particular looks for dark green objects.
import sensor, image, time, pyb, time, stm
from pyb import UART, Timer, LED, Pin

# For color tracking to work really well you should ideally be in a very, very,
# very, controlled enviroment where the lighting is constant...
yellow_threshold  = (   69,   81,  18,   42,   34,   45)
white_threshold   = (   65,   76,  36,   52,   -2,   14)
black_threshold   = (   0,   75)
#设置各色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
#设置（min, max）两个数字即可。

#高度数据
highcnt = 0.0
high = 0
#xy平面误差数据
err_x = 0
err_y = 0

uart_buf = bytearray([0x55,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xAA])

# Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
led = pyb.LED(3)
led.intensity(50)

position_X=60
position_Y=60
def send_position():
    uart.writechar(0x58)
    uart.writechar(position_X)
    uart.writechar(position_Y)
    uart.writechar(0x59)
##超声波接收中断函数
#def Ultrasound(line):
   #if(Echo.value()==1):
        #tim_count.init(prescaler=1799, period=2500)#打开定时器
   #if(Echo.value()==0):
        #global highcnt
        #highcnt = tim_count.counter()#计数
        #tim_count.deinit()

#超声波发射端口配置
#timpwm = Timer(4, freq=30) #超声波60赫兹发射频率
#ch1 = timpwm.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width=80) #100us发射角

##超声波接收端口配置
#tim_count = pyb.Timer(1) #定时器计数
#extint = pyb.ExtInt('P0', pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_DOWN,Ultrasound)#开启外部中断,跳变沿
#Echo = Pin('P0', Pin.IN, Pin.PULL_DOWN)


#串口中断发送函数
def tick(timer):
    led.toggle()   #闪烁led
    uart.write(uart_buf)
    #print(uart_buf)#调试使用

#timer发送配置
senddata = Timer(2, freq=20)
senddata.callback(tick)

#串口三配置
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

# You may need to tweak the above settings for tracking green things...
# Select an area in the Framebuffer to copy the color settings.
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)#设置灰度信息
sensor.set_framesize(sensor.QQVGA)#设置图像大小
sensor.set_windowing((160, 120)) # 160*120 center pixels of VGA#设置图像大小
sensor.skip_frames(20)#相机自检几张图片
sensor.set_auto_whitebal(False)#关闭白平衡
sensor.set_auto_gain(False)    #关闭自动增益
#关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    #high = int(1.7*highcnt) #计算高度
    img = sensor.snapshot() # Take a picture and return the image.

    """
    blobs = img.find_blobs([yellow_threshold])
    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。
    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记
            #print(b[5], b[6])
            #输出目标物体中心坐标
            print(b[9])
            uart.writechar(b[9])
    """

    #blobs_y = img.find_blobs([yellow_threshold])
    #if blobs_y:
        #most_pixels = 0
        #largest_blob = 0
        #for i in range(len(blobs_y)):
            #if blobs_y[i].pixels() > most_pixels:
                #most_pixels = blobs_y[i].pixels()
                #largest_blob = i
        #center_x = int(blobs_y[largest_blob].cx())
        #center_y = int(blobs_y[largest_blob].cy())
        ##img.draw_rectangle(blobs_y[largest_blob][0:4])
        ##img.draw_cross(blobs_y[largest_blob].cx(),blobs_y[largest_blob].cy())#调试使用
        ##print("yellow:"),
        ##print(blobs_y[largest_blob][5], blobs_y[largest_blob][6])
        ##数组中数据写入
        ##uart_buf = bytearray([0x55,0xAA,0x10,0x00,0x00,0x00,0x00,0x00,0xAA])



    #blobs_w = img.find_blobs([white_threshold])
    #if blobs_w:
        #most_pixels = 0
        #largest_blob = 0
        #for i in range(len(blobs_w)):
            #if blobs_w[i].pixels() > most_pixels:
                #most_pixels = blobs_w[i].pixels()
                #largest_blob = i
        #center_x = int(blobs_w[largest_blob].cx())
        #center_y = int(blobs_w[largest_blob].cy())
        ##img.draw_rectangle(blobs_w[largest_blob][0:4])
        ##img.draw_cross(blobs_w[largest_blob].cx(),blobs_w[largest_blob].cy())#调试使用
        ##print("white:"),
        ##print(blobs_w[largest_blob][5], blobs_w[largest_blob][6])



    blobs_b = img.find_blobs([black_threshold], pixels_threshold=200, area_threshold=200, merge=True)
    if blobs_b:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs_b)):
            if blobs_b[i].pixels() > most_pixels:
                most_pixels = blobs_b[i].pixels()
                largest_blob = i
        center_x = int(blobs_b[largest_blob].cx())
        center_y = int(blobs_b[largest_blob].cy())
        position_X = center_x
        position_Y = center_y
        send_position()
        #位置环用到的变量
        err_y = int(60-center_y)
        err_x = int(60-center_x)
        #img.draw_rectangle(blobs_b[largest_blob][0:4])
        #img.draw_cross(blobs_b[largest_blob].cx(),blobs_b[largest_blob].cy())#调试使用
        #print("black:"),
        print(blobs_b[largest_blob][5], blobs_b[largest_blob][6])

        img.draw_rectangle(blobs_b[i][0:4])
        img.draw_cross(blobs_b[i][5], blobs_b[i][6])
        print(blobs_b[i][9])
        #uart.writechar(blobs_b[i][9])

    else:
        err_x = 500
        err_y = 500
    #数组中数据写入
    uart_buf = bytearray([0x55,0xAA,high>>8,high,err_x>>8,err_x,err_y>>8,err_y,0xAA])
    #print("black:")
    #print(err_x)
    #print(err_y)
    print("err_x={},err_y={}".format(err_x,err_y))
    #print(high)
    #stm.mem32[stm.UART4+stm.USART_DR] = 0x01




    #print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
