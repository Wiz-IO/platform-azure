# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/platform-azure

from os.path import join
from common import *
from SCons.Script import Builder

def dev_init(env, platform):
    dev_create_template(env, [ "mediatek.c", "app_manifest.json" ])
    dev_initialize(env, True)
    if 'hard' == env.BoardConfig().get("build.float", "soft"):
        env.cortex = ["-mcpu=cortex-m4", "-mfloat-abi=hard", "-mfpu=fpv4-sp-d16", "-mthumb"] 
    env.Append(
        CPPDEFINES = [], # 'OSAI_BARE_METAL'        
        CPPPATH = [ 
            join(env.framework_dir, "Mediatek", "HDL", "inc"),     
            join(env.framework_dir, "Mediatek", "MHAL", "inc"), 
            join(env.framework_dir, "Mediatek", "mt3620", "inc"),  
            join(env.framework_dir, "Mediatek", "OS_HAL", "inc"),  
            join(env.framework_dir, "Mediatek", "CMSIS", "include"),             
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include"),     
        ],  
        ASFLAGS=[
            env.cortex,
            "-x", "assembler-with-cpp"
        ],                  
        CFLAGS = [ 
            env.cortex,
            "-O0",              
            "-Wall",  
            "-Wfatal-errors",
            "-fno-strict-aliasing",   
            "-fno-exceptions",                                                                   
        ],  
        LINKFLAGS = [ 
            env.cortex, 
            "-O0",            
            "-Wall",   
            "-Wfatal-errors",              
            "-Wl,--no-undefined", 
            "-Wl,-n",
            "-nostartfiles", 
            "--entry=RTCoreMain",
            "-specs=nano.specs",
            "-Xlinker", "--gc-sections",              
            "-Wl,--gc-sections",               
        ],  
        LDSCRIPT_PATH = join(env.framework_dir, "Hardwares", "linker.ld"),                          
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

    ### IF FREERTOS
    if 'enable' == env.BoardConfig().get("build.freertos", ""):
        env.Append(
            CPPDEFINES = ['FREERTOS'],      
            CPPPATH = [
                join(env.framework_dir, "FreeRTOS", "include"),
                join(env.framework_dir, "FreeRTOS", "src"),
            ] 
        )
        libs.append(
            env.BuildLibrary(
                join("$BUILD_DIR", "_freertos"), 
                join(env.framework_dir, 'FreeRTOS', "src"),                       
        ))  

    env.Append(LIBS = libs)  



    
