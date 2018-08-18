import ctypes
import pykeyboard
import random
import time
import win32api
import win32gui
import win32process


# 宏定义键盘函数
key = pykeyboard.PyKeyboard()


# 模式记录变量
mode = input("Mode:\n")

# 起始位置记录变量
start = input("Start:\n")

# 用户目标记录变量
gola = input("Gola:\n")       

# 存档指示变量
late_archive = 2

# 寄存器变量
brick = ctypes.c_int()      # 砖块
bridge = ctypes.c_int()         # 桥
environment = ctypes.c_int()        # 环境
firstworld = ctypes.c_int()     # 大关卡
jump = ctypes.c_int()       # 跳跃状态
lastworld = ctypes.c_int()      # 小关卡
live = ctypes.c_int()       # 生命状态
load = ctypes.c_int()       # 加载
pipeline = ctypes.c_int()       # 水管
speed = ctypes.c_int()      # 移动速度

# 数据记录变量
back_times = 0      # 读档次数
dead_times = 0      # 死亡次数
jump_times = 0      # 跳跃次数
stop_times = 0      # 撞墙次数
used_second = 0     # 使用时间


# 打开工作环境
win32api.ShellExecute(None, "open", ".\\Little Leong\\rams\\Super Mario Bros.nes", None, None, 1)       # 方式为活跃的窗口

# 等待窗口打开
time.sleep(0.5)

# 获得内存接口
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)      # 获得进程所有能获得的访问权限
hwnd = win32gui.FindWindow("VirtuaNESwndclass", "VirtuaNES - Super Mario Bros")     # 获得进程顶层窗口的句柄
hid,pid = win32process.GetWindowThreadProcessId(hwnd)       # 获得进程顶层窗口的PID
phand = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)        # 打开进程顶层窗口的句柄

# 获得内存管理方法
kerneldll = ctypes.windll.LoadLibrary(".\\kernel32.dll")        # 以stdcall调用约定加载

# 等待接口设置结束
time.sleep(0.5)


def get_brick():
    '''
    读取砖块位置的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A6E8, ctypes.byref(brick), 1, None)
    return brick.value


def get_bridge():
    '''
    读取桥梁状态的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A6D4, ctypes.byref(bridge), 1, None)
    return bridge.value


def get_environment():
    '''
    读取环境状态的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A6B2, ctypes.byref(environment), 1, None)
    return environment.value


def get_firstworld():
    '''
    读取大关卡位置的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A6C3, ctypes.byref(firstworld), 1, None)
    return firstworld.value


def get_jump():
    '''
    读取跳跃状态的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x00599F81, ctypes.byref(jump), 1, None)
    return jump.value


def get_lastworld():
    '''
    读取小关卡位置的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A6C0, ctypes.byref(lastworld), 1, None)
    return lastworld.value


def get_live():
    '''
    读取生命状态内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A715, ctypes.byref(live), 1, None)
    return live.value


def get_load():
    '''
    读取加载状态的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x00576F8C, ctypes.byref(load), 1, None)
    return load.value


