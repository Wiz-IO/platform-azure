# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/platform-azure

from os.path import join
from common import *
from SCons.Script import Builder

def dev_init(env, platform):
    dev_create_template(env, [ "main.cpp", "app_manifest.json" ])
    dev_initialize(env, True)
    env.Append(
        CPPDEFINES = [],        
        CPPPATH = [ 
            join(env.framework_dir,  platform, platform),
            join(env.framework_dir,  platform, "core"),
            join(env.framework_dir,  platform, "variants", env.BoardConfig().get("build.variant")),              
            join(env.framework_dir, "baremetal", "libraries", "MT3620", "src"),        
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include"),  
        ],        
        CFLAGS = [ 
            "-O0", 
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
        CCFLAGS = [ env.cortex, ],    
        LINKFLAGS = [ 
            env.cortex, 
            "-nostartfiles", 
            "-Wl,--no-undefined", 
            "-Wl,-n",
        ],                       
        LDSCRIPT_PATH = join(env.framework_dir, "Hardwares", "linker_cpp.ld"),              
        #LIBPATH = [],
        #LIBSOURCE_DIRS = [],     
        LIBS = [ "gcc" ],               
        BUILDERS = dict( PackImage = Builder( 
                action = env.VerboseAction(dev_image_pack, " "),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_image_upload
    )

    libs = []    
    #WIRING  
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_" + platform),
            join(env.framework_dir, platform, platform),
    ))     
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_core"),
            join(env.framework_dir, platform, "core"),
    ))    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_variant"),
            join(env.framework_dir, platform, "variants", env.BoardConfig().get("build.variant")),
    ))    
    #MT3690 
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_mt3620"),
            join(env.framework_dir, "baremetal", "libraries", "MT3620", "src"), 
    ))        
    #USER
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))         
    env.Append(LIBS = libs) 





    
