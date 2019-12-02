# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/platform-azure

from os.path import join
from common import *
from SCons.Script import Builder

def dev_init(env, platform):
    print(env.get("PIOFRAMEWORK")[0])
    dev_create_template(env, [ "mediatek.c", "app_manifest.json" ])
    dev_initialize(env, True)
    env.Append(
        CPPDEFINES = ['OSAI_BARE_METAL'],        
        CPPPATH = [ 
            join(env.framework_dir, "Mediatek", "HDL", "inc"),     
            join(env.framework_dir, "Mediatek", "MHAL", "inc"), 
            join(env.framework_dir, "Mediatek", "mt3620", "inc"),  
            join(env.framework_dir, "Mediatek", "OS_HAL", "inc"),  
            join(env.framework_dir, "Mediatek", "CMSIS", "include"),             
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")         
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
        CCFLAGS = [ env.cortex ], 
        LINKFLAGS = [ 
            env.cortex, 
            "-nostartfiles", 
            "-Wl,--no-undefined", 
            "-Wl,-n",
            "--entry=RTCoreMain",
            '-specs=nano.specs'
        ],  
        LDSCRIPT_PATH = join(env.framework_dir, "Hardwares", "linker.ld"),              
        #LIBPATH = [], 
        LIBSOURCE_DIRS=[ join(env.framework_dir, platform, "libraries"), ], # userware       
        LIBS = [ "gcc" ],               
        BUILDERS = dict( PackImage = Builder( 
                action = env.VerboseAction(dev_image_pack, " "),
                suffix = ".bin"
            )  
        ), 
        UPLOADCMD = dev_image_upload
    )

    libs = []    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom"), 
            join("$PROJECT_DIR", "lib"),                       
    ))       
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_HDL"), 
            join(env.framework_dir, 'Mediatek', "HDL", 'src'),                       
    ))        
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_MHAL"), 
            join(env.framework_dir, 'Mediatek', "MHAL", 'src'),                       
    ))   
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_mt3620"), 
            join(env.framework_dir, 'Mediatek', "mt3620", 'src'),                       
    ))    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_OS_HAL"), 
            join(env.framework_dir, 'Mediatek', "OS_HAL", 'src'),                       
    ))        
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_common"), 
            join(env.framework_dir, 'Mediatek', "src"),                       
    ))            
    env.Append(LIBS = libs)  



    
