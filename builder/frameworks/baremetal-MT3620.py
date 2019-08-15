# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
from os.path import join
from common import *
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder

def dev_create_template(env):
    hardwares = join(env.framework_dir, "Hardwares")
    templates = join(env.framework_dir, "Templates")
    core = env.BoardConfig().get("build.variant")
    print "TEMPLATES", templates 
    F = [ 
        join(templates, "baremetal.c"), 
        join(templates, "app_manifest.json"),  
    ]
    for src in F:
        head, fname = os.path.split(src)
        dst = join( env.subst("$PROJECT_DIR"), "src", fname)        
        if False == os.path.isfile( dst ):
            copyfile(src, dst)

def dev_compiler(env):
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("//", "/"),
        AR="arm-none-eabi-ar",
        AS="arm-none-eabi-as",
        CC="arm-none-eabi-gcc",
        GDB="arm-none-eabi-gdb",
        CXX="arm-none-eabi-g++",
        OBJCOPY="arm-none-eabi-objcopy",
        RANLIB="arm-none-eabi-ranlib",
        SIZETOOL="arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:/.text|/.data|/.bootloader)/s+(/d+).*",
        SIZEDATAREGEXP=r"^(?:/.data|/.bss|/.noinit)/s+(/d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGNAME="app",
        PROGSUFFIX=".elf",  
    )

def dev_init(env, platform):
    env.tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    env.framework_dir = env.PioPlatform().get_package_dir("framework-azure")
    env.toolchain_dir = env.PioPlatform().get_package_dir("toolchain-gccarmnoneeabi")     
    env.baremetal = True 
    dev_create_template(env)
    dev_compiler(env)
    env.sysroot = env.BoardConfig().get("build.sysroot", "2+Beta1905") # INI file, default must be BETA
    print '/033[1;34;40m'+"AZURE SPHERE SDK SYSROOT:", env.sysroot, "[",env.BoardConfig().get("build.core").upper(),"]", env.BoardConfig().get("build.variant")
    env.Append(
        CPPDEFINES = [],        
        CPPPATH = [ 
            join(env.framework_dir, "Sysroots", env.sysroot, "usr", "include"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
        ],        
        CFLAGS = [
            "-O0", "-c",
            "-mcpu=cortex-m4", "-mfloat-abi=soft", "-march=armv7e-m", "-mthumb", 
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
            "-mcpu=cortex-m4", "-mfloat-abi=soft", "-march=armv7e-m", "-mthumb",                                                                                                    
        ],        
        #LIBPATH = [], 
        LDSCRIPT_PATH = join(env.framework_dir, "Sysroots", env.sysroot, "linker.ld"),              
        LINKFLAGS = [  
            "-mcpu=cortex-m4", "-mfloat-abi=soft", "-march=armv7e-m", "-mthumb", 
            "-nostartfiles", 
            "-Wl,--no-undefined", 
            "-Wl,-n",
        ],  
        LIBSOURCE_DIRS=[ join(env.framework_dir, platform, "libraries"), ], # userware       
        LIBS = [ "gcc" ],               
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





    
