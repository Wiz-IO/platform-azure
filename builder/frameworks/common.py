# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO

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
    if proc.returncode == 0: COLOR = Fore.GREEN
    else: COLOR = Fore.RED
    for i in range( len(lines) ):
        print( COLOR + lines[i] )
        sleep(0.1)
    if proc.returncode != 0:
        sleep(0.1)
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
        print( Fore.BLUE + "COPY FILE TO IMAGE", list[i] )
        copyfile(join(env.subst("$PROJECT_DIR"), "src", list[i]), 
                 join(env.subst("$BUILD_DIR"), "approot", list[i])) 

def dev_copy_json(env):
    copy_files(env)
    PROJECT_DIR = env.subst("$PROJECT_DIR")    
    APP_MANIFEST = join(env.subst("$BUILD_DIR"), "approot", "app_manifest.json")
    copyfile(join(PROJECT_DIR, "src", "app_manifest.json"), APP_MANIFEST)
    print( Fore.BLUE + 'COMPONENT ID ', dev_guid(env, False), Fore.BLACK )
    with open(APP_MANIFEST, 'r+') as f:
        data = json.load(f)
        if env.baremetal == True:
            data['ApplicationType'] = "RealTimeCapable"                                                           
        data['Name'] = "APP_" + basename(normpath(PROJECT_DIR)).replace(" ", "") 
        data['EntryPoint'] = "/bin/app"                                                     
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()      

def dev_pack_image(target, source, env):
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
    cmd.append("image")
    cmd.append("package-application")
    cmd.append("-i")
    cmd.append( APPROOT_DIR ) 
    cmd.append("-o")
    cmd.append( join(BUILD_DIR, "app.image") ) 
    cmd.append("-s")
    cmd.append( '2' ) # workaround
    #cmd.append( env.sysroot )
    #cmd.append("-v")
    if env.baremetal == False:
        cmd.append("-h")
        cmd.append( join(env.framework_dir, "Hardwares", "json", env.BoardConfig().get("build.variant") + ".json" ) )
    return execute(cmd)        

def dev_uploader(target, source, env):
    cmd = []
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("delete")
    WHO = "ALL"
    if "current" == env.delete:
        cmd.append("-i")
        cmd.append(env.GUID)
        WHO = env.GUID
    if (0 == execute(cmd)):
        print( Fore.CYAN + WHO + ' APP IS REMOVED' )
    else: exit(1)
    cmd = []        
    cmd.append( join(env.tool_dir, "azsphere") ) 
    cmd.append("device")
    cmd.append("sideload")
    cmd.append("deploy")
    cmd.append("--imagepackage")
    cmd.append(join(env.subst("$BUILD_DIR"), "app.image"))
    #cmd.append("--verbose")
    rc = execute(cmd)
    if (0 == rc):
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
    env.Append(UPLOAD_PORT='azsphere') #upload_port = "must exist variable"

def use_original_sdk(env):
    env.SDK = "C:\\Program Files (x86)\\Microsoft Azure Sphere SDK"
    use_sdk = env.BoardConfig().get("build.use_sdk", 1) # disable from ini
    if 1 == use_sdk and hasattr(env, 'SDK') and os.path.isdir(env.SDK):
        env['ENV']['PATH'] = join(env.SDK, "Sysroots", env.sysroot, "tools", "gcc")
        env.tool_dir = join(env.SDK, "Tools")
        print( Fore.MAGENTA + "USED", env.SDK, Fore.BLACK )
        
def dev_experimental_mode(env):
    ex = join(env.framework_dir, "Sysroots", env.sysroot, "ex")
    if env.BoardConfig().get("build.ex_mode", "0") == "enable": # disabled by default
        env.Append( 
            LIBS       = [ "_wizio_c", "_wizio_wolfssl" ], 
            LIBPATH    = [ join(ex, "lib")  ],             
            CPPPATH    = [ join(ex, "include")  ],
            CPPDEFINES = [ "EX_MODE" ], 
        ) 
        print( Fore.RED + "AZURE SPHERE SDK EXPERIMENTAL MODE ENABLED"  )