def get_pipeline():
    '''
    读取水管状态的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x00599F68, ctypes.byref(pipeline), 1, None)
    return pipeline.value


def get_speed():
    '''
    读取移动速度的内存；

    '''
    kerneldll.ReadProcessMemory(int(phand), 0x0059A664, ctypes.byref(speed), 1, None)
    return speed.value


def jump_random(k):
    '''
    回档或半随机高度跳跃；
    k > 0时会尝试半随机高度跳跃，否则二级回档；

    '''
    # 声明全局变量
    global late_archive
    global back_times
    global dead_times
    global jump_times
    global stop_times

    if get_environment() == 0:
        a = "o"
        b = 2.0
    else:
        a = "l"
        b = 0.7

    # 重置跳跃键
    key.release_key(a)    

    # 一级回档
    key.press_key(key.function_keys[late_archive])
    time.sleep(0.05)
    key.release_key(key.function_keys[late_archive])
    back_times += 1

    if k > 0:
        # 起跳
        key.press_key(a)
        jump_times += 1

        # 半随机跳跃高度
        i = random.uniform(0.0, b)
        j = time.time()

        # 上升阶段
        while time.time() - j < i:

            # 拉旗与断桥的判定
            if get_jump() == 3 or get_bridge() == 2:
                key.release_key(a)

                # 等待进入加载状态
                while get_load() != 36:
                    pass

                next_pass()
                return 0

            # 生命状态的判定
            if get_live() == 1:
                dead_times += 1
                jump_random(k - 1)
                return 0

        # 重置跳跃键
        key.release_key(a)

        # 下降阶段
        while get_jump() != 0:

            # 拉旗与断桥的判定
            if get_jump() == 3 or get_bridge() == 2:
                key.release_key(a)

                # 等待进入加载状态
                while get_load() != 36:
                    pass

                next_pass()
                return 0

            # 生命状态的判定
            if get_live() == 1:
                dead_times += 1
                jump_random(k - 1)
                return 0

            # 移动速度的判定
            if get_speed() <= 5:
                stop_times += 1
                jump_random(k - 1)
                return 0

    else:
        # 二级回档
        late_archive -= 1
        if late_archive == 1:
            late_archive = 8
        key.press_key(key.function_keys[late_archive])
        time.sleep(0.05)
        key.release_key(key.function_keys[late_archive])
        back_times += 1
        late_archive -= 1
        if late_archive == 1:
            late_archive = 8
    return 0



def walk_up():
    '''
    尝试性前进；

    '''
    # 声明全局变量
    global late_archive
    global dead_times
    global jump_times
    global stop_times

    # 加速前进
    key.press_key("k")
    key.press_key("d")

    # 在地面时存档
    if get_jump() == 0:
        late_archive += 1
        if late_archive == 9:
            late_archive = 2        
        key.press_key(str(late_archive))
        time.sleep(0.05)
        key.release_key(str(late_archive))

    #半随机前进距离
    i = random.uniform(0.2, 0.5)
    j = time.time()

    # 前进或未落地阶段
    while time.time() - j < i or get_jump() != 0:
        # 进入水管的判定
        if get_pipeline() == 32:
            while get_pipeline() == 32:
                pass

            # 切换世界时视为出了水管，所以要进行双重判定
            while get_pipeline() == 32:
                pass
            break

        # 生命状态的判定
        if get_live() == 1:
            dead_times += 1
            jump_random(5)
            break

        # 移动速度的判定
        if get_speed() <= 5:
            # 防止起步时的误判
            time.sleep(0.2)

            if get_speed() <= 5:
                stop_times += 1
                jump_random(5)
                break
    return 0


def next_pass():
    '''
    储存练习记录；
    练习前的初始化；

    '''
    # 声明全局变量
    global late_archive

    # 释放
    key.release_key("k")
    key.release_key("d")

    # 获得关卡计数
    if get_lastworld() == 0:
        i = get_firstworld()
        j = 4
    else:
        i = get_firstworld() + 1
        j = get_lastworld()

    # 判定是否完成目标
    if gola == str(i) + "-" + str(j):
        key.press_key("h")
        time.sleep(0.05)
        key.release_key("h")
        test()
        return 0

    # 为下面的记录进行调整
    if j == 4:
        i += 1
        j = 1
    else:
        j += 1

    # 小关卡记录
    if mode == "":
        key.press_key("h")
        time.sleep(0.05)
        key.release_key("h")

        key.press_key("g")
        time.sleep(0.05)
        key.release_key("g")
        key.type_string(str(i) + "-" + str(j))
        key.tap_key(key.enter_key)
        key.tap_key("y")

    # 大关卡记录
    elif mode == "long":
        if j == 1:
            key.press_key("h")
            time.sleep(0.05)
            key.release_key("h")

            key.press_key("g")
            time.sleep(0.05)
            key.release_key("g")
            key.type_string(str(i) + "-0")
            key.tap_key(key.enter_key)
            key.tap_key("y")

    # 全关卡记录
    elif mode == "all":
        if str(i) + "-" + str(j) == "1-1":
            key.press_key("g")
            time.sleep(0.05)
            key.release_key("g")
            key.type_string("all")
            key.tap_key(key.enter_key)
            key.tap_key("y")

    # 初始化存档指示变量
    late_archive = 2

    # 等待加载结束
    while get_load() == 36:
        pass

    # 确认已落地
    while get_jump() == 0:
        pass

    # 调试用的后门
    key.press_key("9")
    time.sleep(0.05)
    key.release_key("9")

    # 初始化首个存档
    key.press_key("2")
    time.sleep(0.05)
    key.release_key("2")
    return 0


def test():
    '''
    练习结束后的测试；

    '''
    # 声明全局变量
    global used_second
    used_second = time.time() - used_second

    # 读取记录文件
    key.press_key("b")
    time.sleep(0.05)
    key.release_key("b")
    if mode == "all":
        key.type_string("all")
    elif mode == "long":
        key.type_string(str(get_firstworld()) + "-0")
    else:
        key.type_string(gola)
    key.tap_key(key.enter_key)

    # 输出数据记录
    print("================================================")
    print("完成目标 %s 共计：" % gola)
    print("尝试 %d 次" % back_times)
    print("死亡 %d 次" % dead_times)
    print("跳跃 %d 次" % jump_times)
    print("撞墙 %d 次" % stop_times)
    print("用时 %f 秒" % used_second)

    input()
    exit(0)


def main():
    '''
    实现工作模式的选择；

    '''
    # 声明全局变量
    global used_second

    # 不设置起点
    if start == "":
        key.press_key("j")
        time.sleep(0.05)
        key.release_key("j")

    # 移动到起点
    else:
        # 读取记录文件
        key.press_key("b")
        time.sleep(0.05)
        key.release_key("b")
        key.type_string(start)
        key.tap_key(key.enter_key)

        # 等待移动到起点
        while True:
            if get_lastworld() == 0:
                i = get_firstworld()
                j = 4
            else:
                i = get_firstworld() + 1
                j = get_lastworld()
            if j == 4 and start == str(i) + "-0":
                break
            if start == str(i) + "-" + str(j):
                break

        # 未设置终点时直接退出
        if gola == "":
            input()
            exit(0)

    # 开始练习
    next_pass()
    used_second = time.time()
    while True:
        walk_up()
        print("尝试：%d；  死亡：%d；  跳跃：%d；  撞墙：%d；" % (back_times, dead_times, jump_times, stop_times))


main()
