# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/platform-azure

from os.path import join
from common import *
from SCons.Script import Builder

def dev_init(env, platform):
    dev_create_template(env, [ "main.c", "app_manifest.json" ])
    dev_initialize(env, False)
    env.Append(
        CPPDEFINES = [ "_POSIX_C_SOURCE" ],        
        CPPPATH = [ 
            join(env.sysroot_dir, "usr", "include"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
        ],        
        CFLAGS = [ 
            "-O0", 
            "-std=c11", 
            "--sysroot=" + env.sysroot_dir,
            "-fno-omit-frame-pointer", 
            "-fno-strict-aliasing",  
            "-Wall",    
            "-fno-exceptions",
                                                                   
        ],  
        CXXFLAGS = [ 
            "-O0",                               
            "-fno-rtti",
            "-fno-exceptions", 
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
            "-fno-threadsafe-statics",
        ],  
        CCFLAGS = [ env.cortex ],                     
        LINKFLAGS = [ 
            env.cortex,
            "--sysroot=" + env.sysroot_dir,
            "-B", env.toolchain_dir,
            "-nodefaultlibs",
            "-Wl,--no-undefined", 
        ],  
        LIBSOURCE_DIRS=[ join(env.framework_dir, platform, "libraries"), ],      
        LIBPATH = [ join("$PROJECT_DIR", "lib") ], # -L
        LIBS = [ "c", "gcc_s", "applibs", "azureiot", "curl" ],               
        BUILDERS = dict( PackImage = Builder( 
                action = env.VerboseAction(dev_image_pack, " "),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_image_upload
    )
    dev_experimental_mode(env)
    libs = []    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))         
    #USER     
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_user"),
            join(env.framework_dir, platform, "libraries"),
    ))     
    env.Append(LIBS = libs)   





    
