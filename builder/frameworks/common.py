# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/platform-azure

import os, json, tempfile, shutil, uuid
from os.path import join, normpath, basename
from uuid import UUID
from shutil import copyfile
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
from time import sleep
from colorama import Fore

def clean(path):
    for c in os.listdir(path):
        full_path = os.path.join(path, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
    try: os.remove(path)     
    except: pass  

def execute(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    lines = out.decode().split("\r\n")
    if proc.returncode == 0: 
        COLOR = Fore.GREEN
    else: 
        COLOR = Fore.RED
    for i in range( len(lines) ):
        print( COLOR + lines[i] )
        sleep(0.02)
    if proc.returncode != 0:
        sleep(0.02)
        exit(1)
    return 0

def dev_guid(env, save = True):
    with open(join(env.subst("$PROJECT_DIR"), "src", "app_manifest.json"), 'r+') as f:
        data = json.load(f)
        NEW = True
        if 'ComponentId' in data:
            try:
                val = UUID(data['ComponentId'], version=4)
                NEW = False
            except ValueError:
                print( Fore.RED + "ERROR GUID ", )
        if True == NEW:
            GUID = str(uuid.uuid4()).upper()
            data['ComponentId'] = GUID
            print( Fore.BLUE + "GENERATED NEW GUID", GUID, Fore.BLACK )
        if True == save:
            f.seek(0)
            json.dump(data, f, indent=4) 
            f.truncate()         
    env.GUID = data['ComponentId']
    return env.GUID

def copy_files(env):
    list = env.BoardConfig().get("build.copy", " ").split()
    count = len(list) 
    for i in range(count):
        print( Fore.BLUE + "COPY TO IMAGE:" )
        print( list[i] )
        copyfile(join(env.subst("$PROJECT_DIR"), "src", list[i]), 
                 join(env.subst("$BUILD_DIR"), "approot", list[i])) 

def dev_copy_json(env):
    copy_files(env)
    PROJECT_DIR = env.subst("$PROJECT_DIR")    
    APP_MANIFEST = join(env.subst("$BUILD_DIR"), "approot", "app_manifest.json")
    copyfile(join(PROJECT_DIR, "src", "app_manifest.json"), APP_MANIFEST)
    print( Fore.BLUE + 'COMPONENT ID ' + dev_guid(env, False) + Fore.BLACK )
    with open(APP_MANIFEST, 'r+') as f:
        data = json.load(f)
        if env.baremetal == True:
            data['ApplicationType'] = "RealTimeCapable"                                                           
        data['Name'] = "APP_" + basename(normpath(PROJECT_DIR)).replace(" ", "") 
        data['EntryPoint'] = "/bin/app"                                                     
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()      

def dev_image_pack(target, source, env):
    BUILD_DIR = env.subst("$BUILD_DIR")
    APPROOT_DIR = join(BUILD_DIR, "approot") 
    bin = join(APPROOT_DIR, "bin")
    if True == os.path.isdir(APPROOT_DIR):
        clean(APPROOT_DIR)  
    if False == os.path.isdir(APPROOT_DIR):
        os.makedirs(APPROOT_DIR)   
    if False == os.path.isdir(bin):
        os.makedirs(bin) 
    copyfile(join(BUILD_DIR, "app.elf"), join(bin, "app"))
    dev_copy_json(env)
    cmd = []
    dst = join(BUILD_DIR, "app_manifest.json")
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("image")                 # image-package     SDK 19.10
    cmd.append("package-application")   # pack-application  SDK 19.10
    cmd.append("-i")
    cmd.append( APPROOT_DIR ) 
    cmd.append("-o")
    cmd.append( join(BUILD_DIR, "app.image") ) 
    cmd.append("-s")
    if env.baremetal: 
        cmd.append( env.sysroot ) # need to be beta
    else:
        cmd.append( env.sysroot[0] )
    if '0' != env.verbose: cmd.append("-v")
    if env.baremetal == False:
        cmd.append("-h")
        cmd.append( join(env.framework_dir, "Hardwares", "json", env.BoardConfig().get("build.variant") + ".json" ) )
    execute(cmd)        

def dev_image_upload(target, source, env):
    cmd = []
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("dev")
    cmd.append("sl")
    cmd.append("delete")
    WHO = 'ALL APPLICATIONS'
    if "current" == env.delete:
        cmd.append("-i")
        cmd.append(env.GUID)
        WHO = 'APPLICATION ' + env.GUID
    execute(cmd)
    print( Fore.CYAN + WHO + ' IS REMOVED' )
    cmd = []        
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("dev")
    cmd.append("sl")
    cmd.append("deploy")
    cmd.append("-p") 
    cmd.append(join(env.subst("$BUILD_DIR"), "app.image"))
    if '0' != env.verbose: cmd.append("-v")
    execute(cmd)
    print( Fore.CYAN + 'NEW APPLICATION IS READY' )

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
        PROGNAME="app",
        PROGSUFFIX=".elf",  
    )      
    env.Append(UPLOAD_PORT='azsphere') # upload_port = "must exist variable"
    env.cortex = [ "-march=armv7ve", "-mthumb", "-mfpu=neon", "-mfloat-abi=hard", "-mcpu=cortex-a7" ]
        
def dev_compiler_none(env):
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
    env.Append(UPLOAD_PORT='azsphere') # upload_port = "must exist variable"
    env.cortex = ["-mcpu=cortex-m4", "-mfloat-abi=soft", "-march=armv7e-m", "-mthumb"]

def dev_experimental_mode(env):
    if env.BoardConfig().get("build.ex_mode", "0") == "enable": # disabled by default
        env.Append( 
            LIBS       = [ "_wizio_c", "_wizio_wolfssl" ], 
            LIBPATH    = [ join(env.sysroot_dir, 'ex', "lib")  ],             
            CPPPATH    = [ join(env.sysroot_dir, 'ex', "include")  ],
            CPPDEFINES = [ "EX_MODE" ], 
        ) 
        print( Fore.BLUE + "AZURE SPHERE SDK EXPERIMENTAL MODE ENABLED"  )

def dev_set_sysroot(env):
    env.sdk = env.BoardConfig().get("build.sdk", "") 
    if "" == env.sdk:
        env.sdk = join(env.framework_dir, "Microsoft Azure Sphere SDK")
    else:
        if False == os.path.isdir(env.sdk):
            print(Fore.RED + "[ERROR] Microsoft Azure Sphere SDK not exist: {}".format(env.sdk))
            exit(1)
        print(Fore.BLUE + "--- USED SDK FROM EXTERNAL FOLDER ---")
    env.sysroot = env.BoardConfig().get("build.sysroot", "3+Beta1909") # default is max version
    env.sysroot_dir = join(env.sdk, "Sysroots", env.sysroot)
    if False == os.path.isdir(env.sysroot_dir):
        print(Fore.RED + "[ERROR] Sysroot '{}' not exist".format(env.sysroot_dir))
        exit(1)       

def dev_initialize(env, bare = True):
    env.baremetal = bare    
    env.tool_dir = join(env.PioPlatform().get_package_dir("tool-azure"), 'azsphere')
    env.framework_dir = env.PioPlatform().get_package_dir("framework-azure")  
    dev_set_sysroot(env)
    dev_guid(env)
    if bare: 
        dev_compiler_none(env)
        print( Fore.MAGENTA + "AZURE SPHERE SDK CORTEX M4 BAREMETAL " + \
            env.sysroot + " [ " + env.BoardConfig().get("build.variant").upper() + " ] " ) 
    else:
        env.toolchain_dir = env.PioPlatform().get_package_dir("toolchain-arm-poky-linux-musleabi-hf")
        dev_compiler_poky(env)
        print( Fore.BLUE + "AZURE SPHERE SDK CORTEX A7 SYSROOT " + \
            env.sysroot + " [ " + env.BoardConfig().get("build.variant").upper() + " ] " ) 
    env.delete = env.BoardConfig().get("build.delete", "all")   
    env.verbose = env.BoardConfig().get("build.verbose", "0")  

def dev_create_template(env, files):
    for src in files:
        src = join(env.PioPlatform().get_package_dir("framework-azure"), "Templates", src)
        head, fname = os.path.split(src)
        dst = join( env.subst("$PROJECT_DIR"), "src", fname)        
        if False == os.path.isfile( dst ):
            copyfile(src, dst)
