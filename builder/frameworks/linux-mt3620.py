# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
from os.path import join
from shutil import copyfile
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder
from subprocess import check_output, CalledProcessError, call
import tempfile
import json

def get_uuid(path):
    t = tempfile.TemporaryFile()
    try:
        output = check_output(path, stderr=t.seek(0))
    except CalledProcessError as e:
        result = e.returncode, t.read()
    else:
        result = 0, output
        print '\nUUID: ' + result[1]
    return result[1].replace("\r\n", "") 

def dev_copy_json(env):
    src = join(env.subst("$PROJECT_DIR"), "src", "app_manifest.json")
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    copyfile(src, dst)
    tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    uuid = get_uuid( join(tool_dir, "uuidgen-64") ) # or 32 
    with open(dst, 'r+') as f:
        data = json.load(f)
        data['ComponentId'] = uuid          # change this
        data['EntryPoint'] = "program.elf"  # change this
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()  

def dev_pack_image(target, source, env):
    try:
        os.remove(join(env.subst("$BUILD_DIR"), "program.img"))
    except:    
        pass
    dev_copy_json(env)
    cmd = []
    tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    dst = join(env.subst("$BUILD_DIR"), "app_manifest.json")
    cmd.append( join(tool_dir, "azsphere") ) 
    cmd.append("image")
    cmd.append("package-application")
    cmd.append("--input")
    cmd.append( env.subst("$BUILD_DIR") ) 
    cmd.append("--output")
    cmd.append( join(env.subst("$BUILD_DIR"), "program.img") ) # "manual.imagepackage" 
    cmd.append("--sysroot")
    cmd.append( env.sysroot )
    #cmd.append("--verbose")
    cmd.append("--hardwaredefinition")
    cmd.append( join(env.subst("$PROJECT_DIR"), "src", "hardware.json") ) 
    t = tempfile.TemporaryFile()
    try:
        output = check_output(cmd, stderr=t.seek(0))
    except CalledProcessError as e:
        result = e.returncode, t.read()
        print'Pack ERROR: ', result[0], result[1]
    else:
        result = 0, output
        print('\033[1;32;40m'+'Pack Image ' + result[1])    
    return


def dev_uploader(target, source, env):
    #azsphere device sideload delete
    #azsphere device sideload deploy --imagepackage manual.imagepackage
    return

def dev_create_template(env):
    src = join(env.PioPlatform().get_package_dir("framework-azure"), "templates")
    print "TEMPLATES", src
    F = [ "main.c", "app_manifest.json", "hardware.json", "epoll_timerfd_utilities.c", "epoll_timerfd_utilities.h" ]
    for I in F:
        dst = join( env.subst("$PROJECT_DIR"), "src", I)
        if False == os.path.isfile( dst ):
            copyfile(join(src, I), dst)

def dev_compiler_poky(env):
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-poky-linux-musleabi-ar",
        AS="arm-poky-linux-musleabi-as",
        CC="arm-poky-linux-musleabi-gcc",
        GDB="arm-poky-linux-musleabi-gdb",
        CXX="arm-poky-linux-musleabi-g++",
        OBJCOPY="arm-poky-linux-musleabi-objcopy",
        RANLIB="arm-poky-linux-musleabi-ranlib",
        SIZETOOL="arm-poky-linux-musleabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".elf",  
    )       

def dev_init(env, platform):
    dev_create_template(env)
    dev_compiler_poky(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-azure")
    gcc_dir = env.PioPlatform().get_package_dir("toolchain-arm-poky-linux-musleabi-hf")
    env.sysroot = env.BoardConfig().get("build.sysroot", "2") # INI file, default is 2 
    print '\033[1;34;40m'+"AZURE SPHERE SDK Sysroot:", env.sysroot
    env.Append(
        CPPDEFINES = [ "_POSIX_C_SOURCE" ],        
        CPPPATH = [ 
            join(framework_dir, "Sysroots", env.sysroot, "usr", "include"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
        ],        
        CFLAGS = [
            "-O0", "-c",
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7", "-std=c11", 
            "--sysroot=" + join(framework_dir, "Sysroots", env.sysroot),
            "-fno-omit-frame-pointer", 
            "-fno-strict-aliasing",  
            "-Wall",    
            "-fno-exceptions",
                                                                   
        ],  
        CXXFLAGS = [                                
            "-fno-rtti",
            "-fno-exceptions", 
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
            "-fno-threadsafe-statics",
        ],  
        CCFLAGS = [
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7",                                                                                                    
        ],                     
        LINKFLAGS = [  
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7", 
            "--sysroot=" + join(framework_dir, "Sysroots", env.sysroot),
            "-B", gcc_dir,
            "-nodefaultlibs",
            "-Wl,--no-undefined", 
        ],        
        LIBS = [ "applibs", "pthread", "gcc_s", "c"],               
        BUILDERS = dict(
            ElfToBin = Builder(action="", suffix=".1"),
            MakeHeader = Builder( 
                action = env.VerboseAction(dev_pack_image, "Packing image..."),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_uploader
    )
    libs = []    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))         
    env.Append(LIBS = libs)   





    
