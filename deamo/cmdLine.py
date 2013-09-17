# -*- coding: utf-8 -*-

import argparse

args = "-f hello.txt -n 1 2 3 -x 100 -y b -z a -q hello @args.txt i_am_bar -h".split()
# 使用@args.txt要求fromfile_prefix_chars="@"
# args.txt文件中应该一行一个参数，想改变行为参考convert_arg_line_to_args()


# ArgumentParser参数的简单说明
# # description - 命令行帮助的开始文字，大部分情况下，我们只会用到这个参数
# epilog - 命令行帮助的结尾文字
# prog - (default: sys.argv[0])程序的名字，一般不需要修改，另外，如果你需要在help中使用到程序的名字，可以使用%(prog)s
# prefix_chars - 命令的前缀，默认是-，例如-f/--file。有些程序可能希望支持/f这样的选项，可以使用prefix_chars="/"
# fromfile_prefix_chars - (default: None)如果你希望命令行参数可以从文件中读取，就可能用到。例如，如果fromfile_prefix_chars='@',命令行参数中有一个为"@args.txt"，args.txt的内容会作为命令行参数
# add_help - 是否增加-h/-help选项 (default: True)，一般help信息都是必须的，所以不用设置啦。
# #  parents - 类型是list，如果这个parser的一些选项跟其他某些parser的选项一样，可以用parents来实现继承，例如parents=[parent_parser]
# # formatter_class - 自定义帮助信息的格式（description和epilog）。默认情况下会将长的帮助信息进行<自动换行和消除多个连续空白>。
# 三个允许的值：
# class argparse.RawDescriptionHelpFormatter 直接输出description和epilog的原始形式（不进行自动换行和消除空白的操作）
# class argparse.RawTextHelpFormatter 直接输出description和epilog以及add_argument中的help字符串的原始形式（不进行自动换行和消除空白的操作）
# # class argparse.ArgumentDefaultsHelpFormatter 在每个选项的帮助信息后面输出他们对应的缺省值，如果有设置的话。这个最常用吧！
# argument_default - (default: None)设置一个全局的选项的缺省值，一般每个选项单独设置，所以这个参数用得少，不细说
# usage - (default: generated)如果你需要修改usage的信息（usage: PROG [-h] [--foo [FOO]] bar [bar ...]），那么可以修改这个，一般不要修改。
# conflict_handler - 不建议使用。这个在极端情况下才会用到，主要是定义两个add_argument中添加的选项的名字发生冲突时怎么处理，默认处理是抛出异常。
# 注释一行有##表示这几个参数比较常用
parser = argparse.ArgumentParser(description = "This is a description of %(prog)s", epilog = "This is a epilog of %(prog)s", prefix_chars = "-+", fromfile_prefix_chars = "@", formatter_class = argparse.ArgumentDefaultsHelpFormatter)

# ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
# add_argument的参数是比较复杂的。。。

# name or flags - 指定参数的形式，想写几个写几个，不过我们一般就写两个，一个短参数，一个长参数，看下面的例子"-f", "--file"
# 可选的选项，位置不固定，想怎么写就怎么写，默认是可选的
parser.add_argument("-f", "--file", help = "test test test")
# 位置固定的选项，例如"prog i_am_bar"，这样子的话，i_am_bar就是bar选项的值啦，默认是必须有的
parser.add_argument("bar", help = "test test test")

# nargs - 指定这个参数后面的value有多少个，例如，我们希望使用-n 1 2 3 4，来设置n的值为[1, 2, 3, 4]
parser.add_argument("-n", "--num", nargs = "+", type = int)
# 这里nargs="+"表示，如果你指定了-n选项，那么-n后面至少要跟一个参数，+表示至少一个,?表示一个或0个,*0个或多个，

# default - 如果命令行没有出现这个选项，那么使用default指定的默认值
parser.add_argument("+g", "++gold", help = "test test test", default = "test_gold")  # 需要prefix_chars包含"+"

# type - 如果希望传进来的参数是指定的类型（例如 float, int or file等可以从字符串转化过来的类型），可以使用
parser.add_argument("-x", type = int)

# choices - 设置参数值的范围，如果choices中的类型不是字符串，记得指定type哦
parser.add_argument("-y", choices = ['a', 'b', 'd'])

# required - 通常-f这样的选项是可选的，但是如果required=True那么就是必须的了
parser.add_argument("-z", choices = ['a', 'b', 'd'], required = True)

# metavar - 参数的名字，在显示 帮助信息时才用到.
parser.add_argument("-o", metavar = "OOOOOO")

# help - 设置这个选项的帮助信息
# dest - 设置这个选项的值就是解析出来后放到哪个属性中
parser.add_argument("-q", dest = "world")

args = parser.parse_args(args)  # 如果你没有args参数，那么就使用sys.argv，也就是命令行参数啦。有这个参数，就方便我们调试啊
# args.world就是-q的值啦

# action - The basic type of action to be taken when this argument is encountered at the command line.
# const - A constant value required by some action and nargs selections.
# 这两个自己看帮助文档啦，比较复杂
# http://docs.python.org/library/argparse.html

print (args)
