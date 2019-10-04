# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
from os.path import join
from common import *
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder
from colorama import Fore

def dev_create_template(env):
    hardwares = join(env.framework_dir, "Hardwares")
    templates = join(env.framework_dir, "Templates")
    core = env.BoardConfig().get("build.variant")
    print( "TEMPLATES", templates )
    F = [ 
        join(templates, "main.c"), 
        join(templates, "app_manifest.json"),  
        join(templates, "epoll_timerfd_utilities.c"), 
        join(templates, "epoll_timerfd_utilities.h"),
        join(hardwares, "json", core + ".json"),
    ]
    for src in F:
        head, fname = os.path.split(src)
        dst = join( env.subst("$PROJECT_DIR"), "src", fname)        
        if False == os.path.isfile( dst ):
            copyfile(src, dst)


def dev_init(env, platform):
    env.tool_dir = env.PioPlatform().get_package_dir("tool-azure")
    env.framework_dir = env.PioPlatform().get_package_dir("framework-azure")
    env.toolchain_dir = env.PioPlatform().get_package_dir("toolchain-arm-poky-linux-musleabi-hf")  
    env.baremetal = False      
    dev_create_template(env)
    dev_guid(env)
    dev_compiler_poky(env)
    env.sysroot = env.BoardConfig().get("build.sysroot", "2+Beta1905") # from ini file, default is max api 
    env.delete = env.BoardConfig().get("build.delete", "all")          # from ini file, delete 'current' or 'all'
    print( Fore.MAGENTA+"AZURE SPHERE SDK SYSROOT:", env.sysroot, "[",env.BoardConfig().get("build.core").upper(),"]", env.BoardConfig().get("build.variant"),Fore.BLACK )
    env.Append(
        CPPDEFINES = [ 
            "_POSIX_C_SOURCE",
            "SYSROOT_" + env.sysroot.upper().replace("+", "_"), # -DSYSROOT_X
        ],        
        CPPPATH = [ 
            join(env.framework_dir, "Sysroots", env.sysroot, "usr", "include"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
        ],        
        CFLAGS = [
            "-O0", "-c",
            "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7", "-std=c11", 
            "--sysroot=" + join(env.framework_dir, "Sysroots", env.sysroot),
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
            "--sysroot=" + join(env.framework_dir, "Sysroots", env.sysroot),
            "-B", env.toolchain_dir,
            "-nodefaultlibs",
            "-Wl,--no-undefined", 
        ],  
        LIBSOURCE_DIRS=[ join(env.framework_dir, platform, "libraries"), ],      
        LIBPATH = [ join("$PROJECT_DIR", "lib") ], # -L
        LIBS = [ "c", "gcc_s", "applibs", "azureiot", "curl" ],               
        BUILDERS = dict(
            ElfToBin = Builder(action="", suffix=".1"),
            MakeHeader = Builder( 
                action = env.VerboseAction(dev_pack_image, "Packing image..."),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_uploader
    )
    dev_experimental_mode(env)
    libs = []    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))         
    env.Append(LIBS = libs)   
    use_original_sdk(env)





    
